---

![作者头像](../images/what-actually-leaked-around-claude-code_00.png)

title: "What Actually Leaked From Claude Code This Time?"
source: "https://claudeai.dev/blog/3-what-actually-leaked"
translated: 2026-04-20
---

这次Claude Code泄露了什么？

"Claude Code源代码泄露"这句话最初听起来言过其实。

仔细查看社区证据后，这种怀疑需要更新。

这个故事不仅仅是提取提示或模糊的谣言。更可信的说法是：Claude Code npm包中的一个源映射暴露了内部源文件的路径，社区用它重建了比公共仓库大得多的代码库。

这比通常的社交媒体夸大更接近真正的源代码泄露。

核心主张

社区的主张很直接：

1. 发布的Claude Code npm包包含了JavaScript源映射。
2. 该源映射指向内部TypeScript源位置。
3. 这些源可以被获取和重建。
4. 结果以反编译或重建形式重新发布到GitHub。

如果这一链条准确的话，这不是"提示泄露"或"有人猜到了系统提示"。

这是一个具有源代码级后果的打包错误。

为什么社区认为这是真的

三个公开 artifacts 在这里很重要。

1. Reddit帖子

2026年3月30日，r/ClaudeAI上的一个帖子声称Claude Code源代码通过NPM上的.map文件泄露了。

这个具体机制很重要，因为源映射是一个已知的失败模式：它们可以暴露原始文件结构，可以揭示未混淆的标识符，并且取决于它们的构建和托管方式，它们可以指向原始源有效载荷。

2. Fried Rice的X帖子

社区引用的X帖子添加了更详细的主张版本：

- 据报道Claude Code的npm包随源映射一起发布
- 据说该映射引用了Anthropic管理存储上的zip存档
- 据说该存档包含比以前公开可见的大得多的内部源树

3. instructkr/claude-code仓库

最强的公开 artifacts 是GitHub仓库：https://github.com/instructkr/claude-code

这个仓库明确表明它是从泄露源映射重建的Claude Code，并声明：

- 原始npm包只暴露了一小部分打包文件
- 恢复的源树要大得多
- 数千个文件被重建
- 泄露暴露了内部实现细节、提示和功能工作

为什么这对开发者重要

实际教训是严酷而熟悉的：源映射是发布面的一部分。

对于AI产品，这种风险更糟，因为一次泄露可以同时暴露多层：

- 代码
- 提示
- 工具契约
- 功能标志
- 安全控制
- 未发布的产品工作

最终结论

查看Reddit帖子、X讨论和重建的GitHub仓库后，更强的结论是：

Claude Code"源代码泄露"故事似乎是实质性的真实，源映射角度是主要原因。

这个故事不仅仅人们猜测提示或过度解读公共代码。

更重要的是，Anthropic似乎通过npm发布了一个构建 artifacts，暴露了足够的源级信息，让社区重建了Claude Code的大部分内容。
