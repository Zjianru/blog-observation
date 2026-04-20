# AI 开发者博客观察

本项目用于学习 AI Agent 工程实践，从三大来源持续跟踪、翻译和整理一手技术文章。

**更新日期：** 2026-04-20
**文章总数：** 51 篇（Anthropic 23 + OpenAI 18 + Claude AI Dev 10）

---

## 目录导航

| 来源 | 文章数 | 简介 |
|------|--------|------|
| [Anthropic Engineering](#anthropic-engineering-23篇) | 23 | 模型评测、Harness 设计、Agent 工具、工程实践 |
| [OpenAI Developers](#openai-developers-18篇) | 18 | Codex、Agents SDK、Responses API、Eval 系统 |
| [Claude AI Dev](#claude-ai-dev-10篇) | 10 | Claude Code、Skill 系统、Agent 工作流、泄漏分析 |

---

## Anthropic Engineering (23篇)

Anthropic 官方工程博客，主题覆盖 Agent 评测、Harness 设计、工具使用和工程实践。

| # | 文章（English) | 文章（中文） |
|---|---------------|-------------|
| 01 | [Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise) | [基础设施噪声如何影响 Agent 评测](anthropic/translated/infrastructure-noise.md) |
| 02 | [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents) | [扩展 Managed Agents：解耦大脑与双手](anthropic/translated/managed-agents.md) |
| 03 | [Claude Code auto mode: a safer way to skip permissions](https://www.anthropic.com/engineering/claude-code-auto-mode) | [Claude Code 自动模式：跳过权限的安全方式](anthropic/translated/claude-code-auto-mode.md) |
| 04 | [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | [长运行应用的 Harness 设计](anthropic/translated/harness-design-long-running-apps.md) |
| 05 | [Eval awareness in Claude Opus 4.6's BrowseComp performance](https://www.anthropic.com/engineering/eval-awareness-browsecomp) | [Eval 感知与 Claude Opus 4.6 的 BrowseComp 表现](anthropic/translated/eval-awareness-browsecomp.md) |
| 06 | [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) | [用一群并行 Claudes 构建 C 编译器](anthropic/translated/building-c-compiler.md) |
| 07 | [Designing AI-resistant technical evaluations](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations) | [设计抗 AI 技术评测](anthropic/translated/AI-resistant-technical-evaluations.md) |
| 08 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | [揭开 AI Agent 评测的神秘面纱](anthropic/translated/demystifying-evals-for-ai-agents.md) |
| 09 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | [长运行 Agent 的有效 Harness](anthropic/translated/effective-harnesses-for-long-running-agents.md) |
| 10 | [Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use) | [在 Claude 开发者平台上引入高级工具使用](anthropic/translated/advanced-tool-use.md) |
| 11 | [Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp) | [MCP 代码执行：构建更高效的 Agent](anthropic/translated/code-execution-with-mcp.md) |
| 12 | [Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/claude-code-sandboxing) | [超越权限提示：让 Claude Code 更安全更自主](anthropic/translated/claude-code-sandboxing.md) |
| 13 | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | [用 Agent Skills 为 Agent 装备现实世界能力](anthropic/translated/equipping-agents-for-the-real-world-with-agent-skills.md) |
| 14 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | [AI Agent 的有效上下文工程](anthropic/translated/effective-context-engineering-for-ai-agents.md) |
| 15 | [A postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) | [三个近期问题的复盘](anthropic/translated/a-postmortem-of-three-recent-issues.md) |
| 16 | [Writing effective tools for agents — with agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | [用 Agent 写有效的 Agent 工具](anthropic/translated/writing-tools-for-agents.md) |
| 17 | [Desktop Extensions: One-click MCP server installation for Claude Desktop](https://www.anthropic.com/engineering/desktop-extensions) | [桌面扩展：一键安装 MCP 服务器](anthropic/translated/desktop-extensions.md) |
| 18 | [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | [我们如何构建多 Agent 研究系统](anthropic/translated/multi-agent-research-system.md) |
| 19 | [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices) | [Claude Code：Agent 编程最佳实践](anthropic/translated/claude-code-best-practices.md) |
| 20 | [The "think" tool: Enabling Claude to stop and think in complex tool use situations](https://www.anthropic.com/engineering/claude-think-tool) | ["Think" 工具：在复杂工具使用场景中让 Claude 停下来思考](anthropic/translated/claude-think-tool.md) |
| 21 | [Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet](https://www.anthropic.com/engineering/swe-bench-sonnet) | [用 Claude 3.5 Sonnet 提升 SWE-bench 基准](anthropic/translated/swe-bench-sonnet.md) |
| 22 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | [构建有效的 Agent](anthropic/translated/building-effective-agents.md) |
| 23 | [Introducing Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) | [介绍 Contextual Retrieval](anthropic/translated/contextual-retrieval.md) |

---

## OpenAI Developers (18篇)

OpenAI 开发者博客，主题覆盖 Codex、Agents SDK、Responses API 和实际应用案例。

| # | 文章（English) | 文章（中文） |
|---|---------------|-------------|
| 01 | [How Perplexity Brought Voice Search to Millions Using the Realtime API](https://developers.openai.com/blog/realtime-perplexity-computer) | [Perplexity 如何用 Realtime API 将语音搜索带给数百万用户](openai/translated/realtime_perplexity_computer.zh.md) |
| 02 | [Designing delightful frontends with GPT-5.4](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4) | [用 GPT-5.4 设计出色的前端](openai/translated/designing_delightful_frontends_with_gpt_5_4.zh.md) |
| 03 | [From prompts to products: One year of Responses](https://developers.openai.com/blog/one-year-of-responses) | [从提示到产品：Responses 的一年](openai/translated/one_year_of_responses.zh.md) |
| 04 | [Using skills to accelerate OSS maintenance](https://developers.openai.com/blog/skills-agents-sdk) | [用 Skills 加速开源维护](openai/translated/skills_agents_sdk.zh.md) |
| 05 | [Building frontend UIs with Codex and Figma](https://developers.openai.com/blog/building-frontend-uis-with-codex-and-figma) | [用 Codex 和 Figma 构建前端 UI](openai/translated/building_frontend_uis_with_codex_and_figma.zh.md) |
| 06 | [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) | [用 Codex 运行长时任务](openai/translated/run_long_horizon_tasks_with_codex.zh.md) |
| 07 | [Shell + Skills + Compaction: Tips for long-running agents](https://developers.openai.com/blog/skills-shell-tips) | [Shell + Skills + 压缩：长运行 Agent 技巧](openai/translated/skills_shell_tips.zh.md) |
| 08 | [15 lessons learned building ChatGPT Apps](https://developers.openai.com/blog/15-lessons-building-chatgpt-apps) | [构建 ChatGPT 应用学到的 15 条经验](openai/translated/15_lessons_building_chatgpt_apps.zh.md) |
| 09 | [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | [用 Evals 系统化测试 Agent Skills](openai/translated/eval_skills.zh.md) |
| 10 | [Supercharging Codex with JetBrains MCP at Skyscanner](https://developers.openai.com/blog/skyscanner-codex-jetbrains-mcp) | [Skyscanner 用 JetBrains MCP 强化 Codex](openai/translated/skyscanner_codex_jetbrains_mcp.zh.md) |
| 11 | [OpenAI for Developers in 2025](https://developers.openai.com/blog/openai-for-developers-2025) | [2025 年 OpenAI 开发者回顾](openai/translated/openai_for_developers_2025.zh.md) |
| 12 | [Updates for developers building with voice](https://developers.openai.com/blog/updates-audio-models) | [语音开发者更新](openai/translated/updates_audio_models.zh.md) |
| 13 | [What makes a great ChatGPT app](https://developers.openai.com/blog/what-makes-a-great-chatgpt-app) | [什么造就一个优秀的 ChatGPT 应用](openai/translated/what_makes_a_great_chatgpt_app.zh.md) |
| 14 | [Why we built the Responses API](https://developers.openai.com/blog/responses-api) | [我们为什么构建 Responses API](openai/translated/responses_api.zh.md) |
| 15 | [Hello, world!](https://developers.openai.com/blog/intro) | [Hello, world!](openai/translated/intro.zh.md) |
| 16 | [Codex at DevDay](https://developers.openai.com/blog/codex-at-devday) | [DevDay 上的 Codex](openai/translated/codex-at-devday.zh.md) |
| 17 | [Codex for Documentation at Dagster](https://developers.openai.com/blog/codex-for-documentation-dagster) | [Dagster 的文档 Codex](openai/translated/codex-for-documentation-dagster.zh.md) |
| 18 | [Realtime API](https://developers.openai.com/blog/realtime-api) | [Realtime API](openai/translated/realtime_api.zh.md) |

---

## Claude AI Dev (10篇)

Claude 开发者博客，含 Claude Code、Skill 系统、Agent 工作流分析及泄漏事件解读。

| # | 文章（English) | 文章（中文） |
|---|---------------|-------------|
| 01 | [Claude Managed Agents: What Just Launched](https://claudeai.dev/blog/claude-managed-agents-what-just-launched) | [Claude Managed Agents：已发布内容](claudeai-dev/translated/claude-managed-agents-what-just-launched.md) |
| 02 | [Conway Timeline: How Anthropic Is Building Always-On Agents](https://claudeai.dev/blog/conway-timeline-how-anthropic-is-building-always-on-agents) | [Conway 时间线：Anthropic 如何构建常驻 Agent](claudeai-dev/translated/conway-timeline-how-anthropic-is-building-always-on-agents.md) |
| 03 | [What Actually Leaked From Claude Code This Time?](https://claudeai.dev/blog/what-actually-leaked-around-claude-code) | [这次 Claude Code 到底泄漏了什么？](claudeai-dev/translated/what-actually-leaked-around-claude-code.md) |
| 04 | [Did Claude Ship Auto-Fix in the Cloud Yet?](https://claudeai.dev/blog/did-claude-ship-auto-fix-in-the-cloud) | [Claude 的云端自动修复上线了吗？](claudeai-dev/translated/did-claude-ship-auto-fix-in-the-cloud.md) |
| 05 | [Claude's March 2026 Sprint: What Matters](https://claudeai.dev/blog/claudes-march-2026-shipping-sprint) | [Claude 2026年3月冲刺：真正重要的](claudeai-dev/translated/claudes-march-2026-shipping-sprint.md) |
| 06 | [Anthropic Skill Creator Update: A Practical Guide](https://claudeai.dev/blog/anthropic-skill-creator-update-practical-guide) | [Anthropic Skill Creator 更新：实用指南](claudeai-dev/translated/anthropic-skill-creator-update-practical-guide.md) |
| 07 | [Build Better Agent Skills with Tests](https://claudeai.dev/blog/build-better-agent-skills-with-tests) | [用测试构建更好的 Agent Skills](claudeai-dev/translated/build-better-agent-skills-with-tests.md) |
| 08 | [Build a Cowork Plugin from Scratch](https://claudeai.dev/blog/build-cowork-plugin-from-scratch) | [从零构建 Cowork 插件](claudeai-dev/translated/build-cowork-plugin-from-scratch.md) |
| 09 | [Choosing AI Agent Workflow Patterns That Ship](https://claudeai.dev/blog/choosing-ai-agent-workflow-patterns-that-ship) | [选择能落地的 AI Agent 工作流模式](claudeai-dev/translated/choosing-ai-agent-workflow-patterns-that-ship.md) |
| 10 | [Claude 1M Context: A Practical Rollout Guide](https://claudeai.dev/blog/claude-1m-context-practical-rollout-guide) | [Claude 1M Context：实用落地指南](claudeai-dev/translated/claude-1m-context-practical-rollout-guide.md) |

---

## 项目结构

```
blog-observation/
├── README.md              # 本文件
├── anthropic/
│   ├── translated/        # 23篇中文翻译 (.md)
│   ├── images/            # 167张配图
│   ├── raw/               # 原始JSON数据
│   ├── SUMMARY.md         # 分类索引
│   └── categories/
├── openai/
│   ├── translated/        # 18篇中文翻译 (.zh.md)
│   ├── images/             # 17张配图
│   ├── raw/               # 原始JSON数据
│   └── SUMMARY.md
└── claudeai-dev/
    ├── translated/        # 10篇中文翻译 (.md)
    ├── images/            # 5张配图
    ├── raw/               # 原始文本提取
    └── SUMMARY.md
```

## 翻译说明

- 翻译由 AI 完成，以中文简体呈现
- 技术术语尽量保留英文原形（API、SDK、MCP、CLI 等）
- 配图保存在各目录 `images/` 子目录，文中使用相对路径引用
- 本项目仅供学习研究使用，版权归各原创作者所有
