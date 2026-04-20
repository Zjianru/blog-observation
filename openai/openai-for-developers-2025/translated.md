# 2025年开发者视角下的OpenAI

来源：https://developers.openai.com/blog/openai-for-developers-2025

---

2025年的重点并非单一模型发布，而是AI在生产环境中变得更易部署的一年。随着模型在规划、工具使用和长周期任务处理能力上的提升，更多团队从“逐步提示”转向将工作委托给智能体执行。

对开发者而言，这种转变体现在几个具体方面：

  * **推理能力成为核心调节器**，并日益与通用对话模型融合。
  * **多模态支持（文档、音频、图像、视频）** 在API中成为一等公民。
  * **智能体构建模块**（Responses API、Agents SDK、AgentKit）让多步骤工作流更易部署和运维。
  * **Codex** 使得开发速度和质量达到前所未有的高度。

## 内容概要

  * 核心转变在于**原生智能体API**与**更优模型**的结合，使模型能执行需要推理和工具调用的复杂任务。
  * Codex在模型和工具链层面全面成熟，GPT-5.2-Codex的仓库级推理能力与面向生产的CLI、Web及IDE工作流相结合，赋能长周期编码任务。
  * 改进的工具链让模型更顺畅地接入真实系统，减少使用摩擦。
  * 多模态输入输出（PDF、图像、音频、视频）成为端到端工作流的实用默认配置。
  * 评估体系、分级器和调优功能成熟化，形成更可复现的“测量→改进→部署”循环。

下文将盘点2025年主要的模型、API和平台更新，助您构建生产级智能体。

## 推理能力：从独立模型到统一体系

自2024年末我们首次引入“推理”范式（让模型获得“思考时间”）后，2025年初迎来了**推理模型**作为独立家族的时期。**o1**、**o3**和**o4-mini**等模型证明，通过额外计算资源进行先思考后回答，能显著提升复杂多步骤任务的可靠性。

值得特别指出的是，**o3-mini**首次表明推理能力不仅是前沿功能，更能以高性价比、开发者友好的形态交付。

到2025年中后期，**融合**成为主流趋势：推理深度、工具使用和对话质量日益集成于同一旗舰模型系列（对多数团队而言，“选择模型”更多是成本/延迟/质量的权衡，而非在不同家族间抉择）。

以推理为先的版本如[**o1**](https://platform.openai.com/docs/models/compare)、[**o3 / o4-mini**](https://openai.com/index/introducing-o3-and-o4-mini)和[**o3-mini**](https://openai.com/research/openai-o3-mini)，使“深度思考与快速响应”成为开发者可调节的决策维度。随着时间推移，这些特性逐步融入GPT-5.x系列，将通用智能、推理深度、代码专业化与多模态能力统一于单一模型体系。

## 多模态：音频、视觉、图像与视频

截至2025年末，**多模态**不再仅指“能接收图像输入”，而是意味着“可跨模态构建端到端产品”——通常通过单一工作流实现。

### 音频+实时处理

  * [**新一代音频模型**](https://openai.com/index/introducing-our-next-generation-audio-models)提升了语音转文本精度，增强可控文本转语音功能，支持生产级语音管道。

*   [**Realtime API**](https://developers.openai.com/blog/realtime-api) 正式发布，实现了低延迟、双向音频流传输，使得生产级的实时语音助手和对话界面成为可能。

### 图像

  *   [**GPT Image 1**](https://platform.openai.com/docs/models/gpt-image-1) 引入了新一代图像生成模型，能够生成高质量图像并进行结构化编辑，其对世界的理解更深入，指令遵循能力更强。
  *   高输入保真度使得在编辑图像时，能更稳定地保留人脸、徽标等细节。
  *   [**GPT Image 1 mini**](https://platform.openai.com/docs/models/gpt-image-1-mini) 使原生图像生成更具成本效益。
  *   [**GPT Image 1.5**](https://openai.com/index/new-chatgpt-images-is-here/) 是我们最先进的生成模型，标志着图像质量和编辑一致性的重大飞跃。
  *   在 Responses API 中将图像生成作为一种工具，使其能够与其他工具结合，在多轮对话中创建图像。

### 视频

  *   [**Sora 2 和 Sora 2 Pro 模型**](https://platform.openai.com/docs/guides/video-generation#sora-2) 引入了更高保真度的视频生成，具有更强的时间连贯性和混剪支持。
  *   [**Video API**](https://platform.openai.com/docs/api-reference/videos) 通过 `v1/videos` 端点开放了视频生成和编辑功能，使视频与文本、图像和音频一同成为 API 中的一等模态。

### PDF 与文档

  *   [**PDF 输入**](https://platform.openai.com/docs/guides/file-inputs) 使得重度依赖文档的工作流可以直接在 API 中实现。
  *   [**PDF-by-URL**](https://platform.openai.com/docs/guides/file-inputs#file-urls) 通过引用文档 URL 而无需上传，减少了操作摩擦。

**重要意义：** 你现在可以依赖 OpenAI 平台，不仅处理文本和视觉任务，还能处理图像和视频生成工作流以及语音到语音的用例。

## Codex

2025年，Codex 超越了单纯的代码模型，成为了你的软件工程师队友：它连接模型、本地工具和云端，帮助开发者处理更长期、更复杂的编码任务。

### 模型

早期的推理模型在复杂编码任务（多文件编辑、调试、规划）上展现出显著优势。到2025年中后期，这些能力被整合进 **GPT-5 系列**，其中 [**GPT-5.2-Codex**](https://openai.com/index/introducing-gpt-5-2-codex/) 成为代码生成、审查和仓库级推理的最新默认选择——它不再是与通用模型分离的独立模型，而是通用模型内部的专门化版本。

### CLI

开源的 [**Codex CLI**](https://developers.openai.com/codex/cli) ([GitHub](https://github.com/openai/codex)) 将智能体风格的编码直接带入本地环境，使开发者能够在真实的代码仓库上运行 Codex，迭代审查变更，并在人工监督下将编辑应用到文件中。这使得长期编码任务在日常工作流中变得切实可行。

Codex 也变得更易于在交互式使用之外进行部署，内置了对可重复自动化模式的支持，例如 [**脚本化 Codex**](https://developers.openai.com/codex/sdk#using-codex-cli-programmatically)。

### 安全性、控制与集成

Codex 深入理解了产品交付的现实需求：[**沙盒机制**](https://developers.openai.com/codex/sandbox)和[**审批模式**](https://developers.openai.com/codex/cli/features#approval-modes)让人工监督更易融入流程。同时，对[**AGENTS.md**](https://developers.openai.com/codex/guides/agents-md)和[**MCP**](https://developers.openai.com/codex/mcp)的支持让Codex能更轻松地适配你的代码库，通过第三方工具和上下文进行扩展，甚至能[**通过Agents SDK编排Codex**](https://developers.openai.com/codex/guides/agents-sdk)（将CLI作为MCP服务器运行）。

### Web端、云端与IDE

除了CLI，Codex还在[**Web+云端**](https://developers.openai.com/codex/cloud)和[**IDE扩展**](https://developers.openai.com/codex/ide)中加强了对长会话和迭代问题解决的支持，缩短了对话推理与具体代码变更之间的循环周期。团队还可以在CI中通过[**Codex Autofix**](https://developers.openai.com/codex/guides/autofix-ci)自动化部分工作流程。

**关键意义**：到2025年底，Codex已不再仅仅是“一个可供提示的模型”，而更像一个编码界面——它将具备推理能力的模型与开发者已使用的工具相结合。

## 平台转型：Responses API与智能体构建模块

2025年最重要的平台变革之一是向**原生智能体API**的演进。

[**Responses API**](https://developers.openai.com/blog/responses-api)让针对新一代模型的开发变得更简单：

  * 支持多输入输出，包括不同模态
  * 支持推理控制与摘要生成
  * 增强的工具调用支持，包括在推理过程中调用

在此基础之上，2025年还带来了更高层次的构建模块，例如开源的[**Agents SDK**](https://openai.github.io/openai-agents-python/)和[**AgentKit**](https://openai.com/index/introducing-agentkit/)，让智能体的构建与编排更加便捷。

状态管理与持久化也变得更容易：

  * [**对话状态**](https://platform.openai.com/docs/guides/conversation-state)（及配套的[**Conversations API**](https://platform.openai.com/docs/api-reference/conversations/create-item)）支持持久化线程与可重放状态
  * [**连接器与MCP服务器**](https://platform.openai.com/docs/guides/tools-connectors-mcp)支持集成外部上下文并通过可信工具界面执行操作

**关键意义**：构建多步骤智能体和长时运行工作流现在需要更少的自定义粘合代码和状态管理。

除了强大的基础组件，我们还推出了一套内置的[**工具**](https://platform.openai.com/docs/guides/tools#available-tools)以最大化模型效用。

* * *

## 工具：从网络搜索到工作流

2025年，我们推出了一系列标准化、可组合的能力，让智能体能够安全地执行有效工作。

  * [**网络搜索**](https://platform.openai.com/docs/guides/tools-web-search)为需要最新信息和引用来源的智能体提供了简单的检索基础功能。
  * [**文件搜索**](https://platform.openai.com/docs/guides/tools-file-search/)（向量存储）提供了默认托管的RAG基础功能，可与Responses API和结构化输出无缝组合使用。

*   [**代码解释器**](https://platform.openai.com/docs/guides/tools-code-interpreter) 在沙盒容器中运行 Python，用于数据处理、文件转换和迭代调试。
    *   [**计算机使用**](https://platform.openai.com/docs/guides/tools-computer-use) 实现了“点击/输入/滚动”的自动化循环（最好与沙盒环境和人工介入配合使用）。

**重要性所在：** 智能体能够可靠地检索、计算和行动，无需每个团队都重新发明一套自定义工具运行时。

## 运行与扩展：异步、事件和成本控制

一旦智能体从“单次请求”转向“多步骤任务”，生产团队就需要应对成本、延迟和可靠性的基础构件。

*   [**提示缓存**](https://platform.openai.com/docs/guides/prompt-caching) 在提示共享较长、重复前缀（系统提示、工具、模式）时，降低了延迟和输入成本。
*   [**后台模式**](https://platform.openai.com/docs/guides/background) 支持长时间运行的响应，而无需保持客户端连接打开。
*   [**Webhooks**](https://platform.openai.com/docs/guides/webhooks) 将“轮询一切”转变为事件驱动系统（批量完成、后台完成、微调完成）。
*   [**速率限制**](https://platform.openai.com/docs/guides/rate-limits) 和工作负载优化指导随着使用层级和模型系列的扩展而成熟。

**重要性所在：** 构建智能体变得与系统设计（异步 + 事件 + 预算）同等重要，不亚于提示工程。

## 开放标准与开源智能体构建模块

伴随 API 整合，2025 年强调了智能体系统的**互操作性和可组合性**。

*   开源的 **Agents SDK** 为 [**Python**](https://openai.github.io/openai-agents-python/) ([GitHub](https://github.com/openai/openai-agents-python)) 和 [**TypeScript**](https://openai.github.io/openai-agents-js/) ([GitHub](https://github.com/openai/openai-agents-js)) 提供了实用的构建模块，涵盖工具使用、任务交接、安全护栏和追踪——并且是**供应商无关的**，文档中说明了使用非 OpenAI 模型的路径。
*   [**AgentKit**](https://openai.com/index/introducing-agentkit/) 为希望更快交付和迭代的团队，增加了围绕智能体开发的高级工具（包括 Agent Builder、ChatKit、Connector Registry 和评估循环）。
*   在标准方面，OpenAI 推动了 **AGENTS.md** ([规范](https://agents.md/)) 并参与了 [**AAIF（Agentic AI 基金会）**](https://aaif.io/news/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation-aaif-anchored-by-new-project-contributions-including-model-context-protocol-mcp-goose-and-agents-md/)，同时参与其他生态系统标准如 [**模型上下文协议 (MCP)**](https://modelcontextprotocol.io/) 和 [**Skills**](https://developers.openai.com/codex/skills)。对开发者的价值在于：随着生态系统在共享规范上趋同，可移植的智能体工具增多，一次性集成减少。

除了我们在智能体及相关标准方面的工作，我们还推出了 [Apps SDK](/apps-sdk)——一个开源框架，它扩展了模型上下文协议 (MCP)，让开发者能够与其 MCP 服务器一同构建 UI，定义可在 ChatGPT 等客户端中运行的应用程序的逻辑和交互界面。

**重要性所在：** 开发者可以构建与单一运行时或 UI 界面耦合度更低的智能体，并更轻松地将 OpenAI 驱动的智能体集成到异构系统中。

## 开源权重模型

除托管API外，OpenAI还发布了**开源权重模型**，旨在实现透明度、支持研究及本地化部署，同时保持强大的推理和指令遵循能力。

  * [**gpt-oss 120b 和 20b**](https://huggingface.co/collections/openai/gpt-oss) 推理模型，专为自主托管和本地化部署设计。
  * [**gpt-oss-safeguard 120b 和 20b**](https://huggingface.co/collections/openai/gpt-oss-safeguard) 安全与策略模型，旨在与gpt-oss协同运行。

## 评估、调优与安全部署

  * [**评估API**](https://platform.openai.com/docs/api-reference/evals/getRun) 支持基于评估的开发流程。
  * [**强化微调**](https://platform.openai.com/docs/guides/reinforcement-fine-tuning) 利用可编程评分器进行模型优化。
  * [**监督微调/蒸馏**](https://platform.openai.com/docs/guides/distillation) 在通过大模型验证任务后，将能力迁移至更小、更经济的模型。
  * [**评分器**](https://platform.openai.com/docs/guides/graders) 与[**提示优化器**](https://platform.openai.com/docs/guides/prompt-optimizer) 帮助团队更高效地运行“评估→改进→再评估”的闭环流程。

## 总结回顾

整个2025年，我们聚焦于几个核心主题，致力于让开发者更便捷地在我们的平台上构建和部署应用：

  * 规模化、可控的推理作为核心能力
  * 统一、面向智能体原生的API接口
  * 开放的构建模块与新兴的互操作性标准
  * 涵盖文本、图像、音频、视频和文档的深度多模态支持
  * 更强大的生产工具链，用于评估、调优和部署

### 按任务推荐的模型（2025年末）

如果您正在启动新项目或升级现有集成，以下是为各类任务推荐的“默认选择”：

  * **通用场景（文本+多模态）：** [**GPT-5.2**](https://openai.com/index/introducing-gpt-5-2/) 适用于对话、长上下文处理及多模态输入。
  * **深度推理/可靠性敏感型任务：** [**GPT-5.2 Pro**](https://platform.openai.com/docs/models/compare) 适用于规划类任务及值得投入额外计算资源以换取更高质量的场景。
  * **编程与软件工程：** [**GPT-5.2-Codex**](https://platform.openai.com/docs/models/compare) 适用于代码生成、审查、仓库级推理及工具驱动的编程智能体。
  * **图像生成与编辑：** [**GPT Image 1.5**](https://openai.com/index/new-chatgpt-images-is-here/) 适用于高保真度图像生成与迭代编辑。
  * **实时语音交互：** [**gpt-realtime**](https://platform.openai.com/docs/guides/realtime) 适用于低延迟语音对话及实时语音智能体。

有关最新可用性与分级信息，请参阅官方[**模型对比页面**](https://platform.openai.com/docs/models/compare)。

这些更新为未来的发展奠定了基础。感谢您在2025年与我们共同构建，我们期待看到您在2026年的创新成果。

## 链接与资源

  * [提示优化器](https://platform.openai.com/chat/edit?models=gpt-5&optimize=true)
  * [模型对比](https://platform.openai.com/docs/models/compare)（当前名称、可用性与分级）
  * [智能体SDK (Python)](https://openai.github.io/openai-agents-python/) 与[智能体SDK (TypeScript)](https://openai.github.io/openai-agents-js/)

* [Codex 文档](https://developers.openai.com/codex/) 与 [Codex CLI GitHub](https://github.com/openai/codex)
  * [图像游乐场](https://platform.openai.com/playground/images)
  * [平台更新日志](https://platform.openai.com/docs/changelog)（功能发布时间记录）