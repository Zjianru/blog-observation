---

![作者头像](../images/conway-timeline-how-anthropic-is-building-always-on-agents_00.png)

title: "Conway Timeline: How Anthropic Is Building Always-On Agents"
source: "https://claudeai.dev/blog/2-conway-timeline"
translated: 2026-04-20
---

Conway时间线：Anthropic如何构建常驻代理

关于Conway最重要的一点是：

Conway不是Anthropic正式发布的产品。

今天存在的是以下内容的混合：

- Anthropic围绕Cowork、Dispatch、计算机使用、计划任务和自动模式进行的正式发布
- 显示这些部分如何组合在一起的当前帮助中心文档
- 2026年4月1日的第三方报告，揭露了一个名为Conway的未发布内部环境

如果你只看泄露，你会错过架构。如果你只看正式发布，你会错过Anthropic似乎要去的地方。

技术故事是两者的结合。

简短回答

从系统角度来看，Anthropic明显正在走向常驻代理模型。

不是因为Conway已被宣布，而是因为已发布的产品堆栈已经包含大部分所需原语：

- 跨设备跟随你的持久线程
- 具有本地文件访问权限的桌面运行时
- 计划执行
- 当直接集成缺失时的计算机使用
- 子代理协调
- 更安全的长期运行权限模式
- 通过Dispatch实现的移动端到桌面端任务传递

Conway之所以重要，是因为它似乎将这些想法打包到一个更明确的常驻代理环境中。

为什么Conway在技术上有意义

如果剥离产品名称，Anthropic已经拥有常驻代理系统所需的大部分组件。

1. 持久控制线程

Dispatch提供在设备变化中存活的用户面对线程。

2. 专业运行时

Anthropic有两个不同的执行面：

- Claude Code用于开发工作
- Cowork用于更广泛的桌面知识工作

3. 超越前台聊天的触发

计划任务和Dispatch将模型推至响应性聊天之外。

4. 通过计算机使用进行回退执行

直接集成始终比屏幕控制好。Anthropic在计算机使用文档中明确表示：Claude应首先使用连接器，然后是浏览器自动化，最后是直接屏幕交互。

5. 长期运行的治理

自动模式是Anthropic知道常驻代理需要与前台助手不同权限架构的第一个可见标志。

最终结论

如果你问"Anthropic是否正式发布了Conway？"答案是否定的。

如果你问"Anthropic是否明显在构建常驻代理架构？"答案是肯定的。

官方产品轨迹已经显示方向：

- Cowork建立了桌面代理运行时
- Dispatch建立了跨设备持久线程
- 计划任务建立了基于时间的自动化
- 计算机使用建立了回退执行器层
- 自动模式建立了更安全的长期运行执行
- 报告的Conway环境添加了实例、Webhooks、扩展和通知的缺失语言

这就是真正的技术故事。

Conway之所以重要，不是因为它证明Anthropic完成了常驻代理。而是因为它使Anthropic的产品轨迹更容易看到。
