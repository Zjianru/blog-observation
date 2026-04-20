使用 JetBrains MCP 为 Skyscanner 的 Codex 提速

How Skyscanner integrated Codex CLI with JetBrains IDEs to speed up debugging, testing, and development workflows.

作者：Jack Waller（Skyscanner 软件工程师）

了解 Skyscanner 如何通过将 OpenAI 的 Codex CLI 与 JetBrains IDE 集成来为其 AI 助手提供与人类开发者相同的调试和测试工具，从而实现提速。

在 Skyscanner，我们一直在寻找在不牺牲质量的情况下加速开发的方法。在过去的几个月里，我一直在尝试将 OpenAI 的 Codex 作为我日常工作流程中的结对程序员。

诀窍是什么？我使用 JetBrains 的模型上下文协议（MCP）服务器将 Codex CLI 连接到 JetBrains 的 IDE：从本质上让 AI 查看和使用 IDE 的功能。这种集成改变了游戏规则。在这篇文章中，我将分享赋予 Codex 访问 JetBrains 工具的权限如何提高了它的问题解决能力并加速了我们的开发。

赋予 Codex IDE 的上下文

使用 JetBrains MCP 服务器与 Codex 合作意味着 AI 现在可以挖掘我的开发环境的丰富上下文——它通常不会"看到"的东西。

通过 JetBrains MCP，Codex 可以向 IDE 请求额外上下文，例如：

查找文件问题：使用 IntelliJ 检查分析文件的错误和警告，并返回确切的问题（带有错误消息和位置）。
执行运行配置：运行预定义的运行配置（如单元测试、linter 或格式化程序）并检索退出代码和输出。

这已被证明非常强大——通过利用人类开发者在编写、编译和测试代码时依赖的相同反馈循环，Codex 可以使用 IDE 的上下文更有效地检查和验证其输出，减少迭代时间。

更快地发现错误：一个真实世界的例子

当我为使用 Databricks Java SDK 的代码编写错误处理的单元测试时，我提示 Codex 帮助我 stub 一个异常场景。它自信地生成了一行看起来像这样的 Java 代码：

var stubError = new NotFound("dummy error");

乍一看，这看起来很合理——我们想要模拟一个 NotFound 错误。但片刻之后，IntelliJ 用一个大的红色下划线突出显示了那一行。

问题：Databricks SDK 中的 NotFound 异常类没有接受单个字符串参数的构造函数（你可以在 Databricks SDK 源代码中看到：NotFound.java）。换句话说，Codex 建议的代码永远不会编译。

默认情况下，Codex 不会知道这个错误。它可能只会在稍后尝试运行测试时才意识到有问题。然而，由于 JetBrains MCP 集成，Codex 立即注意到了错误。在幕后，Codex 调用了 IDE 的 get_file_problems 工具来检查文件，该工具立即返回了编译问题（没有匹配的构造函数）。

如果没有 MCP，可能的流程是：

生成代码
确定如何运行单元测试
运行单元测试（可能需要将命令升级给用户）
阅读和解析失败消息
尝试修复错误

使用 JetBrains MCP，那个循环更加紧密：

生成代码
向 JetBrains 请求文件问题
修复 IntelliJ 报告的确切错误

这节省了时间和上下文，感觉非常像与一位工程师结对编程，他立即说："啊，那个类没有这样的构造函数——它实际上需要不同的东西。让我快速修复它"。

预定义的测试和格式化

我享受的另一个优势是让 Codex 直接从 IDE 中驱动我们现有的构建和测试工具。对于我们大多数项目，我已经在 IDE 中定义了本地运行配置，例如运行测试、格式化和 linting。使用 JetBrains MCP，Codex 可以按需发现和运行这些配置。

在实践中，这减少了 Codex 找出如何运行此功能所需的时间和上下文，帮助它保持对原始问题的专注。通过这个改变，我观察到 Codex 在运行测试、格式化或 linting 时不再踉跄。

在我的自定义代理指令中，因此我指示 Codex 在每次更改后运行测试、linting 和格式化。

## 代码编辑指令

![](images/skyscanner-codex-jetbrains-mcp_00.png)

完成编辑后

- 使用 jetbrains mcp（如果有）查找任何问题
- 如果有格式化命令，运行格式命令
- 如果有 lint 命令，运行 lint 命令

我注意到 Codex 现在经常自己解决问题，而无需我干预。作为开发者，这感觉是一个巨大的胜利：

每次 Codex 更改某些内容时，我不必手动运行测试、linting 和格式化。
我不必每次都将错误消息复制粘贴回聊天中。
Codex 可以快速、精确地了解其更改是否实际有效，减少反馈循环次数。

这给了我更多时间专注于手头的任务：交付高质量的工作软件。

这对我们的构建方式意味着什么

将 Codex 与 JetBrains MCP 集成使我们的 AI 助手在我们的开发过程中变得更加能干和可靠。我们看到的一些实际好处是：

更快的反馈循环：Codex 从 IDE 获得关于编译错误和测试失败的即时反馈。
更少的来回提示：Codex 不必总是等待我运行某些东西并粘贴错误消息——它可以直接查询 IDE。
更高质量的建议：因为 Codex 可以看到 IDE 看到的内容，它的修复更有可能在第一次尝试时编译并通过测试。
与现有工作流程更好的一致性：Codex 插入我们现有的工具，而不是发明自己的。

总的来说，它将 Codex 从一个独立工具变成了我们开发生态系统中更集成的部分。

总结

对于我们 Skyscanner 的人来说，关键见解很简单：上下文就是一切。单独的 Codex 很强大，但具有 IDE 意识的 Codex 更加有效。这种上下文让 Codex 获得更多洞察，使其能够更快地产生准确的修复，并进一步提高我对其输出的信任。

我们希望我们的故事能够激励其他人尝试这些集成。它真的感觉不像使用工具，而更像是与一个可以看到我们所看到的 AI 结对程序员合作。
