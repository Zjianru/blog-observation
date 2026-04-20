---
title: "How to Build a Plugin from Scratch in Cowork (2026 Guide)"
source: "https://claudeai.dev/blog/build-cowork-plugin-from-scratch"
date: "2026-02-28T00:00:00.000Z"
translated: 2026-04-20
---

# 如何在 Cowork 中从零开始构建插件（2026 指南）

如何在 Cowork 中从零开始构建插件（2026 指南）2026年2月28日 · 5 分钟阅读Claude DevClaude Dev如果你想 Cowork 为你完成实际工作，插件就是那个杠杆。截至 2026 年 2 月 28 日，我们现在有了一条清晰的官方路径：
*   Anthropic 于 2026 年 1 月 14 日推出 Cowork
*   自定义插件创建/分享功能于 2026 年 1 月 20 日宣布
*   企业插件目录更新于 2026 年 2 月 24 日发布
*   插件帮助文档于 2026 年 2 月 25 日更新
本指南结合了官方流程和社区用户的实践经验，帮助你从零开始构建第一个有用的插件。

## 一个 Cowork 插件应该做什么（在你接触 UI 之前）
一个好的首个插件应该解决一个具体、重复的任务。
*   **糟糕的首个插件想法**：“制定我的整个营销策略”
*   **优秀的首个插件想法**：
    *   “将会议记录转化为带有负责人和截止日期的每周行动项”
    *   “总结事件日志并输出风险分类表”
    *   “审查候选人资料文本并返回结构化评分卡”
在构建之前，写下这个一句话契约：
*   **输入**：你提供什么。
*   **输出**：插件每次必须返回什么。
如果你不能清晰地定义这一点，你的插件提示就会偏离方向。

## 步骤 1) 在 Cowork 中创建插件外壳
在 Cowork 中，打开插件区域并创建一个新插件。根据官方文档/帮助，你通常可以：
*   在 Cowork UI 中从零开始创建
*   从本地文件导入
*   从插件目录安装（针对现有插件）
对于你的首次构建，选择从零开始，以便理解每个设置。

## 步骤 2) 名称和描述：路由准确性从这里开始
社区构建者反复报告，插件选择在很大程度上受到清晰的命名和描述的影响。使用此格式：
*   **名称**：具体角色（例如：事件分类报告器）
*   **描述**：触发条件 + 范围（例如：当用户要求将原始日志中的运维事件按严重程度、负责人和下一步行动进行分类时使用。）
避免模糊的描述，如“通用助手插件”。
**为什么这很重要**：
*   Cowork 必须决定何时你的插件是相关的
*   模糊的描述会导致错误的插件激活或不激活

## 步骤 3) 编写严格的提示契约
你的插件指令应该读起来像一份生产运行手册。有效的最小结构：
*   角色和目标
*   必需输入
*   输出格式（固定部分/表格/类 JSON 结构）
*   决策规则和优先级
*   安全边界以及不确定时该怎么做
示例框架：
```
你是事件分类报告器。
目标：
- 将原始事件记录转化为优先级分类报告。
必需输入：
- incident_log
- service_name
- report_time
输出格式：
- 严重程度：P0/P1/P2/P3
- 影响摘要（最多 3 个要点）
- 疑似根本原因
- 立即执行的下一步行动
- 负责人建议
规则：
- 如果证据不足，明确说明不确定性。
- 切勿编造输入中不存在的指标。
- 如果关键上下文缺失，提出一个澄清性问题。
```
**社区经验**：简短、受限的提示优于冗长的“无所不能”提示。

## 步骤 4) 为可预测的输出而设计，而非“创造性”输出
如果一个插件是你工作流的一部分，一致性比风格更重要。实用检查：
*   队友能在 10 秒内浏览输出吗？
*   下游自动化能解析它吗？
*   格式在 5 个截然不同的测试输入中保持稳定吗？
如果不满足，请收紧指令并缩小范围。

## 步骤 5) 在分享前用真实边缘案例测试
不要只测试“理想路径”输入。至少运行这 5 项测试：
1.  干净、完整的输入
2.  缺少关键字段
3.  矛盾的数据
4.  非常长/嘈杂的输入
5.  超出插件范围的输入
对于第 5 种情况，预期行为应该是明确拒绝 + 重定向建议。

## 步骤 6) 在你的工作区中安全分享
官方的团队插件推出强调受控分享和工作区治理。在内部发布之前：
*   添加清晰的“何时使用 / 何时不使用”部分
*   在插件文档中添加示例输入/输出
*   设置所有者和维护期望
*   对提示进行版本控制（v0.1, v0.2 等）并附上简短的变更日志
这可以防止几周后出现“神秘插件”漂移。

## 步骤 7) 根据使用信号迭代
发布后，每周审查实际运行情况：
*   激活质量（在正确的时间被调用吗？）
*   输出修正率（用户重写结果的频率）
*   失败模式（缺少上下文、错误假设）
然后每次迭代只更新一个变量：
*   描述措辞
*   提示规则
*   输出模式
小的、受控的编辑胜过完全重写。

## 官方与社区指南：最应信任什么
使用此优先级顺序：
1.  官方 Cowork 产品 + 支持文档（功能行为、权限、发布）
2.  官方插件教程/参考（格式和实现细节）
3.  社区示例（对于边缘案例和实用启发式方法很有用）
社区帖子很有用，但随着 Cowork 的发展，它们可能很快过时。

## 最终要点
你的第一个 Cowork 插件应该是**枯燥的、具体的、可靠的**。如果你能做到这三点：
*   清晰的触发描述
*   严格的输出契约
*   严谨的测试用例
……你将很快获得真正的杠杆作用，并且你的第二个插件会容易得多。

## 来源（于 2026-02-28 核对）
**官方**
*   Anthropic: Introducing Cowork (2026-01-14) https://www.anthropic.com/news/introducing-cowork
*   Anthropic: Create and share plugins in Cowork (2026-01-20) https://www.anthropic.com/news/create-and-share-plugins-in-cowork
*   Anthropic: Cowork and plugins for enterprises and financial services (2026-02-24) https://www.anthropic.com/news/cowork-and-plugins-for-enterprises-and-financial-services
*   Claude Support: Use plugins in Cowork (updated 2026-02-25) https://support.claude.com/en/articles/11811905-use-plugins-in-cowork
*   Claude Code docs: How to build a plugin from scratch in Cowork https://code.claude.com/tutorials/plugins/how-to-build-a-plugin-from-scratch-in-cowork

**社区**
*   Reddit (r/ClaudeAI): “I want to create custom skills for Cowork, but they don't work” https://www.reddit.com/r/ClaudeAI/comments/1ics9f1/i_want_to_create_custom_skills_for_cowork_but/
*   YouTube (Zinho): “Claude COWORK Plugins Just Changed EVERYTHING! NEW Plugin Directory Breakdown” https://www.youtube.com/watch?v=ftQZiP22TF4
*   Medium (Dong Liang): “The Fork in the Road: Claude Code vs Cowork…” (2026-02-26) https://medium.com/@dongliang_47217/the-fork-in-the-road-claude-code-vs-cowork-which-one-really-fits-your-ai-workflow-in-2026-826c8860748d

**标签**：ClaudeCoworkPluginsTutorialAI AgentWorkflow
