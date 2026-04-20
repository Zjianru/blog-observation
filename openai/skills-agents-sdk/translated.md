使用技能加速开源软件维护

Using skills and GitHub Actions to optimize Codex workflows in the OpenAI Agents SDK repos.

作者：Kazuhiro Sera

我们使用 Codex 改变了维护 OpenAI Agents SDK 仓库的方式。仓库本地技能、AGENTS.md 和 GitHub Actions 让我们将验证、发布准备、示例集成测试和 PR 审查等重复性工程工作转变为可重复的工作流程。即使使用相当简单的设置，这也帮助我们提高了这些活跃仓库的开发吞吐量。在 2025 年 12 月 1 日至 2026 年 2 月 28 日期间，两个仓库合并了 457 个 PR，而此前三个月（2025 年 9 月 1 日至 2025 年 11 月 30 日）为 316 个（Python：182 -> 226，TypeScript：134 -> 231）。

快速背景：该 SDK 提供 Python 和 TypeScript 两种版本。它提供了构建代理应用程序的核心组件，也是基于 Realtime API 构建语音代理的一种简洁方式，支持多种代理、工具和人在回路控制。它的使用规模很大：截至 2026 年 3 月 6 日的最近 30 天窗口中，Python 包在 PyPI 上约有 1470 万次下载，TypeScript 包在 npm 上约有 150 万次下载。

设置很简单：

AGENTS.md 中的仓库策略
.agents/skills/ 中的仓库本地技能
这些技能内部的可选脚本和引用
当相同的工作流程应该在 CI 中运行时，使用 Codex GitHub Action

这种设置为 Codex 提供了关于仓库如何工作的稳定上下文，这提高了重复性工程工作的速度和准确性。

如果您维护公共开源项目，请参阅 Codex for OSS。符合条件的维护者可以申请 ChatGPT Pro 与 Codex、API 积分和有条件的 Codex Security 访问权限。

将工作流程保存在仓库中

在这些仓库中，我们使用技能来捕获特定于仓库的工作流程。技能是一个小的操作知识包：一个 SKILL.md 清单，加上可选的 scripts/、references/ 和 assets/。Codex 定制文档描述了为什么这种方法效果很好：技能非常适合可重复的工作流程，因为它们可以携带更丰富的指令、脚本和引用，而不会在一开始就膨胀代理的上下文。

这与技能使用的渐进式披露模型相匹配：

它首先看到元数据，如 name 和 description
仅当选择技能时才加载 SKILL.md
仅在需要时才读取引用或运行脚本

两个 SDK 仓库都将这些工作流程保持在靠近代码的位置：

openai-agents-python 中的 .agents/skills
openai-agents-js 中的 .agents/skills

Python 仓库是更简单的基准：

code-change-verification 在代码或构建行为更改时运行所需的格式化、lint、类型检查和测试堆栈。
docs-sync 审计文档与代码库的对比，发现缺失、不正确或过时的文档。
examples-auto-run 以自动模式运行示例，带有日志和重新运行助手。
final-release-review 将上一个发布标签与当前候选发布进行比较，并检查发布准备情况。
implementation-strategy 在编辑运行时或 API 更改之前决定兼容性边界和实现方法。
openai-knowledge 通过官方 Docs MCP 工作流程获取当前的 OpenAI API 和平台文档。
pr-draft-summary 在交接时准备分支名称建议、PR 标题和草稿描述。
test-coverage-improver 运行覆盖率，发现最大的差距，并提出高影响力的测试。

JavaScript 仓库遵循相同的一般模式，然后为 npm monorepo 和发布流程添加了一些特定于仓库的技能：

changeset-validation 检查 changesets 和 bump level 是否与包 diff 实际匹配。
integration-tests 将包发布到本地 Verdaccio 注册表，并跨支持的运行时验证安装和运行行为。
pnpm-upgrade 以协调方式更新 pnpm 工具链和 CI pins。

比确切列表更重要的是模式。每个技能都有狭窄的合约、明确的触发器和具体的输出。

一些最有用的技能不是硬性关卡。docs-sync 和 test-coverage-improver 是报告优先的工作流程：它们检查当前 diff 或覆盖率工件，优先处理重要事项，然后在进行编辑之前请求批准。在 Python 仓库中，docs-sync 还将源代码文档字符串和注释作为生成参考文档的真实来源，而不是手动修补生成的输出。JavaScript 专用的 pnpm-upgrade 技能是狭窄维护工作流程的另一个很好的例子：它一起更新本地 pnpm 版本、packageManager 和工作流 pins，而不是求助于广泛的搜索和替换。

使工作流程成为强制性

当仓库在正确的时间要求技能时，它们会更有用。这就是 AGENTS.md 的用武之地。

AGENTS.md 指南将这些文件描述为与代码库一起旅行的仓库级指令，并在代理开始工作之前应用。它还建议保持小文件。在 Agents SDK 仓库中，我们使用该空间来记录 Codex 每次应该遵循的规则，我们将最高价值的规则放在最顶部。

实际上，两个仓库都使用简短的 if/then 规则来进行强制性技能使用。在编辑可能影响兼容性边界的运行时或 API 更改之前，调用 $implementation-strategy 来决定兼容性边界和实现方法。如果更改影响 SDK 代码、测试、示例或构建行为，调用 $code-change-verification。如果 JavaScript 包更改影响发布元数据，调用 $changeset-validation。如果工作涉及 OpenAI API 或平台集成，调用 $openai-knowledge。当工作完成并准备好交接时，调用 $pr-draft-summary。

该结构也与 agents.md 建议一致：将项目概述、构建和测试命令、代码风格、测试指导、安全注意事项和其他特定于仓库的规则放在一个地方。Agents SDK 仓库遵循该形状，但它们以日常工作中最重要的操作触发器为首。一个紧凑版本如下所示：

# AGENTS.md

![](images/skills-agents-sdk_00.png)

## 项目概述

- 核心 SDK 代码位于 `src/agents/` 或 `packages/*/src/`。
- 测试位于 `tests/` 或 `packages/*/test/`。
- 示例应用和集成表面位于 `examples/`。

## 强制性技能使用

- 在编辑可能影响兼容性边界的运行时或 API 更改之前，使用 `$implementation-strategy`。
- 当运行时代码、测试、示例或构建/测试行为发生更改时，运行 `$code-change-verification`。
- 对于 OpenAI API 或平台工作，使用 `$openai-knowledge`。
- 当实质代码工作准备好审查时，使用 `$pr-draft-summary`。

## 构建和测试命令

- Python: `make format`, `make lint`, `make typecheck`, `make tests`
- TypeScript: `pnpm i`, `pnpm build`, `pnpm -r build-check`, `pnpm lint`, `pnpm test`

## 兼容性规则

- 保留公共构造函数和 dataclass 字段的位置兼容性。

真实文件然后在该基准上添加特定于仓库的详细信息，例如 JavaScript 仓库中的 $changeset-validation，以及两个文件中更详细的运行时、文档和发布指导。如果您想要完整的示例，请参阅 openai-agents-python 中的 AGENTS.md 和 openai-agents-js 中的 AGENTS.md。

AGENTS.md 不仅用于技能触发。Python 仓库还在那里记录了一个公共 API 兼容性规则：保留导出构造函数参数和 dataclass 字段的位置含义，尽可能在末尾附加新的可选参数，如果重新排序是不可避免的，则添加兼容性测试。这是另一个好模式：将发布关键兼容性规则与技能触发器放在同一个地方。

验证规则

一个清晰的例子是 $code-change-verification。

在这两个仓库中，规则不是"始终运行长验证堆栈"。规则是"当运行时代码、测试、示例或构建/测试行为发生更改时运行它，并且在通过之前不要将工作标记为完成"。

条件部分保持仅文档的工作轻量。强制性部分确保 SDK 代码更改通过仓库的标准验证步骤。

实际的验证堆栈编码在技能本身中。

在 Python 仓库中，它要求：

make format
make lint
make typecheck
make tests

在 JavaScript 仓库中，技能要求此确切顺序：

pnpm i
pnpm build
pnpm -r build-check
pnpm -r -F "@openai/*" dist:check
pnpm lint
pnpm test

技能编码了仓库对"已验证"的定义，AGENTS.md 使该定义可强制执行。

Changeset 验证

JavaScript 仓库对包更改还有一个额外的强制性步骤：$changeset-validation，围绕 Changesets 构建。

当 packages/ 下的任何内容发生变化，或者 .changeset/ 发生变化时，模型不仅仅需要运行测试。它必须创建或更新正确的 changeset，验证 bump level，并确认 changeset 实际上与 diff 匹配。

这个技能不仅仅是检查文件是否存在。它要求 Codex 判断 git diff，并将验证规则保存在共享提示中，以便本地运行和 GitHub Actions 使用相同的逻辑。它还对特定于仓库的策略进行编码，例如：

当已存在一个 changeset 时，使用现有的分支 changeset 而不是创建另一个
将摘要保持在一行，采用 Conventional Commit 样式，以便它可以兼作提交标题
在 1.0 之前，对于正常的功能工作避免重大版本提升，对于明确标记为仅预览的附加内容，如果它们不更改现有行为，则将其视为补丁更改
根据实际包更改验证必需的 bump level

这使得 Codex 在说工作完成之前负责验证它创建的发布元数据。

使用当前文档

两个仓库在工作涉及 OpenAI API 或平台集成时也要求使用 $openai-knowledge。

该技能是官方 OpenAI Docs MCP 的一个简单包装器。它不让模型根据记忆回答，而是告诉 Codex 使用 OpenAI 开发者文档 MCP 服务器来查找 Responses API、工具、流式传输、Realtime 和 MCP 等表面的当前文档。
如果本地 Codex 环境中尚未配置 MCP 服务器，该技能会指向维护者的 Docs MCP 快速入门和官方 MCP 服务器端点。

准备 PR 交接

在实质性工作结束时，两个仓库都使用 $pr-draft-summary。

该技能仅在任务实际完成或准备好审查且更改涉及有意义的代码、测试、有行为影响的文档或构建/测试配置时触发。然后它自动收集分支名称、工作树状态、更改的文件、diff 统计信息和最近提交，并生成：

分支名称建议
PR 标题
草稿 PR 描述

输出格式故意严格要求。一个典型结果如下所示：

# Pull Request Draft

## Branch name suggestion

git checkout -b fix/tracing-lazy-init-fork-safety

## Title

fix: #2489 lazily initialize tracing globals to avoid import-time fork hazards

## Description

This pull request fixes import-time tracing side effects that could break fork-based process models by moving tracing bootstrap to lazy, first-use initialization.

It updates tracing setup so initialization happens once on first access while preserving the existing public tracing APIs.

It also adds regression tests for import-time behavior, one-time bootstrap, and custom provider handling.

This pull request resolves #2489.

一旦你相信模型来验证和总结它自己的工作，要求它生成 PR 草稿作为最后一个自然步骤。它保持交接的一致性，并在编码工作完成后减少重复性写作。

写更好的描述

技能 SKILL.md 前置matter中的 description 字段是路由合约的一部分。

这是结构性的，不是风格性的。代理技能规范将 name 和 description 作为必需的 SKILL.md 前置matter字段，其渐进式披露模型说这些字段在启动时为所有技能加载。完整的 SKILL.md 正文和任何 scripts/、references/ 或 assets/ 仅在技能实际激活后才加载。

Codex 技能文档和定制文档从 Codex 角度描述了相同的行为：Codex 从每个技能的元数据开始发现，仅在选择技能时加载 SKILL.md，并且在需要时读取引用或运行脚本。OpenAI API  cookbook 中的技能描述了托管 shell 端同样明确：OpenAI 首先读取每个技能的名称、描述和路径，模型使用该信息来决定何时读取完整的 SKILL.md。其 SKILL.md 前置matter部分更直接地提出相同观点：name 和 description 对于发现和路由很重要。

在 Agents SDK 仓库中，这使得 description 成为 Codex 读取技能其余部分之前的主要路由信号之一。

这里有一个来自 code-change-verification 的具体例子。

太模糊：

description: 在 OpenAI Agents JS monorepo 中运行强制性验证堆栈。

更好（实际的描述）：

description: 当更改影响 OpenAI Agents JS monorepo 中的运行时代码、测试或构建/测试行为时，运行强制性验证堆栈。

较短版本已经告诉 Codex 该技能做什么，但仍没有说明该技能何时适用，什么类型的更改应该触发它，或者检查是否是可选的。更具体的版本告诉模型所有三个。

同样的模式出现在 pr-draft-summary 中。

太模糊：

description: 为拉取请求创建 PR 标题和草稿描述。

更好（实际的描述）：

description: 在实质性代码更改完成后创建 PR 标题和草稿描述。当结束中等或更大的更改（运行时代码、测试、构建配置、有行为影响的文档）并且需要 PR 就绪的摘要块以及更改摘要和 PR 草稿文本时触发。

再次强调，真正的描述是路由元数据。它告诉 Codex：

这是一个任务结束技能
它用于实质性更改，而不是每个聊天轮次
输出是一个 PR 就绪的块，而不仅仅是散文摘要

从这些仓库中学到的实际教训是花时间在描述上。如果路由感觉不可靠，在你添加更多代码之前修复元数据。

将机制放在脚本中

在那之后，下一个问题是什么属于模型，什么应该推入脚本。

可靠的拆分是：

解释、比较和报告留在模型中
确定性、重复性的 shell 工作进入 scripts/

这与公开指导一致。Codex 定制文档将技能描述为一种方式，为可重复的工作流程给 Codex 更丰富的指令、脚本和引用，而不会在一开始就膨胀上下文。这符合模型优先的设置：让 Codex 处理工作中依赖上下文的部分，仅在需要时引入脚本处理确定性部分。OpenAI API cookbook 中的技能也建议将技能脚本设计为小型 CLI：可从命令行运行的脚本，打印确定性 stdout，在使用或错误消息时大声失败，并在需要时将输出写入已知文件路径。

在 Agents SDK 仓库中，我们尝试在智能真正有用的地方使用模型，例如：

阅读源代码以推断预期行为
将日志与该预期行为进行比较
决定发布 diff 是否包含真正的兼容性风险
产生维护者可以采取行动的解释

脚本然后处理围绕该工作的机制，例如：

按固定顺序运行仓库的必需验证命令
启动示例运行，收集每个示例的日志，并为失败写入重新运行文件
在发布准备情况审查之前获取上一个发布标签
暴露辅助命令如 start、stop、status、logs、tail、collect 和 rerun，以便相同的工作流程易于重复运行

如果模型每次都必须重新发现相同的 shell 配方，这通常是该配方应该成为脚本的信号。如果任务依赖上下文、权衡或解释，那部分应该留在模型中。

自动化集成测试

这两个仓库中最有用的工作流程领域之一是自动化集成测试。这里有两个相关层：在两个仓库中自动验证仓库内示例，以及在 JavaScript 仓库中单独验证已发布的包在用户消费方式安装时仍然有效。

在此设置之前，验证示例部分是手动的。你可以运行示例，但最后一公里通常取决于目视检查日志或通过检查决定输出是否看起来正确。这对于一个示例来说是可控的。它在不断增长的 SDK 仓库中不能很好地扩展。

第一层是 examples-auto-run，但技能出现在运行器之后。为了在任何程度上自动化示例验证，我们首先必须为这两个仓库中的非交互式示例执行构建底层支持。这意味着使在自动模式下运行示例脚本成为可能，包括通常涉及提示或批准的示例。

该基础工作包括：

自动回答常见交互式提示
在运行器支持的地方自动批准 HITL、MCP、apply_patch 和 shell 操作
将仍然不适合自动化的示例保持在自动跳过列表上，例如需要额外运行时设置的 realtime 或 Next.js 应用示例
为每个示例运行写入结构化日志
生成重新运行文件，以便失败可以重试而无需重新运行所有内容

一旦该基础到位，我们将其组织为一个技能，以便工作流程变得可重用且易于调用。在 Python 仓库中，examples-auto-run 包装 uv run examples/run_examples.py --auto-mode --write-rerun --main-log ... --logs-dir ....在 JavaScript 仓库中，它包装构建检查，然后以自动模式运行 pnpm examples:start-all，带有每个示例的日志和重新运行支持。

为了提高验证质量，运行器的工作是执行示例并将其 stdout 和 stderr 保存在每个示例的日志中。然后技能让 Codex 逐一查看这些日志并与源代码进行比较：

阅读示例源代码和注释
推断预期的流程
打开匹配的日志
将预期行为与实际的 stdout 和 stderr 进行比较
对每个成功的示例都这样做，而不仅仅是一个样本

这比尝试将正确性编码为固定脚本级断言更准确和灵活。成功的退出代码很有用，但对于与真实 API 对话、使用工具或产生结构化输出的示例来说，这还不够。通过首先记录实际输出，然后根据源代码仔细检查它，我们可以根据每个示例的真正意图对其进行验证。

在 JavaScript 仓库中，有第二层：单独的 integration-tests 技能。该工作流程超出了在原地运行源代码示例的范围。它将包发布到本地 Verdaccio 注册表，并测试在多个环境中安装和运行它们，包括 Node.js、Bun、Deno、Cloudflare Workers 和 Vite React 应用。这捕获了不同类别的问题：不是"示例在仓库中运行吗？"而是"包在发布、安装和运行时集成后是否仍然表现正确？"

总的来说，这些工作流程说明了为什么将技能、脚本和模型判断结合起来是有用的。脚本使运行可重复，捕获证据，并覆盖手动检查很乏味的安装路径。然后 Codex 使用该证据进行比简单脚本通过/失败检查更仔细的比较。

添加发布检查

发布准备是这种模式有帮助的另一个领域。

两个仓库中的 release-review 工作流程首先找到上一个发布标签，将其与最新 main 进行 diff，然后要求 Codex 检查该 diff 以查找：

公共 API 和面向用户的 SDK 行为中的向后兼容性问题
回归，包括预期行为中的较小更改
缺少需要它们的更改的迁移说明或发布说明更新

基于这些发现，技能做出总体发布准备情况判断。

一个具体例子是 openai/openai-agents-python#2480，发布审查总体保持绿色，同时仍然指出 Python 3.9 放弃及其需要的后续发布说明：

发布准备情况审查（摘录）

发布判断：
🟢 绿灯可以发货。 minor 版本提升包括预期的重大更改
（Python 3.9 放弃），未发现具体回归。

范围摘要：

- 38 个文件更改（+1450/-789）；关键领域：`src/agents/tool.py`、
  `src/agents/extensions/`、`src/agents/realtime/`、`tests/`、
  `pyproject.toml`、`uv.lock`。

Python 3.9 支持被移除

- 风险：🟡 中等。绑定到 Python 3.9 的用户将无法安装
  0.9.0 版本。
- 证据：`pyproject.toml` 现在设置 `requires-python = ">=3.10"` 并删除
  Python 3.9 分类器；CI 跳过了 3.9 的逻辑被移除。
- 行动：确保发布说明明确指出 Python 3.9 放弃，并且
  打包元数据保持 `>=3.10`。

该技能还定义了门决策是如何做出的。审查从"可以安全发布"开始，仅当 diff 显示真实问题的具体证据时才切换到阻止调用。每个阻止调用都必须带有具体的取消阻止清单。这使得输出更容易使用：绿色结果意味着在 diff 中未发现发布阻塞问题，阻止结果意味着存在带有明确后续步骤的真实问题。

这比通用的"请审查发布"更有用。它强制模型对具体 diff 进行推理，并以操作术语解释结果。如果发布是安全的，就说。如果不是，指着确切的证据和确切的后续步骤。

在 CI 中运行工作流程

一旦技能在本地有用，Codex GitHub Action 就可以轻松地在 CI 中自动执行相同的工作流程。当本地工作流程已经稳定时，效果最好，因为手动使用是调试指令、完善脚本和发现真正边缘情况的地方。

对于公共仓库，触发器设计和工作流程本身一样重要。GitHub Action 安全清单建议限制谁可以启动工作流程，偏好可信的事件或明确批准，从 PR、提交、issue 或评论中清理提示输入，使用 drop-sudo 或无特权用户保护 OPENAI_API_KEY，并将 Codex 作为作业中的最后一步运行。

如果工作流程具有写能力并接受不可信的公共输入，风险通常在触发器设计、输入处理和围绕技能的运行时权限中。

在 PR 审查中使用 Codex

技能是这些仓库生产力故事的一部分。Codex GitHub PR 自动审查是另一部分。

自从 Codex GitHub PR 自动审查可用以来，Codex 已成为这些仓库大多数代码更改的有用审查者。我们将其作为审查的常规部分使用，而不是作为特殊案例工具。

对于 straightforward 程序 bug、回归和缺失测试，依靠 Codex 作为必需的审查路径现在在实践中已经足够安全。它在一遍又一遍地检查相同的正确性模式方面是一致的，并且对于小修复和常规改进来说，它消除了一项重大瓶颈。

同行审查仍然很重要，但用于不同类别的更改。

当主要问题不是"这段代码正确吗？"而是"我们应该在多个有效选项中选择哪一个，我们应该如何发货？"时，人工审查仍然是必不可少的。这包括：

有多种合理设计的 API 或架构更改，维护者需要做出明确选择
影响产品期望、向后兼容性承诺或推广策略的行为更改
命名、迁移和发布沟通决策，其中最困难的部分是为用户和贡献者选择最清楚的内容
需要维护者或团队之间对齐的更改，例如范围工作、排序或决定现在应该发货什么 versus 以后

Codex 仍然可以在所有这些情况下做出有用的贡献，但它们仍然受益于人工决策者和直接讨论。

AGENTS.md 也可以对该拆分进行编码：仓库可以告诉 Codex 什么对于正确性审查很重要，Codex 可以一致地应用该指导。

这也是吞吐量提升的重要贡献者。重复性的审查和验证工作不再为每个低风险更改等待稀缺的审查者时间，而维护者可以保持在更高上下文的审查上，他们的判断最重要。这种转变帮助我们更快地处理积压 bug 和较小的功能改进。

最后想法

在 OpenAI Agents SDK 仓库中，技能在作为仓库正常工作设置的一部分时效果最好。

AGENTS.md 告诉 Codex 哪些工作流程是必需的。description 告诉它何时路由到那些工作流程。scripts/ 处理确定性部分。模型处理上下文相关部分。一旦工作流程在本地稳定，Codex GitHub Action 可以将相同的过程带入 CI。

这使得这些仓库的日常工程工作更加明确和可靠。它也使得更快地交付小改进变得更加容易，因为验证、发布审查和 PR 交接现在遵循相同的可重复过程。

资源
OpenAI Agents SDK for Python
OpenAI Agents SDK for JS
Codex 中的技能
使用 AGENTS.md 进行自定义指令
Codex GitHub Action
在 GitHub 中使用 Codex
OpenAI API cookbook 中的技能
代理技能规范
OpenAI API 中的技能：操作最佳实践
