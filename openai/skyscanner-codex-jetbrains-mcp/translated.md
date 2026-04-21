# 在Skyscanner通过JetBrains MCP为Codex注入超强动力

来源：https://developers.openai.com/blog/skyscanner-codex-jetbrains-mcp

---

_了解Skyscanner如何通过将OpenAI的Codex CLI与JetBrains IDE集成，让人工智能助手获得与人类开发者相同的调试和测试工具，从而大幅提升开发效率。_

在Skyscanner，我们始终致力于在不牺牲质量的前提下加速开发进程。过去几个月，我一直在日常工作中尝试将OpenAI的Codex作为结对编程伙伴。

特别之处在于？我通过JetBrains的模型上下文协议（MCP）服务器将Codex CLI接入JetBrains IDE：这实质上让人工智能能够感知并利用IDE的各项功能。这种集成带来了革命性的变化。本文将分享赋予Codex访问JetBrains工具的能力如何提升其问题解决技能，并加快我们的开发速度。

## 赋予Codex IDE上下文环境

通过[JetBrains MCP服务器](https://www.jetbrains.com/help/idea/mcp-server.html)使用Codex，意味着人工智能现在可以获取开发环境的丰富上下文信息——这些通常是它无法“看见”的内容。

借助JetBrains MCP，Codex能够向IDE请求额外上下文，例如：

  * [_查找文件问题_](https://www.jetbrains.com/help/idea/mcp-server.html#get_file_problems)：利用IntelliJ代码检查功能分析文件中的错误和警告，并返回具体问题详情（包含错误信息和位置）。
  * [_执行运行配置_](https://www.jetbrains.com/help/idea/mcp-server.html#execute_run_configuration)：运行预定义的运行配置（如单元测试、代码检查工具或格式化程序），并获取退出码和输出结果。

实践证明这极具威力——通过接入人类开发者在编写、编译和测试代码时依赖的相同反馈循环，Codex能够利用IDE的上下文环境更有效地检查和验证其输出，从而减少迭代时间。

### 加速错误捕获：实际案例演示

在我为使用Databricks Java SDK的代码编写错误处理单元测试时，我让Codex帮我模拟一个异常场景。它信心十足地生成了一行类似这样的Java代码：

    var stubError = new NotFound("dummy error");

乍一看这很合理——我们确实想模拟一个`NotFound`错误。但片刻之后，IntelliJ就用红色波浪线高亮标出了这行代码。

问题在于：Databricks SDK中的`NotFound`异常类并没有接收单个字符串参数的构造函数（你可以在Databricks SDK源码中看到：[NotFound.java](https://github.com/databricks/databricks-sdk-java/blob/4074f4e0ed2dc09f2feffddf14d7abdf20412119/databricks-sdk-java/src/main/java/com/databricks/sdk/core/error/platform/NotFound.java)）。换句话说，Codex建议的代码根本无法通过编译。

默认情况下，Codex不会意识到这个错误。它可能要等到尝试运行测试时才会发现问题。然而，借助JetBrains MCP集成，Codex立即捕捉到了这个错误。[在后台](https://github.com/Jack-Waller/.codex/blob/91acb8cf907bb91133cdf4d5e4e13253f6045873/AGENTS.md?plain=1#L100-L108)，Codex调用了IDE的`get_file_problems`工具来检查文件，该工具当即返回了编译问题（没有匹配的构造函数）。

如果没有MCP，流程很可能是：

  1. 生成代码
  2. 确定如何运行单元测试
  3. 运行单元测试（可能需要向用户申请执行权限）
  4. 读取并解析失败信息
  5. 尝试修复错误

而通过JetBrains MCP，这个循环变得紧凑得多：

  1. 生成代码
  2. 向JetBrains查询文件问题
  3. 直接修复IntelliJ报告的具体错误

这节省了时间和上下文切换，感觉就像与一位工程师结对编程，对方立刻指出：“啊，这个类没有那样的构造函数——它实际需要不同的参数。我马上修正。”

### 预定义测试与格式化

我享受的另一个优势是让Codex直接从IDE驱动我们现有的构建和测试工具。对于我们的大多数项目，我已经在IDE中定义了本地运行配置，比如运行测试、代码格式化和静态检查。通过JetBrains MCP，Codex能够按需发现并运行这些配置。

实际上，这减少了Codex理解如何运行这些功能所需的时间和上下文，帮助它更专注于原始问题。通过这一改变，我观察到Codex在运行测试、格式化或静态检查时不再出现卡顿。

因此，在我的[自定义代理指令](https://github.com/Jack-Waller/.codex/blob/91acb8cf907bb91133cdf4d5e4e13253f6045873/AGENTS.md?plain=1#L93-L108)中，我指示Codex在每次更改后运行测试、静态检查和格式化。

    ## 代码编辑指令

    完成编辑后

    - 使用jetbrains mcp（如果可用）查找任何问题
    - 运行格式化命令（如果可用）
    - 运行静态检查命令（如果可用）

我注意到Codex现在经常能自行解决问题，无需我干预。作为一名开发者，这感觉像是一个巨大的胜利：

  * 我不必在Codex每次修改后手动运行测试、静态检查和格式化。
  * 我不必将错误消息复制粘贴回聊天窗口。
  * Codex能快速、准确地获得其更改是否有效的反馈，减少了反馈循环的次数。

这让我有更多时间专注于手头的任务：交付高质量的可运行软件。

## 这对我们构建方式的意义

将Codex与JetBrains MCP集成，使我们的AI助手在开发过程中显著变得更强大、更可靠。我们观察到的一些实际好处包括：

* **更快的反馈循环**：Codex 能直接从集成开发环境获取编译错误和测试失败的即时反馈。
* **减少来回提示**：Codex 无需总是等待我运行代码并粘贴错误信息——它可以直接查询集成开发环境。
* **更高质量的建议**：由于 Codex 能同步看到集成开发环境中的内容，其修复方案更有可能在首次尝试时就通过编译和测试。
* **与现有工作流更契合**：Codex 无缝接入我们现有的工具链，而非另起炉灶。

总体而言，这使 Codex 从一个独立工具转变为开发生态系统中更深度融合的组成部分。

## 总结

对我们 Skyscanner 团队而言，核心认知很简单：上下文决定一切。独立的 Codex 固然强大，但具备集成开发环境感知能力的 Codex 则显著高效得多。这种上下文赋予 Codex 更深层的洞察力，使其能更快生成精准修复方案，也让我对其输出结果建立起更强的信任。

我们希望这个案例能激励更多开发者尝试此类集成方案。现在的体验已远非使用工具那么简单，更像是与一位能同步感知我们所见所想的 AI 结对编程伙伴展开协作。
