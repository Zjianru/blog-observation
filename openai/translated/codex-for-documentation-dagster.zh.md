---
title: "Using Codex for education at Dagster Labs"
source: "https://developers.openai.com/blog/codex-for-documentation-dagster"
date: ""
translated: 2026-04-20
---

![](../images/codex-for-documentation-dagster_00.png)

# 使用 Codex 进行教育：Dagster Labs 案例

在 Dagster Labs，我们为数据工程师、机器学习工程师和分析师制作大量技术教育内容，帮助他们更好地理解如何使用 Dagster——一个开源的工作流编排框架。由于我们的用户来自不同的技术背景，我们发现以合适的技术深度满足每个角色至关重要。在这篇文章中，我将分享我们如何使用 OpenAI 的 Codex 来加速文档编写、跨媒介翻译内容，甚至衡量文档的完整程度。

## CONTRIBUTING.md 文件的力量

为了让社区成员和内部工程师更容易贡献文档，我们彻底改进了 CONTRIBUTING.md 文件。令我们惊讶的是，我们无意中显著提高了 Codex 的实用性。事实证明，在代码库中清晰地概述文档的层次结构、结构和最佳实践具有重要价值——无论对人类还是机器人都是如此。

## 贡献文档

### 内容

#### 链接

##### 使用完整路径而非相对链接

Docusaurus 并不总是能正确渲染相对链接，这可能导致用户在访问这些链接时看到间歇性的 404 错误。请使用完整路径而非相对链接，例如：

```markdown
更多信息，请参阅"[定义资产](/guides/build/assets/defining-assets)"。
```

而不是：

```markdown
更多信息，请参阅"[定义资产](defining-assets)"。
```

##### 使用不带尾部斜杠的 Dagster 文档链接

例如，使用 `/guides/build/assets/defining-assets` 而不是 `/guides/build/assets/defining-assets/`。

**上下文：** 带尾部斜杠的 Dagster 文档链接会自动重定向到不带尾部斜杠的链接。虽然这对于我们无法控制的文档链接很有帮助，但我们自己页面上的过多重定向可能会使搜索引擎困惑并导致 SEO 问题。

### API 文档

...

Codex 的效果取决于你提供的脚手架。一个结构良好的 CONTRIBUTING.md 既是人类的文档，也是 AI 的地图。

## 用于理解的 Codex

除了编写文档，Codex 还可以作为一个始终可用的代码解释器。对于开发者倡导者和技术写作者来说，这非常宝贵。在开源项目或拥有众多工程师的项目中，通常很难及时了解所有正在开发的功能及其工作原理。对于较小的开发者倡导者和技术写作者团队来说尤其如此。

我们发现 Codex 提供的一些最佳帮助是通过解释拉取请求，或者将其指向代码库的某部分并要求解释。我们在这里发现的一个技巧是利用 Codex 内部的 `gh` 命令来解释拉取请求。要求它审查 PR 描述和差异，总结功能实现的原因，并解释应如何向最终用户展示。

## 单仓库的力量

这可能是一个有争议的观点，但我非常喜欢单仓库。当上下文是关键时，将所有内容放在一个仓库中可访问，使得获取所需内容变得容易得多，对于 Codex 来说，这意味着完整的上下文：代码、文档和示例都在一个地方。

虽然有些人担心像 Codex 这样的工具无法随着仓库的规模扩展，但我发现情况并非如此。通过在 Codex 中使用文件引用（@），你可以给 Codex 一个初始的子目录或文件作为起点，然后再进一步探索。将框架代码与文档放在同一个仓库中有一些显著的好处。

这种设置让我们可以提示 Codex 读取框架代码并起草初始的文档脚手架，然后我们再对其进行完善。以下是一个示例，我们提示 Codex 审查现有的拉取请求，并在文档中添加一个部分，说明这些环境变量在配置部署时究竟有何用处。

>_ 你正在 ~/src/dagster 中使用 OpenAI Codex
> 要开始，请描述一个任务或尝试以下命令之一：
> /init - 创建一个包含 Codex 指令的 AGENTS.md 文件
> /status - 显示当前会话配置和令牌使用情况
> /approvals - 选择 Codex 可以在无需批准的情况下执行的操作
> /model - 选择要使用的模型和推理工作量
> ▌ 使用 `gh pr diff <number>` 审查拉取请求 32557 中的更改，审查引入的以及已存在的用于配置 gRPC 服务器的环境变量，然后更新 docs/docs/deployment/oss/oss-instance-configuration.md 页面以概述配置选项。

> 我将获取 PR 32557 的差异并扫描添加/更新的 gRPC 相关环境变量，然后与仓库中现有的环境变量使用情况进行交叉检查。
> • 运行 gh pr diff 32557 | sed -n '1,200p'
> • 运行 gh pr diff 32557 | sed -n '200,400p'
> • 探索
>   └ 在 dagster 中搜索 DAGSTER_GRPC_[A-Z_]+
>     读取 api.py, code_server.py, oss-instance-configuration.md
>     搜索 DAGSTER_CODE_SERVER_[A-Z_]+
>     读取 constants.py
>     搜索 DAGSTER_(REPOSITORY|SCHEDULE|SENSOR)_GRPC_TIMEOUT_SECONDS| DAGSTER_GRPC_SHUTDOWN_GRACE_PERIOD
>     在 dagster 中读取 proxy_server_manager.py
> > 接下来，我将扩展实例配置文档中的 gRPC 服务器部分，以包含 API gRPC 服务器变量和通信超时/限制，保持风格一致...

你可以在 dagster-io/dagster #32558 找到此会话生成的拉取请求。

## 在不同内容媒介之间翻译

不同的角色偏好不同的学习形式，但核心思想通常是相同的。因此，我们制作了多种内容媒介：博客文章、教程、在线课程、YouTube 视频等。这些材料的核心内容通常是相同的，只是根据目标角色的不同而呈现方式不同。

Codex 在这些媒介之间翻译方面表现得非常出色。例如，将教程转换为 YouTube 视频的脚本，或者将低级教程稍作抽象用于博客文章。在下面的截图中，你可以找到一个示例提示，用于处理我们的一个示例项目并生成视频脚本。这种方法节省了数小时的改写时间，同时保持了我们在各个渠道上信息的一致性。

>_ 你正在 ~/src/dagster 中使用 OpenAI Codex
> ▌ 审查示例项目：examples/docs_projects/project_dagster_modal_pipes
> ▌ 并生成一个视频脚本来教授用户所涵盖的核心 Dagster 和 Modal 概念。
> ▌ 将脚本分成几个部分，并包含要在视频中展示的代码片段。
> ▌ 脚本的散文风格应有趣但专业。
> ▌ 将其保存到 MODAL_VIDEO_TRANSCRIPT.md。

> 我将在起草视频脚本之前扫描示例项目以了解其结构和代码。
> • 运行
>   └ bash -lc 'ls -la'
>     bash -lc 'ls -la examples/docs_projects/ project_dagster_modal_pipes'
>     bash -lc "rg --files examples/docs_projects/ project_dagster_modal_pipes | sed -n '1,120p'"
> • 探索
>   └ 列出 project_dagster_modal_pipes
>     搜索 rg --files examples/docs_projects/project_dagster_modal_pipes
>     读取 README.md, definitions.py, __init__.py, resources.py, constants.py, feeds.py, pipeline_factory.py, summarize.py, config.py, transcribe.py, hello_dagster.py, verify_cloud_mount.py
> • 添加 MODAL_VIDEO_TRANSCRIPT.md (+335 -0)

在此处查看完整的视频脚本！

## 评估文档覆盖率

我们使用 Codex 的一种更具实验性的方式是将其作为人类理解的代理。通过将文档作为事实来源和 Codex 的基础上下文，我们可以让它生成代码。例如，人们经常使用 Dagster 来运行和观察他们的 dbt 数据模型以及其他数据处理代码。通过提示 Codex 参考文档并为此项目生成代码，然后我们可以对生成的代码运行测试套件，以检查其是否按预期运行。如果它按预期工作，我们可以假设我们的文档充分涵盖了所需内容。如果 Codex 可以仅从我们的文档生成可运行的代码，这是一个强烈的信号，表明人类也可以做到，这成为文档完整性的间接衡量标准。

## 总结

总而言之，Dagster 团队发现 Codex 对于创建、审查和翻译教育内容非常有帮助。它使我们能够超越原有的能力进行扩展，帮助我们在框架发展过程中确保有足够的文档覆盖率，更重要的是，它使我们能够更容易地支持我们的社区。

Codex 强调了上下文和结构的重要性。对我们来说，这意味着完善我们的文档架构，以便人类和 AI 都能轻松导航。这个由 AI 驱动的反馈循环改善了我们创建内容的方式以及用户生成框架代码的方式。

随着 AI 工具的发展，文档、代码和自动化之间的界限将变得模糊。将文档视为结构化数据的团队将具有重大优势。
