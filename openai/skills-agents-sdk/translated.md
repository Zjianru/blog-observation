# 运用技能加速开源软件维护

来源：https://developers.openai.com/blog/skills-agents-sdk

---

我们运用Codex改变了维护[OpenAI智能体SDK](/api/docs/guides/agents)代码库的方式。通过仓库本地技能、`AGENTS.md`文档和GitHub Actions，我们将重复性工程任务——例如验证、发布准备、示例集成测试和PR审查——转化为可复用的工作流。即使采用相当简单的配置，这种方法也显著提升了这些活跃代码库的开发吞吐量。在2025年12月1日至2026年2月28日期间，两个代码库共合并了457个PR，较前三个月（2025年9月1日至11月30日）的316个大幅增长（Python版：182→226，TypeScript版：134→231）。

快速背景介绍：该SDK提供[Python](https://github.com/openai/openai-agents-python)和[TypeScript](https://github.com/openai/openai-agents-js)两种版本。它不仅为构建智能体应用提供核心组件，还能基于[实时API](/api/docs/guides/realtime)简洁地构建支持多智能体、工具和人机交互控制的语音智能体。该SDK已被大规模采用：截至2026年3月6日的最近30天内，Python包在PyPI上的下载量约达1470万次，TypeScript包在npm上的下载量约达150万次。

配置方案简明扼要：

  * 仓库策略定义于[`AGENTS.md`](https://agents.md/)
  * 仓库本地技能存放于`.agents/skills/`目录
  * 技能文件夹内可选的脚本与参考文件
  * 需在CI中运行相同工作流时启用[Codex GitHub Action](/codex/github-action)

该配置为Codex提供了稳定的仓库运作上下文，从而提升了重复性工程工作的速度与准确性。

如果您正在维护公开的开源项目，请参阅[面向开源项目的Codex](/community/codex-for-oss)。符合条件的维护者可申请包含Codex的ChatGPT Pro、API额度以及有条件访问Codex安全功能的权限。

## 将工作流保留在代码库中

在这些代码库中，我们使用技能来捕获特定于仓库的工作流。技能是一小包操作知识：一个 `SKILL.md` 清单文件，加上可选的 `scripts/`、`references/` 和 `assets/` 目录。[Codex 定制文档](/codex/concepts/customization#skills)解释了为何这种方式效果良好：技能非常适合可重复的工作流，因为它们能够携带更丰富的指令、脚本和参考资料，而不会一开始就使智能体的上下文变得臃肿。

这与技能所采用的渐进式披露模式相匹配：

  * 首先看到 `name` 和 `description` 等元数据
  * 仅在技能被选中时加载 `SKILL.md`
  * 仅在需要时读取参考资料或运行脚本

两个 SDK 仓库都将这些工作流紧密地保持在代码附近：

  * [openai-agents-python 中的 .agents/skills](https://github.com/openai/openai-agents-python/tree/main/.agents/skills)
  * [openai-agents-js 中的 .agents/skills](https://github.com/openai/openai-agents-js/tree/main/.agents/skills)

Python 仓库是较简单的基准：

  * `code-change-verification` 在代码或构建行为变更时运行所需的格式化、代码检查、类型检查和测试堆栈。
  * `docs-sync` 根据代码库审核文档，并查找缺失、错误或过时的文档。
  * `examples-auto-run` 以自动模式运行示例，附带日志和重新运行辅助工具。
  * `final-release-review` 比较上一个发布标签与当前发布候选版本，并检查发布就绪状态。
  * `implementation-strategy` 在编辑运行时或 API 变更之前，决定兼容性边界和实施方法。
  * `openai-knowledge` 通过官方的 Docs MCP 工作流拉取最新的 OpenAI API 和平台文档。
  * `pr-draft-summary` 在交接时准备分支名称建议、PR 标题和草稿描述。
  * `test-coverage-improver` 运行覆盖率检查，找出最大的差距，并提出高影响力的测试。

JavaScript 仓库遵循相同的一般模式，然后为其 npm 单体仓库和发布流程添加了一些特定于仓库的技能：

* `changeset-validation` 会检查变更集与版本升级级别是否与包的实际变更相匹配。
* `integration-tests` 将包发布到本地 Verdaccio 注册表，并验证其在所有支持的运行时环境中的安装和运行行为。
* `pnpm-upgrade` 以协调的方式更新 pnpm 工具链和 CI 中的固定版本。

比具体清单更重要的是其模式。每项技能都有明确的约定、清晰的触发条件和具体的输出结果。

一些最有用的技能并非硬性关卡。`docs-sync` 和 `test-coverage-improver` 属于报告优先的工作流：它们会检查当前的变更差异或覆盖率工件，优先处理重要事项，并在进行编辑前请求批准。在 Python 代码库中，`docs-sync` 还将源代码文档字符串和注释视为生成参考文档的权威来源，而不是手动修补生成的输出。仅适用于 JavaScript 的 `pnpm-upgrade` 技能是另一个典型的狭义维护工作流示例：它会同时更新本地 pnpm 版本、`packageManager` 和工作流中的固定版本，而不是退而求其次采用宽泛的搜索替换方式。

## 使工作流成为强制要求

当代码库在适当时机要求执行这些技能时，它们会变得更加有用。这正是 `AGENTS.md` 的作用所在。

[AGENTS.md 指南](/codex/guides/agents-md#layer-project-instructions) 将这些文件描述为代码库级别的指令，它们随代码库一起传递，并在代理开始工作前生效。该指南还建议保持这些文件的简洁性。在 Agents SDK 代码库中，我们利用这一空间来规定 Codex 每次都应遵循的规则，并将价值最高的规则置于文件顶部。

实际上，两个代码库都使用简短的条件/结果规则来强制要求技能的使用。在编辑运行时或 API 变更之前，先调用 `$implementation-strategy` 来确定兼容性边界和实施方法。如果变更影响 SDK 代码、测试、示例或构建行为，则调用 `$code-change-verification`。如果 JavaScript 包的变更影响发布元数据，则调用 `$changeset-validation`。如果工作涉及 OpenAI API 或平台集成，则调用 `$openai-knowledge`。当工作完成并准备移交时，调用 `$pr-draft-summary`。

该结构也符合[agents.md](https://agents.md/)的推荐方案：将项目概述、构建与测试命令、代码风格、测试指南、安全考量及其他仓库特定规则集中管理。Agents SDK 仓库遵循这一形态，但它们在日常工作中优先突出最关键的操作触发器。其精简版本如下所示：

    # AGENTS.md

    ## 项目概述

    - 核心 SDK 代码位于 `src/agents/` 或 `packages/*/src/` 目录下。
    - 测试代码位于 `tests/` 或 `packages/*/test/` 目录下。
    - 示例应用与集成接口位于 `examples/` 目录下。

    ## 强制技能使用规范

    - 修改可能影响兼容性边界的运行时或 API 变更前，必须使用 `$implementation-strategy`。
    - 当运行时代码、测试、示例或构建/测试行为发生变更时，必须运行 `$code-change-verification`。
    - 涉及 OpenAI API 或平台开发时，必须使用 `$openai-knowledge`。
    - 重大代码工作准备接受评审时，必须使用 `$pr-draft-summary`。

    ## 构建与测试命令

    - Python：`make format`, `make lint`, `make typecheck`, `make tests`
    - TypeScript：`pnpm i`, `pnpm build`, `pnpm -r build-check`, `pnpm lint`, `pnpm test`

    ## 兼容性规则

    - 公共构造函数与数据类字段必须保持参数位置兼容性。

实际文件会在此基础框架上补充仓库特定细节，例如 JavaScript 仓库中的 `$changeset-validation`，以及两个文件中更详尽的运行时、文档和发布指南。如需查看完整示例，请参阅 [openai-agents-python 的 AGENTS.md](https://github.com/openai/openai-agents-python/blob/main/AGENTS.md) 和 [openai-agents-js 的 AGENTS.md](https://github.com/openai/openai-agents-js/blob/main/AGENTS.md)。

`AGENTS.md` 不仅用于技能触发器。Python 仓库还在其中记录了公共 API 兼容性规则：保持导出构造函数参数与数据类字段的位置含义，新增可选参数应尽可能置于末尾，若必须调整顺序则需补充兼容性测试。这体现了另一个优秀实践：将发布关键兼容性规则与技能触发器置于同一位置进行管理。

### 验证规则

一个清晰的例子是 `$code-change-verification`。

在两个代码库中，规则并非“始终运行冗长的验证流程”。规则是“当运行时代码、测试、示例或构建/测试行为发生变更时运行验证，且必须在验证通过后才能标记工作完成。”

条件性部分确保仅涉及文档的工作保持轻量化。强制性部分则保证 SDK 代码变更必须经过代码库的标准验证步骤。

实际的验证流程被编码在技能本身中。

在 Python 代码库中，它要求：

    make format
    make lint
    make typecheck
    make tests

在 JavaScript 代码库中，该技能要求严格按照以下顺序执行：

    pnpm i
    pnpm build
    pnpm -r build-check
    pnpm -r -F "@openai/*" dist:check
    pnpm lint
    pnpm test

该技能编码了代码库对“已验证”的定义，而 `AGENTS.md` 文件使该定义具有可执行性。

### 变更集验证

JavaScript 代码库对包变更还有一个额外的强制步骤：围绕 [Changesets](https://github.com/changesets/changesets) 构建的 `$changeset-validation`。

当 `packages/` 目录下的任何内容发生变更，或 `.changeset/` 目录发生变更时，模型需要做的不仅仅是运行测试。它必须创建或更新正确的变更集，验证版本升级级别，并确认变更集与实际代码差异相匹配。

该技能不仅检查文件是否存在。它会要求 Codex 评估 git 差异，并将验证规则保存在共享提示中，以确保本地运行和 GitHub Actions 使用相同的逻辑。同时它还编码了代码库特定的策略，例如：

  * 当已存在变更集时，使用现有分支的变更集而非创建新集
  * 将摘要保持为符合约定式提交风格的单行内容，使其可兼作提交标题
  * 在 1.0 版本前，常规功能开发避免主版本号升级，并将明确标记为仅预览的新功能视为补丁变更（若未改变现有行为）
  * 根据实际包变更验证所需的版本升级级别

这使得 Codex 需要对其创建的发布元数据进行验证后，才能宣告工作完成。

### 使用最新文档

两个代码库在涉及OpenAI API或平台集成的工作时，均要求具备`$openai-knowledge`技能。

该技能是对官方[OpenAI文档MCP](https://developers.openai.com/learn/docs-mcp)的轻量封装。它并非让模型依赖记忆作答，而是指示Codex调用OpenAI开发者文档MCP服务器，实时查询最新文档内容，涵盖响应API、工具、流式传输、实时通信及MCP等接口。

若本地Codex环境中尚未配置MCP服务器，该技能会引导维护者查阅[文档MCP快速入门指南](https://developers.openai.com/learn/docs-mcp#quickstart)及[官方MCP服务器端点](https://developers.openai.com/mcp)。

### 准备PR交接

在实质性工作结束时，两个代码库都会使用`$pr-draft-summary`技能。

该技能仅在任务基本完成或准备进入评审阶段，且变更涉及核心代码、测试用例、示例、影响行为的文档或构建/测试配置时触发。它会自动收集分支名称、工作树状态、变更文件、差异统计和近期提交记录，并生成：

* 分支命名建议
* PR标题
* PR描述草案

输出格式经过刻意固化设计，典型生成结果如下所示：

    # 拉取请求草案

    ## 分支命名建议

    git checkout -b fix/tracing-lazy-init-fork-safety

    ## 标题

    fix: #2489 通过延迟初始化追踪全局变量避免导入时分支安全隐患

    ## 描述

    本拉取请求通过将追踪引导程序改为首次使用时延迟初始化的方式，修复了可能破坏基于分支的进程模型的导入时追踪副作用问题。

    更新了追踪设置机制，使初始化在首次访问时仅执行一次，同时保留现有公开追踪API。

    新增了针对导入时行为、一次性引导程序和自定义提供程序处理的回归测试。

    本拉取请求解决了#2489号问题。

当您信任模型能够自主验证并总结其工作成果时，要求其生成PR草案便成为自然的收尾步骤。这既能保持交接流程的一致性，又能在编码工作完成后减少重复性文案撰写工作。

## 撰写更优质的描述

技能文件 `SKILL.md` 前置元数据中的 `description` 字段属于路由契约的一部分。

这是结构性的要求，而非风格性的。[《智能体技能规范》](https://agentskills.io/specification) 将 `name` 和 `description` 规定为 `SKILL.md` 前置元数据的必填字段，其渐进式披露模型明确指出：系统启动时会为所有技能加载这两个字段。完整的 `SKILL.md` 正文以及任何 `scripts/`、`references/` 或 `assets/` 内容，仅在技能实际被激活时才会延迟加载。

[Codex 技能文档](/codex/skills) 与 [定制化文档](/codex/concepts/customization#skills) 从 Codex 侧阐述了相同的行为逻辑：Codex 启动时通过各技能的元数据进行发现，仅在选定技能时加载 `SKILL.md`，而引用文件读取或脚本执行则按需触发。[OpenAI API 指南中的技能章节](https://developers.openai.com/cookbook/examples/skills_in_api/#what-is-a-skill) 对托管环境侧的说明同样明确：OpenAI 首先读取每个技能的 `name`、`description` 和路径信息，模型依据这些信息决策何时读取完整 `SKILL.md`。其 [SKILL.md 前置元数据章节](https://developers.openai.com/cookbook/examples/skills_in_api/#skillmd-frontmatter) 更直接地指出：`name` 和 `description` 对技能发现与路由至关重要。

在 Agents SDK 代码库中，这意味着在 Codex 读取技能其余内容之前，`description` 已成为主要的路由信号之一。

以下以 `code-change-verification` 为例进行具体说明：

**过于模糊的描述：**

    description: 在 OpenAI Agents JS 单体仓库中运行强制验证流程。

**更优描述（实际采用的版本）：**

    description: 当 OpenAI Agents JS 单体仓库中的运行时代码、测试用例或构建/测试行为发生变更时，运行强制验证流程。

简短版本虽已向 Codex 说明技能功能，但未明确技能适用场景、触发变更类型及检查是否可选。而更具体的版本则完整传达了这三层信息。

相同模式也体现在 `pr-draft-summary` 中：

**过于模糊的描述：**

description: 为代码变更完成后创建PR标题和草稿描述。

更优版本（实际使用的描述）：

    description: 在实质性代码变更完成后创建PR标题和草稿描述。适用于中等及以上规模变更（运行时代码、测试用例、构建配置、影响行为的文档）收尾阶段，需要生成包含变更摘要和PR草稿文本的PR就绪摘要块。

重申：真实描述是路由元数据。它向Codex传达：

  * 这是任务收尾阶段的技能
  * 仅针对实质性变更，而非每次对话回合
  * 输出的是PR就绪文本块，而非普通 prose 摘要

从这些代码库中获得的一个实际经验是：应在`description`上投入时间。如果路由机制不可靠，应在添加更多代码前先修复元数据。

## 将机械性操作放入脚本

接下来要解决的问题是：哪些功能应放在模型中，哪些应下沉到脚本中。

可靠的划分原则是：

  * 解释、比较和报告功能保留在模型中
  * 确定性的、重复的 shell 操作放入 `scripts/` 目录

这与公开指导原则一致。[Codex定制文档](/codex/concepts/customization#skills)将技能描述为：在不预先膨胀上下文的情况下，为Codex提供更丰富的指令、脚本和参考资料以实现可重复工作流的方式。这符合模型优先的架构设计：让Codex处理依赖上下文的工作环节，仅在需要时调用脚本处理确定性环节。[OpenAI API使用指南中的技能章节](https://developers.openai.com/cookbook/examples/skills_in_api/#operational-best-practices)也建议将技能脚本设计为微型CLI工具：可通过命令行运行、输出确定性标准输出、通过使用说明或错误信息明确报错、必要时将输出写入已知文件路径。

在Agents SDK代码库中，我们尝试在模型智能真正发挥价值的场景使用模型，例如：

  * 通过阅读源代码推断预期行为
  * 将日志记录与预期行为进行比对
  * 判断版本差异是否包含实际兼容性风险
  * 生成可供维护者操作的说明文本

而脚本则负责处理围绕这些工作的机械性操作，例如：

* 以固定顺序运行仓库所需的验证命令
* 启动示例运行，收集每个示例的日志，并为失败案例生成重运行文件
* 在发布就绪审查前获取上一个发布标签
* 提供辅助命令如`start`、`stop`、`status`、`logs`、`tail`、`collect`和`rerun`，使相同工作流能够轻松重复执行

如果模型每次都需要重新发现相同的Shell操作流程，这通常意味着该流程应该编写为脚本。如果任务依赖于上下文、权衡或解释说明，这部分内容则应保留给模型处理。

## 自动化集成测试

两个代码仓库中最有价值的工作流领域之一是自动化集成测试。这里包含两个相关层面：在两个仓库中自动验证内置示例，以及在JavaScript仓库中单独验证已发布软件包在用户实际安装使用时是否仍能正常工作。

在此设置之前，示例验证过程部分依赖人工操作。虽然可以运行示例，但最终阶段往往需要人工检查日志或通过观察判断输出结果是否正确。这对于单个示例尚可管理，但在不断增长的SDK仓库中难以规模化实施。

第一层是`examples-auto-run`系统，但相关技术能力是在运行器开发完成后形成的。要实现示例验证的完全自动化，我们首先必须在两个仓库中构建非交互式示例执行的基础支持。这意味着需要让示例脚本能够在自动模式下运行，包括那些通常涉及提示或确认操作的示例。

这项基础工作包含：

* 自动应答常见的交互式提示
* 在运行器支持的情况下，自动批准HITL、MCP、`apply_patch`和Shell操作
* 将仍不适合自动化的示例（如需要额外运行时设置的真实场景或Next.js应用示例）列入自动跳过清单
* 为每个示例运行生成结构化日志
* 创建重运行文件，使得失败案例能够单独重试而无需重新运行全部测试

在基础框架搭建完成后，我们将其组织为一项技能，使工作流程变得可复用且易于调用。在Python代码库中，`examples-auto-run`封装了`uv run examples/run_examples.py --auto-mode --write-rerun --main-log ... --logs-dir ...`命令。在JavaScript代码库中，它先执行构建检查，随后以自动模式运行`pnpm examples:start-all`，并为每个示例提供独立的日志记录与重试支持。

为提升验证质量，运行器的任务是执行示例代码，并将每个示例的标准输出与错误输出保存至独立日志中。随后该技能会驱动Codex逐条分析这些日志，并与源代码进行比对：

* 读取示例源码及注释
* 推断预期执行流程
* 打开对应的日志文件
* 将预期行为与实际输出进行比对
* 对每个成功运行的示例执行此流程，而非仅抽样检查

这种方法比将正确性编码为固定脚本级断言更为精确灵活。虽然成功退出码具有参考价值，但对于需要调用真实API、使用工具或生成结构化输出的示例而言并不足够。通过先记录实际输出，再与源代码进行细致比对，我们能依据每个示例的真实意图进行验证。

在JavaScript代码库中还存在第二层验证：独立的`integration-tests`技能。该工作流程不仅限于在本地运行源码示例，还会将软件包发布到本地Verdaccio注册表，并在多环境中测试安装与运行，包括Node.js、Bun、Deno、Cloudflare Workers及Vite React应用。这能发现另一类问题：不仅验证“示例是否能在代码库中运行”，更验证“软件包在发布、安装及运行时集成后是否仍能保持正确行为”。

综合来看，这些工作流程揭示了结合技能、脚本与模型判断的价值所在：脚本确保运行可重复性、捕获执行证据，并覆盖了人工检查繁琐的安装路径；Codex则利用这些证据进行比简单脚本化通过/失败检查更细致的比对。

## 增加发布检查

发布准备是这一模式同样能发挥作用的另一个领域。

两个仓库中的发布审查工作流均始于查找上一个发布标签，将其与最新的`main`分支进行差异比对，然后调用Codex分析该差异以检查：

* 公共API及面向用户的SDK行为中的向后兼容性问题
* 回归问题，包括预期行为的细微变化
* 需要补充迁移说明或更新发布说明的变更项缺失情况

基于这些发现，该智能模块会做出整体发布就绪性判定。

一个具体案例是[openai/openai-agents-python#2480](https://github.com/openai/openai-agents-python/pull/2480)，该次发布审查在保持整体绿色通过的同时，仍明确指出对Python 3.9支持的移除及其所需的发布说明跟进：

    发布就绪性审查（节选）

    发布判定：
    🟢 绿灯放行。次版本号升级包含预期重大变更（Python 3.9支持移除），未发现具体回归问题。

    变更范围概览：

    - 共修改38个文件（+1450/-789行）；关键涉及区域：`src/agents/tool.py`、
      `src/agents/extensions/`、`src/agents/realtime/`、`tests/`、
      `pyproject.toml`、`uv.lock`。

    Python 3.9支持已移除

    - 风险等级：🟡 中等。依赖Python 3.9的用户将无法安装0.9.0版本
    - 证据：`pyproject.toml`现设置`requires-python = ">=3.10"`并移除Python 3.9分类标识；CI中针对3.9的跳过逻辑已删除
    - 后续措施：确保发布说明明确标注Python 3.9支持移除，且打包元数据保持`>=3.10`要求

该智能模块还定义了门控决策机制。审查默认以“可安全发布”为起点，仅当差异分析显示具体实际问题证据时才转为阻止状态。每次阻止判定必须附带具体的解阻检查清单。这使得输出结果更易使用：绿色结果表示差异分析中未发现阻碍发布的问题，而阻止结果则意味着存在明确后续步骤的实际问题。

这比泛泛的“请审阅本次发布”更有用。它迫使模型基于具体的代码差异进行推理，并以可操作的术语解释结果。如果发布是安全的，请明确说明；如果不安全，则需指出确切的证据以及所需的具体后续措施。

## 在CI中运行工作流

一旦某项技能在本地环境中证明有效，[Codex GitHub Action](/codex/github-action) 可轻松实现CI中相同工作流的自动化。当本地工作流已稳定运行时效果最佳，因为手动使用阶段正是调试指令、优化脚本和发现实际边界案例的关键环节。

对于公共代码库，触发机制的设计与技能本身同等重要。[GitHub Action安全清单](/codex/github-action#security-checklist)建议：限制工作流启动权限，优先采用可信事件或显式审批机制，对来自PR、提交记录、议题或评论的提示输入进行净化处理，通过`drop-sudo`或非特权用户保护`OPENAI_API_KEY`，并将Codex设置为作业的最后执行步骤。

若工作流具备写入权限且接收不可信的公共输入，风险通常存在于触发机制设计、输入处理流程以及技能运行时的权限配置环节。

## 在PR审阅中使用Codex

技能提升只是这些代码库生产力故事的一个方面，[Codex GitHub PR自动审阅](/codex/integrations/github)则是另一重要维度。

自Codex GitHub PR自动审阅功能上线以来，它已成为这些代码库中大多数代码变更的有效审阅者。我们将其作为常规审阅流程的组成部分，而非特殊场景工具。

对于明显的程序错误、功能回归和缺失测试，在实践中依赖Codex作为必要审阅路径已足够可靠。它能持续稳定地反复核查相同的正确性模式，并为小型修复和常规改进消除了主要瓶颈。

同行审阅依然重要，但其关注点已转向另一类变更。

当核心问题并非“这段代码是否正确？”，而是“我们应在多个有效方案中作何选择？以及如何部署实施？”时，人工审阅仍不可或缺。这类情况包括：

  * 涉及API或架构变更，存在多种合理设计方案，需要维护者明确做出选择的情况
  * 影响产品预期、向后兼容承诺或发布策略的行为变更
  * 命名规范、迁移方案及发布通告等决策，其难点在于如何选择对用户和贡献者最清晰的方案
  * 需要维护者或跨团队达成共识的变更，例如工作范围界定、实施顺序安排，以及当前版本与后续版本的功能划分

Codex在所有上述场景中仍能提供有效支持，但这些决策仍需人类决策者通过直接讨论来最终定夺。

`AGENTS.md`文件也可体现这种分工：代码库可告知Codex哪些内容属于正确性审查的关键要素，而Codex能持续应用这些指导原则。

这种模式显著提升了处理效率。重复性的审查与验证工作不再需要为每个低风险变更等待稀缺的审核资源，同时维护者可专注于需要更高情境判断力的审查工作。这种转变帮助我们更快地处理积压缺陷和较小的功能改进。

## 最终思考

在OpenAI智能体SDK代码库中，当技能成为仓库常规工作流程的组成部分时，其效能最为显著。

`AGENTS.md`文件告知Codex必须执行的工作流程。`description`字段指示何时触发这些流程。`scripts/`目录处理确定性环节。模型则负责情境化部分。当本地工作流程稳定后，[Codex GitHub Action](/codex/github-action)可将相同流程延伸至持续集成环境。

这使得日常工程工作在这些代码库中变得更加明确可靠。同时，由于验证、发布审查和PR交接现在都遵循相同的可重复流程，小型改进的交付速度也得以加快。

## 资源列表

* [OpenAI Agents SDK for Python](https://github.com/openai/openai-agents-python)
* [OpenAI Agents SDK for JS](https://github.com/openai/openai-agents-js)
* [Codex 中的技能](/codex/concepts/customization#skills)
* [使用 AGENTS.md 进行自定义指令](/codex/guides/agents-md)
* [Codex GitHub Action](/codex/github-action)
* [在 GitHub 中使用 Codex](/codex/integrations/github)
* [OpenAI API 示例库中的技能](https://developers.openai.com/cookbook/examples/skills_in_api)
* [Agent Skills 规范](https://agentskills.io/specification)
* [OpenAI API 中的技能：操作最佳实践](https://developers.openai.com/cookbook/examples/skills_in_api/#operational-best-practices)
