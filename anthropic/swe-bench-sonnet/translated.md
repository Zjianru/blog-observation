# 在SWE-bench Verified基准测试中刷新纪录：Claude 3.5 Sonnet的突破表现

来源：https://www.anthropic.com/engineering/swe-bench-sonnet

---

_我们最新升级的[Claude 3.5 Sonnet模型](https://www.anthropic.com/news/3-5-models-and-computer-use)在软件工程评估基准SWE-bench Verified中取得了49%的优异成绩，超越了此前最先进模型45%的表现。本文将详细解析我们围绕该模型构建的“智能体”系统，旨在帮助开发者充分发挥Claude 3.5 Sonnet的最佳性能。_

[SWE-bench](https://www.swebench.com/)是一个评估AI模型完成实际软件工程任务能力的基准测试平台。该基准专门测试模型如何解决来自热门开源Python代码库的GitHub问题。在每项测试任务中，AI模型会获得一个配置好的Python环境，以及该代码库在问题被解决前的工作副本。模型需要理解、修改并测试代码，最终提交其解决方案。

每个解决方案都会根据原始GitHub问题合并请求中的真实单元测试进行评分。这检验了AI模型是否能够实现与原始PR作者相同的功能。

SWE-bench不仅评估孤立的AI模型，而是评估整个“智能体”系统。在此语境中，“智能体”指的是AI模型与其周边软件框架的组合。这个框架负责生成输入模型的提示词、解析模型输出以执行操作，并管理交互循环——将模型前一步操作的结果整合到下一个提示中。即使使用相同的底层AI模型，智能体在SWE-bench上的表现也会因这个框架的不同而产生显著差异。

虽然存在许多评估大语言模型编码能力的基准测试，但SWE-bench之所以日益受到青睐，主要有以下几个原因：

1. 它采用真实项目中的实际工程任务，而非竞赛或面试风格的问题；
2. 该领域尚未饱和——存在广阔的改进空间。目前尚无模型在SWE-bench Verified测试集上突破50%的完成率（尽管截至本文撰写时，更新版Claude 3.5 Sonnet已达到49%）；
3. 它评估的是完整“智能体”而非孤立模型。开源开发者和初创企业在优化框架方面取得显著成果，能够基于相同模型大幅提升性能。

需注意，原始SWE-bench数据集包含部分必须依赖GitHub议题外额外信息才能解决的任务（例如涉及特定错误消息返回）。[SWE-bench-Verified](https://openai.com/index/introducing-swe-bench-verified/)作为SWE-bench的500题精选子集，经人工审核确保可解性，为编码智能体性能提供了最清晰的衡量标准。本文将以此作为基准参照。

## 实现尖端水平

### 工具调用型智能体

我们为优化更新版Claude 3.5 Sonnet设计智能体框架时，秉持的设计理念是：尽可能将控制权赋予语言模型本身，保持框架极简。该智能体包含提示指令、用于执行bash命令的Bash工具，以及用于查看编辑文件和目录的编辑工具。我们会持续采样直到模型自行判定任务完成，或超出其20万字符的上下文长度限制。这种框架设计使模型能自主判断问题解决路径，而非被硬编码到特定模式或工作流中。

提示指令为模型提供了建议解决路径，但并未针对此任务设置过长或过细的约束。模型可自由决定各步骤间的衔接方式，无需遵循严格离散的转换规则。若对令牌数量不敏感，明确鼓励模型生成详细响应将有助于任务执行。

以下代码展示我们智能体框架中的提示指令：

<uploaded_files>
{location}
</uploaded_files>
我已将 Python 代码仓库上传至目录 {location}（不在 /tmp/inputs 中）。请考虑以下 PR 描述：

<pr_description>
{pr_description}
</pr_description>

你能帮我实现对仓库的必要更改，以满足 <pr_description> 中指定的要求吗？
我已经处理了 <pr_description> 中描述的所有测试文件的更改。这意味着你**不需要**以任何方式修改测试逻辑或任何测试！

你的任务是对 {location} 目录中的非测试文件进行最小化更改，以确保满足 <pr_description> 的要求。

按照以下步骤解决问题：
1. 作为第一步，探索仓库以熟悉其结构可能是个好主意。
2. 创建一个脚本来重现错误，并使用 BashTool 通过 `python <filename.py>` 执行它，以确认错误
3. 编辑仓库的源代码以解决问题
4. 重新运行你的重现脚本，确认错误已修复！
5. 考虑边缘情况，并确保你的修复也能处理它们

你的思考应该彻底，所以即使很长也没关系。

Copy

模型的第一个工具执行 Bash 命令。其模式很简单，只接受要在环境中运行的命令。然而，该工具的描述更为重要。它包含了更详细的指令，包括转义输入、无网络访问权限以及如何在后台运行命令。

接下来，我们展示 Bash 工具的规范：

{
   "name": "bash",
   "description": "在bash shell中运行命令\n
* 调用此工具时，“command”参数的内容无需进行XML转义。\n
* 通过此工具无法访问互联网。\n
* 但可以通过apt和pip访问常见Linux及Python软件包的镜像源。\n
* 状态在命令调用和与用户的对话过程中是持久保留的。\n
* 若要检查文件的特定行范围（例如第10-25行），可尝试使用命令 'sed -n 10,25p /path/to/the/file'。\n
* 请避免运行可能产生大量输出的命令。\n
* 长时间运行的命令请在后台执行，例如 'sleep 10 &' 或在后台启动服务器。",
   "input_schema": {
       "type": "object",
       "properties": {
           "command": {
               "type": "string",
               "description": "要执行的bash命令。"
           }
       },
       "required": ["command"]
   }
}

模型的第二个工具（编辑工具）要复杂得多，它包含了模型查看、创建和编辑文件所需的一切功能。同样，我们的工具描述中为模型提供了关于如何使用该工具的详细信息。

我们投入了大量精力来完善这些工具在各种代理任务中的描述和规范。通过测试，我们发现了模型可能误解规范的方式或使用工具时潜在的陷阱，并据此修改描述以预先规避这些问题。我们认为，应当像设计人类使用的工具界面那样，投入更多精力来为模型设计工具接口。

以下代码展示了我们编辑工具的描述：

{
   "name": "str_replace_editor",
   "description": "用于查看、创建和编辑文件的自定义编辑工具\n
* 状态在命令调用和与用户的对话间持久保持\n
* 如果`path`是文件，`view`会显示应用`cat -n`的结果。如果`path`是目录，`view`会列出最多2层深的非隐藏文件和目录\n
* 如果指定的`path`已作为文件存在，则不能使用`create`命令\n
* 如果`command`生成长输出，它将被截断并标记为`<response clipped>`\n
* `undo_edit`命令将撤销对`path`处文件所做的最后一次编辑\n
\n
使用`str_replace`命令的注意事项：\n
* `old_str`参数应完全匹配原始文件中的一个或多个连续行。请注意空格！\n
* 如果`old_str`参数在文件中不唯一，则不会执行替换。确保在`old_str`中包含足够的上下文以使其唯一\n
* `new_str`参数应包含应替换`old_str`的编辑后行",
...

我们提升性能的一种方法是“防错”我们的工具。例如，有时在代理移出根目录后，模型可能会搞乱相对文件路径。为了防止这种情况，我们简单地让工具始终要求绝对路径。

我们尝试了多种指定对现有文件进行编辑的策略，其中字符串替换的可靠性最高，即模型在给定文件中指定用`new_str`替换`old_str`。只有当`old_str`恰好有一个匹配项时，才会执行替换。如果匹配项过多或过少，模型会看到相应的错误信息，以便重试。

我们的编辑工具的规范如下所示：

...
       "input_schema": {
           "type": "object",
           "properties": {
               "command": {
                   "type": "string",
                   "enum": ["view", "create", "str_replace", "insert", "undo_edit"],
                   "description": "要运行的命令。允许的选项包括：`view`、`create`、`str_replace`、`insert`、`undo_edit`。"
               },
               "file_text": {
                   "description": "`create` 命令的必需参数，包含要创建的文件内容。",
                   "type": "string"
               },
               "insert_line": {
                   "description": "`insert` 命令的必需参数。`new_str` 将被插入到 `path` 文件的第 `insert_line` 行之后。",
                   "type": "integer"
               },
               "new_str": {
                   "description": "`str_replace` 命令的必需参数，包含新字符串。`insert` 命令的必需参数，包含要插入的字符串。",
                   "type": "string"
               },
               "old_str": {
                   "description": "`str_replace` 命令的必需参数，包含 `path` 中要被替换的字符串。",
                   "type": "string"
               },
               "path": {
                   "description": "文件或目录的绝对路径，例如 `/repo/file.py` 或 `/repo`。",
                   "type": "string"
               },
               "view_range": {
                   "description": "当 `path` 指向文件时，`view` 命令的可选参数。如果未提供，则显示整个文件。如果提供，文件将在指定的行号范围内显示，例如 [11, 12] 将显示第 11 和 12 行。行号从 1 开始索引。设置 `[start_line, -1]` 将显示从 `start_line` 到文件末尾的所有行。",
                   "items": {
                       "type": "integer"
                   },
                   "type": "array"
               }
           },
           "required": ["command", "path"]
       }

## 结果

总体而言，升级后的Claude 3.5 Sonnet在推理、编程和数学能力方面均超越了我们先前的模型以及[先前的最先进模型](https://solverai.com/)。它还展现出更强的代理能力：工具和框架的辅助使其改进的能力得以充分发挥。

模型| **Claude 3.5 Sonnet（新版）**| 先前最优模型| Claude 3.5 Sonnet（旧版）| Claude 3 Opus
---|---|---|---|---
SWE-bench验证得分| 49%| 45%| 33%| 22%

部分模型在SWE-bench验证中的得分，均使用此代理框架。

## 代理行为示例

在运行基准测试时，我们以[SWE-Agent](https://swe-agent.com/)框架为基础构建了代理代码。在下面的日志中，我们将代理的文本输出、工具调用和工具响应呈现为THOUGHT、ACTION和OBSERVATION，尽管我们并未强制模型遵循固定的顺序。

以下代码块将展示Sonnet 3.5解决SWE-bench问题的典型过程。

在第一个代码块中，您可以看到提供给模型的部分初始提示，其中`{pr_description}`已填入SWE-bench任务的实际值。重要的是，此任务包含了重现问题的步骤，这将为模型提供宝贵的调查起点。

    <uploaded_files>
    /repo
    </uploaded_files>
    我已将Python代码仓库上传至/repo目录（不在/tmp/inputs中）。请考虑以下PR描述：

    <pr_description>
    linear_model.RidgeClassifierCV的参数store_cv_values问题
    #### 描述
    sklearn.linear_model.RidgeClassifierCV的参数store_cv_values错误

    #### 重现步骤/代码
    import numpy as np
    from sklearn import linear_model as lm

    #测试数据库
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size = n)

    rr = lm.RidgeClassifierCV(alphas = np.arange(0.1, 1000, 0.1), normalize = True,
                                             store_cv_values = True).fit(x, y)

    #### 预期结果
    期望获得常规的岭回归模型输出，并将交叉验证预测保留为属性。

#### 实际结果
TypeError: __init__() 收到了一个意外的关键字参数 'store_cv_values'

lm.RidgeClassifierCV 实际上并没有 store_cv_values 这个参数，尽管某些属性依赖于它。

模型响应并首先使用编辑工具查看仓库结构。你可以在 THOUGHT 和 ACTION 下看到模型的文本输出和工具调用参数，并在 OBSERVATION 下看到部分工具输出：

    THOUGHT:
    我将帮助你实施更改以满足 PR 描述的要求。让我们按照你概述的步骤进行。

    1. 首先，让我们探索仓库结构：
    ACTION (str_replace_editor):
    command:
    view

    path:
    /repo

    OBSERVATION:
    以下是 /repo 中最多 2 层深度的文件和目录（排除隐藏项）：
    /repo
    /repo/PULL_REQUEST_TEMPLATE.md
    /repo/ISSUE_TEMPLATE.md
    /repo/sklearn
    /repo/sklearn/decomposition
    /repo/sklearn/kernel_ridge.py
    /repo/sklearn/model_selection
    /repo/sklearn/covariance
    /repo/sklearn/cluster
    /repo/sklearn/base.py
    /repo/sklearn/dummy.py
    /repo/sklearn/naive_bayes.py
    ...

现在模型对仓库结构有了更好的了解，它使用编辑工具创建一个新脚本，用于复现问题并测试其修复方案：

    THOUGHT:
    根据仓库结构，我们需要修改 `sklearn/linear_model` 目录中的 Ridge 分类器。

    让我们创建一个脚本来复现错误：
    ACTION (str_replace_editor):
    command:
    create

    path:
    /repo/reproduce_error.py

    file_text:
    import numpy as np
    from sklearn import linear_model as lm

    # 测试数据集
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size = n)

    rr = lm.RidgeClassifierCV(alphas=np.arange(0.1, 1000, 0.1), normalize=True,
                             store_cv_values=True).fit(x, y)

    OBSERVATION:
    文件成功创建于：/repo/reproduce_error.py

然后模型使用 Bash 工具执行它编写的脚本，并成功复现了任务中的问题：

THOUGHT:
让我们验证是否能复现该错误：
ACTION (bash):
command:
python3 /repo/reproduce_error.py

OBSERVATION:
Traceback (most recent call last):
  File "/repo/reproduce_error.py", line 10, in <module>
    store_cv_values=True).fit(x, y)
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'

Copy

从此刻起，模型使用编辑工具修改仓库中的源代码，并重新运行脚本来验证修改是否解决了问题：

THOUGHT:
错误可复现。查看代码后，我发现问题在于：虽然`RidgeClassifierCV`类继承自`_BaseRidgeCV`，但其构造函数未能将`store_cv_values`参数传递给基类构造函数。

现在进行修复：
ACTION (str_replace_editor):
command:
str_replace

path:
/repo/sklearn/linear_model/ridge.py

old_str:
    def __init__(self, alphas=(0.1, 1.0, 10.0), fit_intercept=True,
                 normalize=False, scoring=None, cv=None, class_weight=None):
        super(RidgeClassifierCV, self).__init__(
            alphas=alphas, fit_intercept=fit_intercept, normalize=normalize,
            scoring=scoring, cv=cv)
        self.class_weight = class_weight

new_str:
    def __init__(self, alphas=(0.1, 1.0, 10.0), fit_intercept=True,
                 normalize=False, scoring=None, cv=None, class_weight=None,
                 store_cv_values=False):
        super(RidgeClassifierCV, self).__init__(
            alphas=alphas, fit_intercept=fit_intercept, normalize=normalize,
            scoring=scoring, cv=cv, store_cv_values=store_cv_values)
        self.class_weight = class_weight

Copy

在这个具体示例中，模型经过12个步骤后判定已准备就绪可以提交。随后任务测试成功运行，验证了模型的解决方案确实解决了问题。有些任务需要超过100轮交互后模型才提交解决方案；而在另一些任务中，模型会持续尝试直到上下文资源耗尽。

通过对比更新后的Claude 3.5 Sonnet与旧版模型的尝试，新版3.5 Sonnet展现出更频繁的自我修正行为。它还表现出尝试多种不同解决方案的能力，而非反复陷入相同错误。

## 挑战

SWE-bench Verified虽然是一个强大的评估工具，但其运行复杂度远超简单的单轮评估。以下是我们在使用过程中遇到的一些挑战——其他AI开发者同样可能面临这些问题。

  1. **耗时与高昂的令牌成本。** 上述示例来自一个仅用12步就成功完成的案例。然而，许多成功的运行需要模型耗费数百轮交互才能解决问题，且消耗超过10万个令牌。升级后的Claude 3.5 Sonnet具有顽强性：只要给予足够时间，它通常能找到解决问题的途径，但这可能带来高昂成本；
  2. **评分机制。** 在检查失败任务时，我们发现存在模型行为正确，但环境设置出现问题，或安装补丁被重复应用的情况。解决这些系统性问题对于准确评估AI智能体的性能至关重要。
  3. **隐藏测试。** 由于模型无法看到其正在接受的评分测试，它常常在任务实际失败时“认为”自己已成功。部分失败源于模型在错误的抽象层级解决问题（例如采用临时修补而非深度重构）。另一些失败则显得不太公平：模型解决了问题，但未能匹配原始任务的单元测试标准。
  4. **多模态能力。** 尽管升级后的Claude 3.5 Sonnet具备卓越的视觉与多模态能力，我们尚未实现让其查看文件系统保存文件或URL引用内容的功能。这使得调试特定任务（尤其是涉及Matplotlib的任务）异常困难，且容易引发模型幻觉。开发者在此方面显然存在可快速改进的空间——SWE-bench已推出专注于[多模态任务的新评估体系](https://www.swebench.com/multimodal.html)。我们期待开发者在近期能运用Claude在此评估中获得更高分数。

升级版Claude 3.5 Sonnet在SWE-bench Verified测试中取得49%的得分，以简单提示和两种通用工具超越了先前45%的最佳记录。我们确信，基于新版Claude 3.5 Sonnet进行开发的工程师们，将很快找到超越我们当前演示水平的、更高效的SWE-bench分数提升方案。

## 致谢

Erik Schluntz 优化了 SWE-bench 智能体并撰写了这篇博客文章。Simon Biggs、Dawn Drain 和 Eric Christiansen 协助实施了该基准测试。Shauna Kravec、Dawn Drain、Felipe Rosso、Nova DasSarma、Ven Chandrasekaran 以及许多其他贡献者共同训练 Claude 3.5 Sonnet，使其在代理式编码方面表现出色。
