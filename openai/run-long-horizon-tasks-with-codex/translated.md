# 使用Codex执行长周期任务

来源：https://developers.openai.com/blog/run-long-horizon-tasks-with-codex

---

2025年9月，OpenAI推出了GPT-5-Codex，这是首个针对智能体编码优化的GPT-5版本。2025年12月，我们发布了5.2版本，从那时起人们开始相信使用自主编码智能体是可靠的。特别是，我们发现模型能够可靠遵循指令的时长实现了巨大飞跃。

我想对这一极限进行压力测试。于是我给Codex一个空白代码库、完全访问权限和一项任务：从零开始构建一个设计工具。然后我让它以“超高”推理级别运行GPT-5.3-Codex。Codex连续运行了约25小时，使用了约1300万token，生成了约3万行代码。

这是一次实验，而非生产部署。但它在长周期工作所需的关键环节表现良好：遵循规范、保持任务专注、运行验证以及实时修复故障。

![Codex设计工具界面](run-long-horizon-tasks-with-codex_00.jpeg)

## 长周期Codex会话实录

我让Codex为会话数据生成摘要页面：

![Codex会话摘要面板](run-long-horizon-tasks-with-codex_01.jpeg)

以下是CLI会话统计和token使用情况的视图：

![Codex CLI会话统计与token用量](run-long-horizon-tasks-with-codex_02.jpeg)

这些截图很有价值，因为它们清晰展现了核心转变：智能体编码正日益关注时间跨度，而不仅仅是单次智能表现。

## 真正的变革在于时间跨度

这不仅是“模型变得更聪明”。实际变化在于智能体能够更长时间保持连贯性，端到端完成更大规模的工作模块，并在出错时恢复执行而不丢失任务主线。

METR在时间跨度基准测试方面的研究为这一趋势提供了有益框架：前沿智能体能以约50%和80%可靠性完成的软件任务时长正在快速攀升，粗略估计每7个月翻一番。详见[《衡量AI完成长周期任务的能力（METR）》](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)。

![METR图表测量AI完成长任务的能力](run-long-horizon-tasks-with-codex_03.jpeg)

我们近期发布的GPT-5.3-Codex[上线公告](https://openai.com/index/introducing-gpt-5-3-codex/)通过两种实用方式进一步推动了智能体工作：

  1. 更擅长多步骤执行（规划→实施→验证→修复）
  2. 无需重置整个运行过程即可在中途灵活调整方向（进度修正不会清除已有成果）

Cursor团队关于长期自主编码系统的论述也给予我启发，包括他们的浏览器构建实验：[Cursor如何构建网页浏览器（智能体规模化实践）](https://cursor.com/blog/scaling-agents)。

Cursor团队指出，OpenAI模型在“持续自主工作方面表现更出色：遵循指令、保持专注、避免偏离，并能精准完整地实现目标”。

## Codex为何能在长任务中保持连贯性

长期运行的工作并非依赖单一巨型提示，而更取决于模型运行的智能体循环框架。

在Codex中，循环流程大致如下：

  1. 规划
  2. 编辑代码
  3. 运行工具（测试/构建/代码检查）
  4. 观察结果
  5. 修复故障
  6. 更新文档/状态
  7. 重复循环

这个循环至关重要，因为它为智能体提供：

  * 真实反馈（错误信息、差异对比、运行日志）
  * 外部化状态（代码库、文件、文档、工作树、输出结果）
  * 持续可控性（可根据结果动态调整方向）

这也解释了为何Codex模型在专属界面中的表现优于通用聊天窗口：运行框架提供了结构化上下文（代码库元数据、文件树、差异对比、命令输出），并强制执行规范的“完成判定”流程。

我们近期发布的[专题文章](https://openai.com/index/unrolling-the-codex-agent-loop/)详细解析了Codex智能体循环机制。

此外，我们还推出了让该循环能投入日常使用的Codex应用程序：

*   [跨项目并行线程](https://developers.openai.com/codex/app/features)（长时间工作不会阻塞你的日常工作）
*   [技能](https://developers.openai.com/codex/skills)（标准化计划/实施/测试/报告流程）
*   [自动化](https://developers.openai.com/codex/app/automations/)（后台处理常规工作）
*   [Git 工作树](https://developers.openai.com/codex/app/worktrees/)（隔离运行环境，保持差异可审查，减少冲突）

![带有项目线程的 Codex 应用工作区](run-long-horizon-tasks-with-codex_04.jpeg)

## 我的测试配置

我选择了一个设计工具进行这次“实验”，因为它是一个严苛的测试：涉及用户界面、数据模型、编辑操作以及大量边界情况。你无法蒙混过关。如果架构出错，它会很快崩溃。

我向 GPT-5.3-Codex 提供了一个内容详尽的规格说明，并以“超高”推理模式运行。最终，它连续运行了约 25 小时，能够保持思路连贯并交付高质量的代码。该模型还为完成的每个里程碑运行了验证步骤（测试、代码检查、类型检查）。

## 核心理念：持久的项目记忆

最重要的技术是持久的项目记忆。我将规格说明、计划、约束条件和状态写入 Markdown 文件中，以便 Codex 能够反复查阅。这防止了目标偏离，并保持了对“完成”定义的稳定理解。

相关代码库链接如下，文件结构如下：

#### [Prompt.md](https://github.com/derrickchoi-openai/design-desk/blob/main/docs/prompt.md)（规格说明 + 交付成果）

目的：锁定目标，确保智能体不会“构建出令人印象深刻但错误的东西”。

文件中的关键部分：

*   目标与非目标
*   硬性约束（性能、确定性、用户体验、平台）
*   交付成果（完成时必须存在的内容）
*   “完成标准”（检查项 + 演示流程）

初始提示告诉 Codex 将提示/规格说明文件视为完整的项目规范，并生成基于里程碑的计划：

![用于启动 Codex 运行的提示](run-long-horizon-tasks-with-codex_05.jpeg)

#### [Plan.md](https://github.com/derrickchoi-openai/design-desk/blob/main/docs/plans.md)（里程碑 + 验证）

目的：将开放式任务转化为智能体能够完成并验证的一系列检查点。

文件中的关键部分：

  * 里程碑需细化至单个循环内可完成
  * 每个里程碑的验收标准 + 验证指令
  * 暂停修复规则：若验证失败，需修复后再继续
  * 决策记录以避免反复摇摆
  * 代码库的预期架构

![Codex 在工作时参考计划 Markdown 文件](run-long-horizon-tasks-with-codex_06.jpeg)

_请注意，我们最近在 Codex 应用、CLI 和 IDE 扩展中新增了原生计划模式。该功能可在实施变更前将大型任务拆解为清晰、可审查的步骤序列，便于预先统一实施方案。若需要额外说明，Codex 会提出后续问题。可通过 /plan 斜杠命令启用此功能。_

#### [实施指南.md](https://github.com/derrickchoi-openai/design-desk/blob/main/docs/implement.md)（参照计划的执行说明）

目的：这是操作手册。它明确告知 Codex 如何执行：遵循计划、控制变更范围、运行验证、更新文档。

文件中的关键部分：

  * 计划 Markdown 文件是唯一信源（按里程碑推进）
  * 每个里程碑后执行验证（立即修复失败项）
  * 控制变更范围（不扩大任务边界）
  * 持续更新文档 Markdown 文件

![指示 Codex 读取 implement.md 作为执行指令的提示](run-long-horizon-tasks-with-codex_07.jpeg)

#### [文档记录.md](https://github.com/derrickchoi-openai/design-desk/blob/main/docs/documentation.md)（实施过程中的状态+决策）

目的：这是共享记忆与审计日志。通过它，即使离开数小时仍能掌握进展全貌。

文件中的关键部分：

  * 当前里程碑状态（已完成项、待办事项）
  * 已确定的决策（及其依据）
  * 运行与演示方法（指令+快速冒烟测试）
  * 已知问题/后续事项

![显示里程碑状态更新的文档文件](run-long-horizon-tasks-with-codex_08.jpeg)

以下是实际运行中里程碑验证的具体呈现：

![Codex在里程碑阶段为验证质量所运行的命令](run-long-horizon-tasks-with-codex_09.jpeg)

### 每个里程碑的验证

Codex并非仅仅编写代码并期望其运行。在每个里程碑节点后，它会运行验证命令，修复问题后再继续推进。

以下是它被要求使用的质量检查命令示例：

![用于代码规范检查、类型检查、测试、构建和导出的质量命令](run-long-horizon-tasks-with-codex_10.jpeg)

以及Codex在代码规范检查失败后修复问题的示例：

![Codex在运行npm run lint后修复问题](run-long-horizon-tasks-with-codex_11.jpeg)

## 智能体构建的成果

最终成果虽非完美或可直接投入生产，但它是真实且可测试的。本次运行的评判标准不是“能否编译通过”，而是“是否遵循指令，以及能否实际运行？”

已实现的高级功能包括：

  1. 画布编辑（框架、群组、形状、文本、图像/图标、按钮、图表）
  2. 实时协作（在线状态显示、光标追踪、选区同步、跨标签页编辑同步）
  3. 检查器控件（几何属性、样式设置、文本编辑）
  4. 图层管理（搜索、重命名、锁定/隐藏、排序）
  5. 参考线/对齐/吸附功能
  6. 历史快照与恢复
  7. 时间轴回放与历史分支创建
  8. 原型模式（热点区域与流程导航）
  9. 评论系统（可固定线程与解决/重开功能）
  10. 导出功能（保存/导入/导出 + 通过CLI导出为JSON及React + Tailwind格式）

## 长周期Codex任务的关键启示

本次运行成功的关键并非单一的精巧提示，而是以下要素的结合：

  * 明确的目标与约束条件（规范文件）
  * 设有验收标准的里程碑节点（`plans.md`）
  * 指导智能体操作流程的执行手册（`implement.md`）
  * 持续验证机制（测试/代码检查/类型检查/构建）
  * 实时状态与审计日志（`documentation.md`）确保运行过程可追溯

这代表了长周期编码工作的演进方向：减少人工监控，在设定防护机制的前提下实现更多自主执行。

## 尝试用Codex处理您的长周期任务

这次为期25小时的Codex运行展示了代码构建的未来方向。我们正在超越单次提示和紧密结对编程的循环，转向能够端到端承担实际工作任务的长期运行伙伴，你只需在关键节点进行引导，而无需逐行微管理。

Codex的发展方向很明确：强化协作伙伴行为，与你的真实工作场景更紧密集成，并设立防护机制确保工作可靠、可审查且易于交付。我们已经看到，当智能体能够处理常规实现和验证工作时，开发者的效率显著提升，从而让人力能够专注于最重要的部分：设计、架构、产品决策以及那些没有现成模板的创新性问题。

这种变革不会止步于开发者。随着Codex在捕捉意图和提供安全脚手架（计划、验证、预览、回滚）方面日益精进，更多非技术人员将能够在无需深度使用集成开发环境的情况下进行构建和迭代。Codex的界面和模型将持续升级，但核心目标始终如一：让智能体不再像需要时刻照看的工具，而更像能在长期工作中值得信赖的合作伙伴。

如果你想亲自尝试，可以从以下资源开始：

  * [Codex概述](https://developers.openai.com/codex/)
  * [Codex快速入门](https://developers.openai.com/codex/quickstart/)
  * [Codex模型](https://developers.openai.com/codex/models/)
  * [Codex应用功能](https://developers.openai.com/codex/app/features/)
