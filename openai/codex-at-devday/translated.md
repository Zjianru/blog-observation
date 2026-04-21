# Codex如何助力OpenAI DevDay 2025

来源：https://developers.openai.com/blog/codex-at-devday

---

本周，我们在旧金山圆满结束了第三届也是规模最大的一届OpenAI开发者大会。这场盛会凝聚了公司全体成员的辛勤付出。但在筹备过程中，有一个话题在讨论中被反复提及："如果没有[Codex](/codex)，我根本无法完成这些工作。"

今年是首次由Codex深度参与的开发者大会。从舞台演示（甚至那些与Codex无关的环节）到社区展厅的街机设备，再到产品本身，我们构建的每个环节都运用了Codex，它已成为打造2025年开发者大会的核心力量。

以下将简要揭秘Codex如何帮助我们提升效率、解决问题、实现多任务并行、优化优先级排序并完善组织协调的幕后故事。

## 操控摄像机与打造场馆灯光MCP系统

让我们从最引人注目的项目说起：罗曼·休伊特展示的Codex主题演讲演示。若您错过了直播，可[点击此处观看回放](https://www.youtube.com/live/hS1YqcewH0c?si=gw-CPYc-bZ9f0huh&t=2067)。

正如罗曼所言，这场演示中除使用我们的[实时智能体入门应用](https://github.com/openai/openai-agents-js/tree/main/examples/realtime-next)外，所有呈现内容均由Codex构建完成。

演示的初衷本是展现实时系统如何控制观众席的摄像机与灯光。但当罗曼深入该项目时，他面临着通过编程控制摄像机与灯光的技术挑战。

Codex成功找到了解决方案：它利用VISCA协议（一种诞生于90年代初的通信协议！）控制网络摄像机，独立完整地实现了该协议，并进一步构建了MCP服务器来管理灯光控制协议。

通过使用[Codex命令行工具](/codex/cli)，罗曼得以并行处理这两大难题，仅用一个下午就搭建出可运行的初始版本——全程无需触碰键盘，避免了原本可能耗费大量时间的研究与调试过程。

## 律动生成

DevDay的一大亮点是[Apps SDK](https://developers.openai.com/apps-sdk)的发布，它允许开发者直接在ChatGPT内构建丰富的应用体验。在Katia Gil Guzman的开发者主题演讲演示中，其构想是在Codex为Romain构建的轻量级MCP服务器基础上，打造一个功能丰富的节奏垫交互界面。

这意味着需要构建一个视觉美观且功能完善的界面，包括处理与灯光MCP服务器的连接以控制灯光效果，并支持演奏不同乐器。

借助[Codex Cloud](/codex/cloud)和最优N次采样技术，Katia不仅快速实现了可运行的应用，还能并行迭代多种设计方案。她尝试了从未来主义现代风格到OpenAI DevDay品牌化界面的各种设计，甚至探索了不同功能特性，整个过程高效且无需重复劳动。

![DevDay 2025舞台上Katia演示节奏垫应用的场景，背景为运行中的界面](codex-at-devday_00.jpg)

## 多任务游戏设计

如果你曾在DevDay的展区漫步，或许见过ArcadeGPT——两台街机设备允许用户通过GPT-5对现有游戏库进行混合重构，从而定制专属电子游戏。

当Kevin Whinnery开始搭建基础框架时，他需要为GPT-5准备一系列用于混合的初始游戏，且时间紧迫。为了快速创建并迭代这些游戏，他同时开启了七个（！！）终端窗口，每个窗口都运行着Codex CLI实例，分别处理单个文件的Phaser游戏实现。

得益于Codex CLI，他能异步迭代每个游戏版本，同步测试所有游戏，最终为参会者提供了大量可游玩和重构的游戏选择。

![ArcadeGPT标题界面的屏幕截图](codex-at-devday_01.png)

![ArcadeGPT游戏生成界面截图，同时显示提示词、实时生成的代码以及等待时可玩的俄罗斯方块游戏](codex-at-devday_02.png)

![由Codex生成的游戏画面截图](codex-at-devday_03.png)

## 重构演示应用

就我个人而言，在开发者日之前，我几乎每个任务都依赖Codex。要细数所有对Codex心怀感激的时刻实在困难，但有一个场景尤为突出。

当时我正在为我的[开放模型演讲](https://www.youtube.com/watch?v=1HL2YHRj270)准备微调演示，整个项目都基于Streamlit搭建。但这款Streamlit应用结构复杂，观众难以理解，还存在一些不易修复的行为漏洞。在用v0工具截取部分界面并快速完成初步设计后，我下载了模拟的[Next.js](https://nextjs.org)应用，并启动了Codex IDE扩展功能。

我指示它将我的Streamlit应用转换为能实现相同功能的FastAPI服务器，并与[Next.js](https://nextjs.org)前端对接。下达任务后，我外出用餐，归来时一个功能完备的应用程序已完整实现。此后，我又让Codex继续创建辅助页面，使演示效果更加生动直观。

若没有Codex，这项演示绝不可能如期完成。

![IDE扩展界面截图：显示将Streamlit应用移植到Next.js并搭配FastAPI服务器的指令](codex-at-devday_04.png)

## 从构想到现实

埃里卡·凯特尔森通过Codex IDE扩展，将整个展位演示从概念转化为现实，大幅节省了时间。她首先将设计草图输入Codex生成初始界面，甚至让Codex编写评估程序，帮助在速度与质量间权衡选择生成SVG的最佳模型。Codex协助埃里卡评估了演示采用单代理或多代理架构的优劣，随后重构了整个代码库，最终转向单代理架构。

项目构建完成后，Codex还生成了详细的Mermaid图表，埃里卡在展位现场用这些图表向参观者清晰阐释了应用的工作原理。

![埃里卡展位演示实景截图](codex-at-devday_05.png)

![Codex生成的SVG评估结果截图](codex-at-devday_06.png)

## 规模化审查

[AgentKit发布](https://openai.com/index/introducing-agentkit/)的一部分内容，是我们新推出的[Python](https://pypi.org/project/openai-guardrails/)和[TypeScript](https://www.npmjs.com/package/@openai/guardrails)版Guardrails SDK。这些SDK旨在与我们的[Python](https://openai.github.io/openai-agents-python)和[TypeScript](https://openai.github.io/openai-agents-js)版Agents SDK以及Agent Builder协同工作。为确保开发者获得出色的SDK使用体验，Kazuhiro（Kaz）Sera加入项目团队，助力项目完成最终冲刺。

他借助Codex快速熟悉了两个SDK的代码库，精准定位了他与Codex共同发现的若干缺陷的根本原因，通过Codex CLI和IDE扩展工具进行修复，并利用Codex代码审查功能排查遗留问题。

得益于Codex，他高效完成了所有工作，既帮助团队顺利发布SDK，又运用相同工具优化了同日发布的[ChatKit](https://platform.openai.com/docs/guides/chatkit)示例应用。

## 同时驾驭多重项目

在开发者大会前夕，我们许多人同时推进着日益增多的项目。Codex使我们能够通过IDE扩展和CLI工具，在本地与云端任务间灵活调配资源，实现多任务并行处理。

我们经常同时运行3-4个完全独立的任务。以我自身为例，我曾让Codex同步执行以下工作：为[gpt-oss服务器](https://github.com/openai/gpt-oss)构建Jupyter notebook支持功能、重构并修复智能体演示项目的若干缺陷、调整部分Codex文档结构、调试模型微调运行过程。

为实现快速上下文切换，我们不会耗费大量时间精心设计提示词——而是用简短的语句向Codex描述问题，启动任务后立即切换至下一项工作，稍后再返回查看Codex执行状态。甚至离开工位前，我们也养成了“让我再发送一个Codex任务”的习惯。

## 建立高效工作体系

为开发者推出多款新产品时，总会伴随大量新文档的产生。在早期阶段，这些文档往往散落在各处：无论是GitHub仓库内部、Google Docs还是Notion中。通常这些文档会反复修改直到最后一刻，本次发布也不例外。

得益于Codex Cloud，团队能够将这些零散的文档整合起来，只需向Codex提供关于如何拆分和组织文档的大致描述，剩下的工作就交给Codex处理。Codex自动分割文件，将其转换为MDX格式，建立必要的导航结构，并通过部署预览功能生成可供团队评审和迭代的PR。

如果没有Codex，这项工作通常需要花费数小时（甚至数天）才能赶在开发者日之前完成。

## 应对突发支线任务

最后，我们都经历过这样的场景——当你正专注于最重要的任务时，突然想起某个计划已久却总被耽搁的事项。

开发者日前夜的情况也颇为相似。在彩排间隙，我们正为这个重要日子做最后准备。当Katia即将登台彩排演示时，她突然想起自己还未按计划发布更新后的404页面。

她迅速在Codex Web上新建标签页，向Codex发送任务指令：要求同时生成两个版本的[developers.openai.com/404](https://developers.openai.com/404)页面，并启用最优候选功能。五分钟后登台前，Katia已通过Codex的预览截图审阅了两个方案，使用IDE扩展快速检出页面进行微调，最终成功发布了全新设计的404页面。

![Codex Web界面截图，含404页面预览](codex-at-devday_07.png)

## 这只是冰山一角

我们本可以花上数小时详述Codex如何助力开发者日的筹备，更不用说它在我们日常工作中提供的支持——但这仅仅是OpenAI内部运用Codex的惊鸿一瞥。

如果您想了解更多关于我们如何使用Codex以及一些最佳实践，[请观看我们关于Codex的开发者日演讲](https://www.youtube.com/watch?v=Gr41tYOzE20)或[查阅我们的文档](https://developers.openai.com/codex)。
