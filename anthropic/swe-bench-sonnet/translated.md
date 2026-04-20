---
title: "使用Claude 3.5 Sonnet将SWE-bench Verified提升到新水平"
subtitle: "发布日期：2025年1月6日"
date: ""
source: "https://www.anthropic.com/engineering/swe-bench-sonnet"
---

我们最新的模型，升级版Claude 3.5 Sonnet，在软件工程评估SWE-bench Verified上达到了49%，超越了之前最先进的45%。这篇文章解释了我们围绕该模型构建的"智能体"，旨在帮助开发者从Claude 3.5 Sonnet获得最佳性能。

SWE-bench是一个AI评估基准，测试模型完成真实世界软件工程任务的能力。具体来说，它测试模型如何解决来自流行开源Python仓库的GitHub问题。对于基准中的每个任务，AI模型会获得一个设置好的Python环境和一个仓库的checkout（本地工作副本），时间点就在问题被解决之前。然后模型需要理解、修改和测试代码，然后提交其提议的解决方案。

每个解决方案根据关闭原始GitHub问题的pull request的真实单元测试进行评分。这测试了AI模型是否能够实现与PR原始人类作者相同的功能。

SWE-bench不仅仅是在隔离状态下评估AI模型，而是评估整个"智能体"系统。在这种情况下，"智能体"指的是AI模型与其周围的软件脚手的组合。这个脚手负责生成进入模型的提示、解析模型的输出以采取行动，以及管理交互循环——将模型先前行动的结果纳入其下一个提示。智能体在SWE-bench上的性能可能因这种脚手而显著不同，即使使用相同的底层AI模型。

还有许多其他用于大型语言模型编码能力的基准，但SWE-bench由于以下几个原因越来越受欢迎：

请注意，原始SWE-bench数据集包含一些任务，如果没有GitHub问题之外的额外上下文，这些任务是不可能解决的（例如，关于要返回的特定错误消息）。SWE-bench-Verified是SWE-bench的500个问题子集，已经过人工审查以确保它们是可解决的，因此提供了对编码智能体性能最清晰的衡量。这是我们在这篇文章中引用的基准。

达到最先进的性能

工具使用智能体

我们为更新版Claude 3.5 Sonnet创建智能体脚手的设计哲学是尽可能多地将控制权交给语言模型，并保持脚手 minimal。智能体有一个提示、一个用于执行bash命令的Bash Tool和一个用于查看和编辑文件和目录的Edit Tool。我们继续采样，直到模型决定它完成了，或者超过了其200k上下文长度。这个脚手允许模型使用自己的判断来追求问题，而不是被硬编码到特定模式或工作流程中。

提示概述了模型建议的方法，但它对于这个任务来说不是太长或太详细。模型可以自由选择如何从一步移动到另一步，而不是有严格和离散的转换。如果你不对token敏感，明确鼓励模型产生长的响应可能会有帮助。

以下代码显示了我们智能体脚手的提示：

<uploaded_files>
{location}
</uploaded_files>
I've uploaded a python code repository in the directory {location} (not in /tmp/inputs). Consider the following PR description:

<pr_description>
{pr_description}
</pr_description>

Can you help me implement the necessary changes to the repository so that the requirements specified in the <pr_description> are met?
I've already taken care of all changes to any of the test files described in the <pr_description>. This means you DON'T have to modify the testing logic or any of the tests in any way!

Your task is to make the minimal changes to non-tests files in the {location} directory to ensure the <pr_description> is satisfied.

Follow these steps to resolve the issue:
1. As a first step, it might be a good idea to explore the repo to familiarize yourself with its structure.
2. Create a script to reproduce the error and execute it with `python <filename.py>` using the BashTool, to confirm the error
3. Edit the sourcecode of the repo to resolve the issue
4. Rerun your reproduce script and confirm that the error is fixed!
5. Think about edgecases and make sure your fix handles them as well

Your thinking should be thorough and so it's fine if it's very long.

模型的第一个工具执行Bash命令。模式很简单，只需要在环境中运行的命令。然而，工具的描述带有更多权重。它为模型包含了更详细的指令，包括转义输入、无互联网访问以及如何在后台运行命令。

接下来，我们展示Bash Tool的规范：

{
   "name": "bash",
   "description": "Run commands in a bash shell\n
* When invoking this tool, the contents of the \"command\" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* State is persistent across command calls and discussions with the user.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Please avoid commands that may produce a very large amount of output.\n
* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.",
   "input_schema": {
       "type": "object",
       "properties": {
           "command": {
               "type": "string",
               "description": "The bash command to run."
           }
       },
       "required": ["command"]
   }
}

模型的第二个工具（Edit Tool）要复杂得多，包含模型查看、创建和编辑文件所需的一切。同样，我们的工具描述包含关于如何使用工具的详细信息。

我们在各种智能体任务中为这些工具的描述和规范付出了很多努力。我们对它们进行了测试，以发现模型可能误解规范或使用工具的可能陷阱，然后编辑描述以预先防止这些问题。我们认为，在设计工具接口方面应该投入更多的注意力，就像为人类设计工具接口投入大量注意力一样。

以下代码显示了我们Edit Tool的描述：

{
   "name": "str_replace_editor",
   "description": "Custom editing tool for viewing, creating and editing files\n
* State is persistent across command calls and discussions with the user\n
* If `path` is a file, `view` displays the result of applying `cat -n`. If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep\n
* The `create` command cannot be used if the specified `path` already exists as a file\n
* If a `command` generates a long output, it will be truncated and marked with `<response clipped>` \n
* The `undo_edit` command will revert the last edit made to the file at `path`\n
\nNotes for using the `str_replace` command:\n
* The `old_str` parameter should match EXACTLY one or more consecutive lines from the original file. Be mindful of whitespaces!\n
* If the `old_str` parameter is not unique in the file, the replacement will not be performed. Make sure to include enough context in `old_str` to make it unique\n
* The `new_str` parameter should contain the edited lines that should replace the `old_str`",
...

我们改进性能的一种方法是"错误防护"我们的工具。例如，有时候模型在智能体移出根目录后可能会搞砸相对文件路径。为了防止这种情况，我们简单地让工具始终需要绝对路径。

我们尝试了几种不同的策略来指定对现有文件的编辑，字符串替换的可靠性最高，模型指定要替换文件中的`old_str`为`new_str`。仅当正好有一个匹配时才会发生替换。如果匹配更多或更少，模型会看到适当的错误消息以重试。

我们Edit Tool的规范如下所示：

...
   "input_schema": {
       "type": "object",
       "properties": {
           "command": {
               "type": "string",
               "enum": ["view", "create", "str_replace", "insert", "undo_edit"],
               "description": "The commands to run. Allowed options are: `view`, `create`, `str_replace`, `insert`, `undo_edit`."
           },
           "file_text": {
               "description": "Required parameter of `create` command, with the content of the file to be created.",
               "type": "string"
           },
           "insert_line": {
               "description": "Required parameter of `insert` command. The `new_str` will be inserted AFTER the line `insert_line` of `path`.",
               "type": "integer"
           },
           "new_str": {
               "description": "Required parameter of `str_replace` command containing the new string. Required parameter of `insert` command containing the string to insert.",
               "type": "string"
           },
           "old_str": {
               "description": "Required parameter of `str_replace` command containing the string in `path` to replace.",
               "type": "string"
           },
           "path": {
               "description": "Absolute path to file or directory, e.g. `/repo/file.py` or `/repo`.",
               "type": "string"
           },
           "view_range": {
               "description": "Optional parameter of `view` command when `path` points to a file. If none is given, the full file is shown. If provided, the file will be shown in the indicated line number range, e.g. [11, 12] will show lines 11 and 12. Indexing at 1 to start. Setting `[start_line, -1]` shows all lines from `start_line` to the end of the file.",
               "items": {
                   "type": "integer"
               },
               "type": "array"
           }
       },
       "required": ["command", "path"]
   }
}

...

结果

总的来说，升级版Claude 3.5 Sonnet展示了比我们之前的模型和之前最先进的模型更高的推理、编码和数学能力。它还展示了改进的智能体能力：工具和脚手帮助将这些改进的能力发挥到最佳使用。

智能体行为示例

对于运行基准测试，我们使用SWE-Agent框架作为智能体代码的基础。在下面的日志中，我们将智能体的文本输出、工具调用和工具响应呈现为THOUGHT、ACTION和OBSERVATION，尽管我们不将模型约束为固定顺序。

下面的代码块将逐步介绍Sonnet 3.5解决SWE-bench问题的典型案例。

在第一个块中，您可以看到给予模型的初始提示的一部分，其中{pr_description}填充了来自SWE-bench任务的真实值。重要的是，这个任务包含重现问题的步骤，这将为模型提供调查的宝贵起点。

<uploaded_files>
/repo
</uploaded_files>
I've uploaded a python code repository in the directory /repo (not in /tmp/inputs). Consider the following PR description:

<pr_description>
linear_model.RidgeClassifierCV's Parameter store_cv_values issue
#### Description
Parameter store_cv_values error on sklearn.linear_model.RidgeClassifierCV

#### Steps/Code to Reproduce
import numpy as np
from sklearn import linear_model as lm

#test database
n = 100
x = np.random.randn(n, 30)
y = np.random.normal(size = n)

rr = lm.RidgeClassifierCV(alphas = np.arange(0.1, 1000, 0.1), normalize = True, 
                                         store_cv_values = True).fit(x, y)

#### Expected Results
Expected to get the usual ridge regression model output, keeping the cross validation predictions as attribute.

#### Actual Results
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'

lm.RidgeClassifierCV actually has no parameter store_cv_values, even though some attributes depends on it.

</pr_description>

模型响应并首先使用Edit Tool查看仓库结构。您可以在THOUGHT和ACTION下看到模型的文本输出和工具调用参数，在OBSERVATION下看到工具的部分输出：

THOUGHT:
I'll help you implement the changes to satisfy the PR description. Let's follow the steps you outlined.

1. First, let's explore the repo structure:
ACTION (str_replace_editor):
command:
view

path:
/repo

OBSERVATION:
Here's the files and directories up to 2 levels deep in /repo, excluding hidden items:
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

现在模型对仓库结构有了更好的理解，它使用Edit Tool创建一个新脚本，用于重现问题并测试其修复：

THOUGHT:
Based on the repository structure, we'll need to modify the Ridge Classifier in the `sklearn/linear_model` directory.

Let's create a script to reproduce the error:
ACTION (str_replace_editor):
command:
create

path:
/repo/reproduce_error.py

file_text:
import numpy as np
from sklearn import linear_model as lm

#test database
n = 100
x = np.random.randn(n, 30)
y = np.random.normal(size = n)

rr = lm.RidgeClassifierCV(alphas=np.arange(0.1, 1000, 0.1), normalize=True, 
                         store_cv_values=True).fit(x, y)

OBSERVATION:
File created successfully at: /repo/reproduce_error.py

然后模型使用Bash Tool执行它编写的脚本，并成功重现了任务中的问题：

THOUGHT:
Let's verify that we can reproduce the error:
ACTION (bash):
command:
python3 /repo/reproduce_error.py

OBSERVATION:
Traceback (most recent call last):
  File "/repo/reproduce_error.py", line 10, in <module>
    store_cv_values=True).fit(x, y)
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'

从这里开始，模型使用Edit Tool更改仓库中的源代码，并重新运行其脚本以验证更改是否解决了问题：

THOUGHT:
The error is reproducible. Looking at the code, I can see that the issue is that while the `RidgeClassifierCV` class inherits from `_BaseRidgeCV`, it fails to pass the `store_cv_values` parameter from its constructor through to the base class constructor.

Let's fix this:
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

在这个特定示例中，模型工作了12步才决定准备好提交。然后任务的测试成功运行，验证了模型的解决方案解决了问题。有些任务需要模型超过100轮才提交其解决方案；在其他任务中，模型不断尝试直到用完上下文。

从更新版Claude 3.5 Sonnet与旧模型的尝试对比来看，更新版3.5 Sonnet更经常自我纠正。它还展示了尝试几种不同解决方案的能力，而不是反复犯同样的错误。

挑战

SWE-bench Verified是一个强大的评估，但运行起来也比简单的单轮评估更复杂。这些是我们使用它面临的一些挑战——其他AI开发者可能也会遇到。

升级版Claude 3.5 Sonnet在SWE-bench Verified上达到了49%，超越了之前最先进的（45%），使用简单的提示和两个通用工具。我们相信，使用新版Claude 3.5 Sonnet构建的开发者将很快找到新的、更好的方法来改进我们最初在这里展示的SWE-bench分数。

致谢

Erik Schluntz优化了SWE-bench智能体并撰写了这篇博客文章。Simon Biggs、Dawn Drain和Eric Christiansen帮助实现了基准测试。Shauna Kravec、Dawn Drain、Felipe Rosso、Nova DasSarma、Ven Chandrasekaran以及许多其他人为训练Claude 3.5 Sonnet出色的智能体编码能力做出了贡献。
