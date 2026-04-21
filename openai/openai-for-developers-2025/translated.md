# 2025年面向开发者的OpenAI

来源：https://developers.openai.com/blog/openai-for-developers-2025

---

2025年的重点并非单一模型的发布，而是人工智能在生产环境中运行变得更加便捷的一年。随着模型在规划、工具使用和长周期任务方面的能力不断提升，越来越多的团队从“逐步提示”转向将工作委托给智能体处理。

对开发者而言，这一转变体现在几个具体方面：

  * **推理成为核心调节器**，并日益与通用聊天模型融合。
  * **多模态支持（文档、音频、图像、视频）** 在API中成为一等公民。
  * **智能体构建模块**（Responses API、Agents SDK、AgentKit）让多步骤工作流的部署和运维更加轻松。
  * **Codex** 使得开发速度和质量达到前所未有的高度。

## 内容提要

  * 重大转变在于**原生智能体API**与**更强大的模型**的结合，这些模型能够执行需要推理和工具使用的复杂任务。
  * Codex在模型和工具链方面均趋于成熟，GPT-5.2-Codex的仓库级推理能力与面向生产的CLI、Web及IDE工作流相结合，助力长周期编码任务。
  * 改进的工具链让模型更顺畅地接入实际系统，减少了使用摩擦。
  * 多模态输入输出（PDF、图像、音频、视频）成为端到端工作流的实用默认配置。
  * 评估系统、分级器和调优功能演变为更可复现的“测量→改进→部署”循环。

下文将回顾2025年主要的模型、API和平台更新，并探讨它们如何助您部署生产级智能体。

## 推理：从独立模型到统一产品线

自2024年末我们首次引入“推理”范式（即让模型拥有“思考时间”）以来，2025年初曾是“推理模型”作为一个独立产品系列的时期。诸如 **o1**、**o3** 和 **o4-mini** 等模型明确表明，通过额外计算资源让模型在回答前进行思考，能显著提升复杂多步骤工作的可靠性。

值得一提的是，**o3-mini** 首次释放出明确信号：推理能力将不仅是前沿模型的专属功能，还能以高性价比、开发者友好的形态交付。

到2025年中后期，行业主流趋势已演变为 **融合化**：推理深度、工具调用能力和对话质量日益集成于同一旗舰模型系列（对多数团队而言，“选择模型”更多成为成本/延迟/质量的权衡，而非在不同技术路线的模型家族间抉择）。

以推理为核心设计的版本如 [**o1**](https://platform.openai.com/docs/models/compare)、[**o3 / o4-mini**](https://openai.com/index/introducing-o3-and-o4-mini) 和 [**o3-mini**](https://openai.com/research/openai-o3-mini)，推动“深度思考与快速响应”成为开发者可调节的技术决策。随着时间推移，这些理念逐步融入GPT-5.x系列，将通用智能、深度推理、代码专业化与多模态能力统一于单一模型体系。

## 多模态：音频、视觉、图像与视频

截至2025年末，_多模态_ 不再仅指“可接收图像输入”，而是意味着“能够构建跨模态的端到端产品”——通常可在单一工作流中实现。

### 音频+实时交互

  * [**新一代音频模型**](https://openai.com/index/introducing-our-next-generation-audio-models) 提升了语音转文字精度，增强了可控文本转语音功能，支撑生产级语音流水线
  * [**实时API**](https://developers.openai.com/blog/realtime-api) 正式发布并实现低延迟双向音频流传输，使生产级实时语音助手与对话界面成为可能

### 图像

*   [**GPT Image 1**](https://platform.openai.com/docs/models/gpt-image-1) 引入了新一代图像生成模型，能够生成高质量图像并进行结构化编辑，其对世界的理解更深刻，指令遵循能力也更强。
*   高输入保真度使得在编辑图像时，能更稳定地保留如人脸和徽标等细节。
*   [**GPT Image 1 mini**](https://platform.openai.com/docs/models/gpt-image-1-mini) 使原生图像生成更具成本效益。
*   [**GPT Image 1.5**](https://openai.com/index/new-chatgpt-images-is-here/) 是我们最先进的生成模型，标志着图像质量和编辑一致性的重大飞跃。
*   作为 Responses API 中的一项工具，图像生成功能使得在多轮对话中结合其他工具创建图像成为可能。

### 视频

*   [**Sora 2 和 Sora 2 Pro 模型**](https://platform.openai.com/docs/guides/video-generation#sora-2) 引入了更高保真度的视频生成，具有更强的时间连贯性和混音支持。
*   [**Video API**](https://platform.openai.com/docs/api-reference/videos) 通过 `v1/videos` 端点开放了视频生成和编辑功能，使视频成为 API 中与文本、图像和音频并列的一等模态。

### PDF 与文档

*   [**PDF 输入**](https://platform.openai.com/docs/guides/file-inputs) 使得直接在 API 中处理文档密集型工作流成为可能。
*   [**PDF-by-URL**](https://platform.openai.com/docs/guides/file-inputs#file-urls) 通过引用文档而无需上传，减少了操作摩擦。

**其重要性在于：** 你现在可以依赖 OpenAI 平台，不仅用于文本和视觉任务，还可用于图像和视频生成工作流以及语音到语音的应用场景。

## Codex

2025年，Codex 超越了仅仅作为一个代码模型的角色，成为了你的软件工程师队友：它连接模型、本地工具和云端，帮助开发者应对更长期、更复杂的编码任务。

### 模型

早期的推理模型在复杂编码任务（多文件编辑、调试、规划）上展现出显著优势。到2025年中后期，这些能力被整合进**GPT-5系列**，其中[**GPT-5.2-Codex**](https://openai.com/index/introducing-gpt-5-2-codex/)成为代码生成、审查及仓库级推理的最新默认选择——它不再独立于通用模型，而是作为其内置的专业化模块存在。

### 命令行界面

开源工具[**Codex CLI**](https://developers.openai.com/codex/cli)（[GitHub](https://github.com/openai/codex)）将智能体式编程直接引入本地环境，使开发者能在真实代码库上运行Codex，迭代审查修改内容，并在人工监督下应用文件变更。这让长周期编码任务得以融入日常开发流程。

Codex在交互式使用之外也变得更易部署，其内置了对可重复自动化模式的支持，例如[**脚本化调用Codex**](https://developers.openai.com/codex/sdk#using-codex-cli-programmatically)。

### 安全性、控制与集成

Codex深入契合实际开发需求：[**沙箱机制**](https://developers.openai.com/codex/sandbox)与[**审批模式**](https://developers.openai.com/codex/cli/features#approval-modes)让人工监督更易融入流程。同时，对[**AGENTS.md**](https://developers.openai.com/codex/guides/agents-md)和[**MCP**](https://developers.openai.com/codex/mcp)的支持使Codex能灵活适配代码库，通过第三方工具与上下文进行扩展，甚至可[**通过智能体SDK编排Codex**](https://developers.openai.com/codex/guides/agents-sdk)（将CLI作为MCP服务器运行）。

### 网页端、云端与集成开发环境

除命令行界面外，Codex在[**网页+云端平台**](https://developers.openai.com/codex/cloud)和[**IDE扩展**](https://developers.openai.com/codex/ide)中加强了对长会话与迭代问题解决的支持，缩短了对话式推理与具体代码变更间的循环周期。团队还可在持续集成中使用[**Codex自动修复**](https://developers.openai.com/codex/guides/autofix-ci)实现工作流环节的自动化。

**为何重要：** 到2025年底，Codex 已不再仅仅是“一个供你提示的模型”，而是演变为一个编程界面——它将具备推理能力的模型与开发者已熟用的工具相结合。

## 平台转变：Responses API 与智能体构建模块

2025年最重要的平台变革之一是向 **原生智能体 API** 的演进。

[**Responses API**](https://developers.openai.com/blog/responses-api) 让为新世代模型构建应用变得更加容易：

  * 支持多输入与多输出，包括不同模态
  * 支持推理控制与摘要生成
  * 更好地支持工具调用，包括在推理过程中进行

在此基础之上，2025年还带来了更高层次的构建模块，例如开源的 [**Agents SDK**](https://openai.github.io/openai-agents-python/) 和 [**AgentKit**](https://openai.com/index/introducing-agentkit/)，使得构建和编排智能体更为便捷。

状态与持久性管理也变得更为简单：

  * [**对话状态**](https://platform.openai.com/docs/guides/conversation-state)（以及 [**Conversations API**](https://platform.openai.com/docs/api-reference/conversations/create-item)）用于持久化线程和可重放的状态
  * [**连接器与 MCP 服务器**](https://platform.openai.com/docs/guides/tools-connectors-mcp) 用于整合外部上下文并通过可信工具界面执行操作

**为何重要：** 如今构建多步骤智能体和长时间运行的工作流，所需的定制粘合代码和状态管理大大减少。

除了强大的基础组件，我们还引入了一套功能强大的内置 [**工具**](https://platform.openai.com/docs/guides/tools#available-tools)，以最大化模型的实用性。

* * *

## 工具：从网络搜索到工作流

2025年，我们推出了一套标准化、可组合的能力，使得智能体能够安全地执行有用的工作。

*   [**网络搜索**](https://platform.openai.com/docs/guides/tools-web-search) 为需要最新信息和引用来源的智能体提供了一个简单的检索基础功能。
*   [**文件搜索**](https://platform.openai.com/docs/guides/tools-file-search/)（向量存储）提供了一个默认托管的RAG（检索增强生成）基础功能，可与响应和结构化输出无缝结合。
*   [**代码解释器**](https://platform.openai.com/docs/guides/tools-code-interpreter) 在沙盒容器中运行Python，用于数据处理、文件转换和迭代调试。
*   [**计算机使用**](https://platform.openai.com/docs/guides/tools-computer-use) 实现了“点击/输入/滚动”的自动化循环（最好与沙盒环境和人工监督结合使用）。

**重要性所在：** 智能体能够可靠地进行检索、计算和行动，而无需每个团队都重新发明一套自定义的工具运行时环境。

## 运行与扩展：异步、事件和成本控制

一旦智能体从“单次请求”转向“多步骤任务”，生产团队就需要针对成本、延迟和可靠性的基础功能。

*   [**提示缓存**](https://platform.openai.com/docs/guides/prompt-caching) 在提示共享较长且重复的前缀（系统提示、工具、模式）时，降低了延迟和输入成本。
*   [**后台模式**](https://platform.openai.com/docs/guides/background) 实现了长时间运行的响应，而无需保持客户端连接开放。
*   [**Webhooks**](https://platform.openai.com/docs/guides/webhooks) 将“轮询所有内容”转变为事件驱动系统（批量完成、后台完成、微调完成）。
*   随着使用层级和模型系列的扩展，[**速率限制**](https://platform.openai.com/docs/guides/rate-limits) 和工作负载优化指南也日趋成熟。

**重要性所在：** 构建智能体变得与系统设计（异步 + 事件 + 预算）和提示工程同等重要。

## 开放标准和开源智能体构建模块

除了API整合，2025年还强调了智能体系统的**互操作性和可组合性**。

* 开源的 **Agents SDK** 支持 [**Python**](https://openai.github.io/openai-agents-python/) ([GitHub](https://github.com/openai/openai-agents-python)) 和 [**TypeScript**](https://openai.github.io/openai-agents-js/) ([GitHub](https://github.com/openai/openai-agents-js))，为工具使用、任务交接、安全护栏和运行追踪提供了实用的构建模块——并且它是 **供应商无关的** ，提供了使用非 OpenAI 模型的文档化路径。
* [**AgentKit**](https://openai.com/index/introducing-agentkit/) 为希望快速交付和迭代的团队增加了更高层次的智能体开发工具（包括 Agent Builder、ChatKit、Connector Registry 和评估循环）。
* 在标准方面，OpenAI 推动了 **AGENTS.md** ([规范](https://agents.md/)) 并参与了 [**AAIF（Agentic AI 基金会）**](https://aaif.io/news/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation-aaif-anchored-by-new-project-contributions-including-model-context-protocol-mcp-goose-and-agents-md/)，同时推进其他生态系统标准如 [**模型上下文协议（MCP）**](https://modelcontextprotocol.io/) 和 [**Skills**](https://developers.openai.com/codex/skills)。对开发者的价值在于：随着生态系统在共享规范上趋于一致，可移植的智能体工具将更丰富，定制化集成需求将减少。

除了我们在智能体及相关标准方面的工作，我们还推出了 [Apps SDK](/apps-sdk)——这是一个开源框架，它扩展了模型上下文协议（MCP），使开发者能够在构建 MCP 服务器的同时创建用户界面，定义可在 ChatGPT 等客户端中运行的应用程序的逻辑和交互界面。

**其重要性在于**：开发者可以构建不那么紧密依赖于单一运行时或用户界面的智能体，并更轻松地将 OpenAI 驱动的智能体集成到异构系统中。

## 开放权重模型

除了托管 API，OpenAI 还发布了 **开放权重模型**，这些模型专为透明度、研究以及本地或自托管部署而设计，同时保持了强大的推理和指令遵循能力。

*   [**gpt-oss 120b 与 20b**](https://huggingface.co/collections/openai/gpt-oss) 推理模型，专为自主托管和本地部署设计。
*   [**gpt-oss-safeguard 120b 与 20b**](https://huggingface.co/collections/openai/gpt-oss-safeguard) 安全与策略模型，旨在与 gpt-oss 模型协同运行。

## 评估、调优与安全部署

*   [**Evals API**](https://platform.openai.com/docs/api-reference/evals/getRun) 用于支持评估驱动的开发。
*   [**强化微调**](https://platform.openai.com/docs/guides/reinforcement-fine-tuning) 利用可编程评分器进行。
*   [**监督微调 / 蒸馏**](https://platform.openai.com/docs/guides/distillation) 用于在通过更大模型验证任务后，将高质量性能迁移至更小、更经济的模型。
*   [**评分器**](https://platform.openai.com/docs/guides/graders) 与 [**提示优化器**](https://platform.openai.com/docs/guides/prompt-optimizer) 帮助团队更高效地运行“评估 → 改进 → 再评估”的闭环流程。

## 总结

在整个2025年，我们专注于几个一贯的主题，旨在让开发者更轻松地基于我们的平台进行构建和部署：

*   将规模化、可控的推理作为核心能力
*   统一、原生支持智能体的API接口
*   开放的构建模块与新兴的互操作性标准
*   跨文本、图像、音频、视频和文档的深度多模态支持
*   更强大的用于评估、调优和部署的生产工具

### 按任务推荐的模型（2025年底）

如果您正在启动新项目或对现有集成进行现代化改造，以下是为您的任务推荐的合理“默认选择”：

*   **通用型（文本+多模态）：**[**GPT-5.2**](https://openai.com/index/introducing-gpt-5-2/) 适用于对话、长上下文处理及多模态输入。
*   **深度推理/可靠性敏感型任务：**[**GPT-5.2 Pro**](https://platform.openai.com/docs/models/compare) 适用于规划任务及对质量要求高于额外计算成本的工作负载。
*   **编程与软件工程：**[**GPT-5.2-Codex**](https://platform.openai.com/docs/models/compare) 适用于代码生成、审查、仓库级推理及工具驱动的编码智能体。
*   **图像生成与编辑：**[**GPT Image 1.5**](https://openai.com/index/new-chatgpt-images-is-here/) 适用于高保真度图像生成及迭代编辑。
*   **实时语音：**[**gpt-realtime**](https://platform.openai.com/docs/guides/realtime) 适用于低延迟语音到语音转换及实时语音智能体。

有关最新可用性及层级划分，请参阅官方 [**模型对比页面**](https://platform.openai.com/docs/models/compare)。

这些更新为未来的发展奠定了基础。感谢您在2025年与我们共同构建——我们期待您在2026年创造的新成果。

## 链接与资源

*   [提示词优化器](https://platform.openai.com/chat/edit?models=gpt-5&optimize=true)
*   [模型对比](https://platform.openai.com/docs/models/compare)（当前名称、可用性及层级划分）
*   [智能体 SDK (Python)](https://openai.github.io/openai-agents-python/) 与 [智能体 SDK (TypeScript)](https://openai.github.io/openai-agents-js/)
*   [Codex 文档](https://developers.openai.com/codex/) 与 [Codex CLI GitHub](https://github.com/openai/codex)
*   [图像游乐场](https://platform.openai.com/playground/images)
*   [平台更新日志](https://platform.openai.com/docs/changelog)（发布内容与时间）
