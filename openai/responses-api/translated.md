
![](../images/responses-api_00.png)

为什么我们构建了 Responses API

How the Responses API unlocks persistent reasoning, hosted tools, and multimodal workflows for GPT-5.

作者：Steve Coffey、Prashant Mital

随着 GPT-5 问世，我们想提供更多关于最佳集成方式、Responses API 以及为什么 Responses 是为推理模型和代理未来量身定制的背景。

每一代 OpenAI API 都围绕着同一个问题构建：对于开发者来说，与模型对话的最简单、最强大的方式是什么？

我们的 API 设计始终由模型本身的工作方式引导。最初的 /v1/completions 端点很简单，但有限制：你给模型一个提示，它只会完成你的想法。通过少样本提示等技术，开发者可以尝试引导模型做输出 JSON 和回答问题等事情，但这些模型比我们今天习惯的要弱得多。

然后 RLHF、ChatGPT 和后训练时代来临。突然间，模型不再只是完成你写了一半的文章——它们像对话伙伴一样响应。为了跟上，我们构建了 /v1/chat/completions（ famously在一个周末内）。通过给予 system、user、assistant 等角色，我们提供了脚手架来快速构建具有自定义指令和上下文的聊天界面。

我们的模型越来越强大。很快，它们开始看、听、说。2023 年底的函数调用被证明是我们最受欢迎的功能之一。大约在同一时间，我们在 beta 中推出了 Assistants API：我们首次尝试使用 code interpreter 和 file search 等托管工具的完全代理界面。一些开发者喜欢它，但由于 API 设计限制且相对于 Chat Completions 难以采用，它从未获得大规模采用。

到 2024 年底，很明显我们需要统一：像 Chat Completions 一样易于接近，像 Assistants 一样强大，但也专为多模态和推理模型构建。进入 /v1/responses。

/v1/responses 是一个代理循环

Chat Completions 给你一个简单的基于轮次的聊天界面。Responses 反而给你一个用于推理和行动的结构化循环。把它想象成与侦探合作：你给他们证据，他们调查，他们可能咨询专家（工具），最后他们报告。侦探在步骤之间保留私人笔记（推理状态），但从不将它们交给客户端。

这就是推理模型真正闪耀的地方：Responses 在这些轮次之间保留模型的推理状态。在 Chat Completions 中，推理在调用之间被丢弃，就像侦探每次离开房间时忘记线索一样。Responses 保持笔记本打开；逐步思考过程实际上会延续到下一轮。这体现在基准测试中（TAUBench +5%）以及更高效的缓存利用率和延迟。

Responses 还可以发出多个输出项：不仅是模型说的，还有它做的。你获得收据——工具调用、结构化输出、中间步骤。这就像同时获得完成的论文和草稿数学。对调试、审计和构建更丰富的 UI 很有用。

Chat completions 每个请求发出一 message。消息的结构是有限的：消息和函数调用哪个先来？

Responses发出一列多态 Items。模型采取的操作顺序是清晰的。作为开发者，你可以选择显示、记录或完全忽略哪些。

使用托管工具向上堆叠

在函数调用早期，我们注意到一个关键模式：开发者使用模型来调用 API，也搜索文档存储以引入外部数据源——现在称为 RAG。但如果你是一个刚起步的开发者，从头开始构建检索管道是一项艰巨且昂贵的努力。使用 Assistants，我们引入了第一个托管工具：file_search 和 code_interpreter，允许模型进行 RAG 并编写代码来解决你要求它的问题。在 Responses 中，我们走得更远，添加了网络搜索、图像生成和 MCP。而且因为工具执行通过 code interpreter 或 MCP 等托管工具在服务器端发生，你不会通过你自己的后端反弹每个调用，确保更好的延迟和往返成本。

安全地保留推理

那么为什么要这么麻烦地混淆模型的原始思维链（CoT）？为什么不直接暴露 CoT 让客户端处理它们类似于其他模型输出？简短的回答是暴露原始 CoT 有很多风险：例如幻觉、在最终响应中不会产生的有害内容，对 OpenAI 来说，打开了竞争风险。

当我们去年晚些时候发布 o1-preview 时，我们的首席科学家 Jakub Pachocki 在我们的博客中写道：

我们相信隐藏的思维链为监控模型提供了独特的机会。假设它是忠实和清晰的，隐藏的思维链允许我们"阅读模型的思想"并理解其思维过程。例如，将来我们可能希望监控思维链中操纵用户的迹象。然而，为了使其工作，模型必须自由地以未更改的形式表达其思想，因此我们不能将任何策略合规性或用户偏好训练到思维链上。我们也不想将未对齐的思维链直接显示给用户。

Responses 通过以下方式解决这一问题：

在内部保留推理，加密且对客户端隐藏。
允许通过 previous_response_id 或推理项目安全继续，而不暴露原始 CoT。
为什么 /v1/responses 是最好的构建方式

我们设计 Responses 是为了有状态、多模态和高效。

代理工具使用：Responses API 使用 File Search、Image Gen、Code Interpreter 和 MCP 等工具使代理工作流程变得超级容易。
默认有状态。对话和工具状态自动跟踪。这使得推理和多轮工作流程变得非常简单。通过利用保留的推理，GPT-5 通过 Responses 集成在 TAUBench 上得分比 Chat Completions 高 5%。
从基础上是多模态的。文本、图像、音频、函数调用——所有都是一等公民。我们没有将模态螺栓固定在文本 API 上；从第一天起我们就设计了足够卧室的房子。
更低成本，更好性能。内部基准测试显示与 Chat Completions 相比，缓存利用率好 40-80%。这意味着更低的延迟和更低的成本。
更好的设计：我们从 Chat Completions 和 Assistants API 中学到了很多东西，并在 ResponsesAPI 和 SDK 中进行了许多小的生活质量改进，包括
语义流事件。
内部标记的多态性。
SDK 中的 output_text 助手（不再是 choices.[0].message.content）。
更好地组织多模态和推理参数。
Chat Completions 怎么样？

Chat Completions 不会消失。如果它适合你，继续使用它。但如果你想要推理持久化、感觉原生的多模态交互，以及不需要胶带的代理循环——Responses 是前进的方向。

展望未来

正如 Chat Completions 取代了 Completions，我们期望 Responses 成为开发者使用 OpenAI 模型构建的默认方式。在你需要简单时简单，在你想要强大时强大，足够灵活以处理下一个范式抛给我们的任何东西。

这就是我们未来几年将构建的 API。
