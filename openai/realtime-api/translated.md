# Realtime API 开发者笔记

来源：https://developers.openai.com/blog/realtime-api

---

我们最近[宣布](https://openai.com/index/introducing-gpt-realtime/)了最新的语音到语音模型 `gpt-realtime`，同时 Realtime API 和一系列新 API 功能也已全面开放。Realtime API 和语音到语音（s2s）模型现已正式发布（GA），在模型质量、可靠性和开发者体验方面均有重大改进。

虽然您可以在[文档](https://platform.openai.com/docs/guides/realtime)和[API 参考](https://platform.openai.com/docs/api-reference/realtime)中了解新的 API 功能，但我们想重点介绍一些您可能错过的内容，并提供使用指南。如果您正在集成 Realtime API，希望这些笔记能对您有所帮助。

## 模型改进

新模型包含多项改进，旨在更好地支持生产级语音应用。本文主要关注 API 变更。为了更好地理解和使用该模型，我们推荐阅读[发布博客文章](https://openai.com/index/introducing-gpt-realtime/)和[实时提示指南](/cookbook/examples/realtime_prompting_guide)。不过，我们也会指出一些具体细节。

使用该模型的几点关键建议：

  * 在[实时交互界面](https://platform.openai.com/playground/realtime)中尝试提示词。
  * 使用 `marin` 或 `cedar` 语音以获得最佳的助手语音质量。
  * 为新模型重写提示词。由于指令遵循能力的改进，具体的指令现在效果更强。
    * 例如，一个提示词说“当 Y 发生时，总是说 X”，旧模型可能将其视为模糊的指导，而新模型可能会在意想不到的情况下严格遵守它。
    * 注意您提供的具体指令。假设指令会被遵循。

## API 结构变更

随着 GA 版本的发布，我们更新了 Realtime API 的结构，这意味着现在存在一个 Beta 接口和一个 GA 接口。我们建议客户端迁移到 GA 接口进行集成，因为它提供了新功能，而 Beta 接口最终将被弃用。

迁移所需更改的完整列表可在 [Beta 到 GA 迁移文档](https://platform.openai.com/docs/guides/realtime#beta-to-ga-migration)中找到。

您可以通过 Beta 接口访问新的 `gpt-realtime` 模型，但某些功能可能不受支持。更多详情见下文。

### 功能可用性

Realtime API GA 版本包含许多新功能。其中一些功能在旧模型上可用，一些则不可用。

功能| GA 模型| Beta 模型
---|---|---
图像输入| ✅| ❌
长上下文| ✅| ✅
异步函数调用| ✅| ❌
提示词| ✅| ✅
MCP| ✅ _与异步 FC 配合最佳_|  ✅ _无异步 FC 时功能有限*_
音频令牌 → 文本| ✅| ❌
欧盟数据驻留| ✅| ✅ _仅限 06-03 版本_
SIP| ✅| ✅
空闲超时| ✅| ✅

*由于 Beta 模型缺乏异步函数调用，没有输出的待处理 MCP 工具调用可能无法被模型很好地处理。我们建议将 GA 模型与 MCP 配合使用。

### 温度参数变更

GA 接口已将 `temperature` 作为模型参数移除，而 Beta 接口将温度限制在 `0.6 - 1.2` 的范围内，默认值为 `0.8`。

你可能会问：“为什么用户不能随意设置温度参数，比如通过调低温度来让回答更确定呢？”答案是，对于这种模型架构，温度参数的作用方式有所不同，而将温度设置为建议的 `0.8` 几乎总能给用户带来最佳体验。

根据我们的观察，目前无法通过调低温度参数使音频响应变得确定，而更高的温度则会导致音频异常。我们建议通过调整提示词来尝试控制模型行为的这些维度。

## 新功能

除了从测试版到正式版的变更外，我们还为 Realtime API 新增了多项功能。

所有功能均在[文档](https://platform.openai.com/docs/guides/realtime)和[API 参考](https://platform.openai.com/docs/api-reference/realtime)中详细说明，但这里我们将重点介绍在集成和迁移过程中如何理解这些新功能。

### 对话空闲超时

对于某些应用场景，用户长时间无输入可能不符合预期。想象一下电话通话——如果听不到对方的声音，我们通常会询问对方状态。可能是模型漏听了用户发言，也可能是用户不确定模型是否仍在说话。我们新增了一项功能，可自动触发模型说出类似“您还在吗？”的询问。

通过在语音活动检测（`server_vad`）的轮次检测设置中配置 `idle_timeout_ms` 即可启用此功能。超时计时将从最后一个模型响应的音频播放结束后开始计算——即超时值设定为 `response.done` 时间加上音频播放时长再加上超时时间。如果在该时段内未触发语音活动检测，则会激活超时机制。

超时触发时，服务器会发送 [`input_audio_buffer.timeout_triggered`](https://platform.openai.com/docs/api-reference/realtime-server-events/input_audio_buffer/timeout_triggered) 事件，随后将空音频片段提交至对话历史记录并触发模型响应。提交空音频能让模型有机会检测语音活动检测是否失效，以及相关时段内是否存在用户话语。

客户端可通过以下方式启用此功能：

    {
      "type": "session.update",
      "session": {
        "type": "realtime",
        "instructions": "你是一个乐于助人的助手。",
        "audio": {
          "input": {
            "turn_detection": {
              "type": "server_vad",
              "idle_timeout_ms": 6000
            }
          }
        }
      }
    }

### 长对话与上下文处理

我们调整了 Realtime API 处理长会话的方式。需要注意以下几点：

  * Realtime 会话时长现延长至 60 分钟（原为 30 分钟）
  * `gpt-realtime` 模型的令牌窗口为 32,768 个令牌，响应最多可消耗 4,096 个令牌，这意味着模型最大输入为 28,672 个令牌
  * 会话指令与工具描述的最大长度为 16,384 个令牌
  * 当会话达到 28,672 个令牌时，服务将自动截断（丢弃）部分消息，但此行为可配置
  * 正式版服务会在有转录文本时自动丢弃部分音频令牌以节省令牌占用

#### 配置截断设置

当对话上下文窗口达到令牌限制时，Realtime API 会自动开始从会话开头（最旧的消息）截断（丢弃）消息。您可以通过设置 `"truncation": "disabled"` 来禁用此截断行为，这样当输入令牌过多时，系统会抛出错误。不过，截断功能很有用，因为即使输入大小超出模型处理能力，会话仍能继续。Realtime API 不会对被丢弃的消息进行摘要或压缩，但您可以自行实现。

截断的一个负面影响是，改变对话开头的消息会破坏[令牌提示缓存](https://platform.openai.com/docs/guides/prompt-caching)。提示缓存的工作原理是识别提示前缀中完全相同的匹配内容。在后续的每一轮对话中，只有未更改的令牌会被缓存。当截断改变了对话开头时，它会减少可缓存的令牌数量。

我们已实施一项功能来减轻这种负面影响：每当发生截断时，系统会进行超出必要范围的截断。将保留比例设置为 `0.8`，即可截断 20% 的上下文窗口，而不是仅截断刚好使输入令牌数低于上限的部分。这样做的思路是**一次性**截断**更多**的上下文窗口，而不是每次只截断一点点，从而减少缓存被破坏的频率。这种缓存友好方法可以降低达到输入限制的长会话的成本。

    {
      "type": "session.update",
      "session": {
        "truncation": {
          "type": "retention_ratio",
          "retention_ratio": 0.8
        }
      }
    }

### 异步函数调用

Responses API 会在函数调用后立即强制返回函数响应，而 Realtime API 允许客户端在函数调用挂起时继续会话。这种延续有利于用户体验，使实时对话能够自然进行，但模型有时会幻觉出不存在的函数响应内容。

为了缓解这个问题，GA Responses API 添加了占位符响应，其内容经过我们在实验中的评估和调整，以确保模型即使在等待函数响应时也能优雅运行。如果您向模型询问函数调用的结果，它会回答类似“我还在等待结果”的内容。此功能已为新模型自动启用——您无需进行任何更改。

### 欧盟数据驻留

欧盟数据驻留现已专门针对 `gpt-realtime-2025-08-28` 和 `gpt-4o-realtime-preview-2025-06-03` 模型提供支持。数据驻留必须为组织明确启用，并通过 `https://eu.api.openai.com` 访问。

### 追踪

Realtime API 将追踪日志记录到[开发者控制台](https://platform.openai.com/logs?api=traces)，记录实时会话期间的关键事件，有助于调查和调试。作为 GA 的一部分，我们推出了几种新的事件类型：

  * 会话更新（当 `session.updated` 事件发送到客户端时）
  * 输出文本生成（针对模型生成的文本）

### 托管提示

您现在可以使用[Realtime API的提示功能](https://platform.openai.com/docs/guides/realtime-models-prompting#update-your-session-to-use-a-prompt)，通过引用可独立编辑的提示来简化应用代码。提示既包含指令也包含会话配置，例如语音端点检测设置。

您可以在[实时交互界面](https://platform.openai.com/audio/realtime)中创建提示，根据需要进行迭代和版本管理，随后客户端即可通过ID引用该提示，示例如下：

    {
      "type": "session.update",
      "session": {
        "type": "realtime",
        "prompt": {
          "id": "pmpt_123", // 您存储的提示ID
          "version": "89", // 可选：锁定特定版本
          "variables": {
            "city": "Paris" // 提示中使用的示例变量
          }
        },
        // 仍可直接设置会话字段；若与提示字段冲突，这些设置将覆盖提示配置：
        "instructions": "请清晰简洁地表达。执行操作前先确认理解。"
      }
    }

如上述示例所示，若提示设置与会话传入的其他配置发生重叠，会话配置将优先生效。这意味着客户端既可采用提示的配置，也可在会话时动态调整配置。

### 旁路连接

Realtime API允许客户端通过WebRTC或SIP直接连接至API服务器。但您很可能希望将工具调用及其他业务逻辑保留在应用服务器上，以确保逻辑的私密性和客户端无关性。

通过旁路控制通道连接，可将工具调用、业务逻辑等敏感细节安全地部署在服务器端。我们现在为SIP和WebRTC连接均提供了旁路连接方案。

旁路连接意味着同一实时会话将同时保持两个活跃连接：一个来自用户客户端，另一个来自您的应用服务器。服务器连接可用于监控会话状态、更新指令以及响应工具调用。

更多信息请参阅[旁路连接文档](https://platform.openai.com/docs/guides/realtime-server-controls)。

## 开始构建

希望以上说明能帮助您理解正式发布的Realtime API及新版实时模型的更新要点。

掌握最新框架后，请查阅[实时功能文档](https://platform.openai.com/docs/guides/realtime)，开始构建语音助手、建立连接或尝试实时模型提示功能。