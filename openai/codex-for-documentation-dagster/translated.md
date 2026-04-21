# 在Dagster Labs利用Codex赋能教育

来源：https://developers.openai.com/blog/codex-for-documentation-dagster

---

在[Dagster Labs](https://dagster.io)，我们为数据工程师、机器学习工程师和分析师制作了大量技术教育内容，以帮助他们更好地理解如何使用Dagster——一个开源的工作流编排框架。由于我们的用户来自不同的技术背景，我们发现以恰当的技术深度满足每个用户群体的需求至关重要。

在这篇文章中，我将分享我们如何利用OpenAI的Codex来加速文档编写、跨媒介翻译内容，甚至评估我们文档的完整度。

## CONTRIBUTING.md文件的强大作用

为了让社区成员和内部工程师更轻松地贡献文档，我们彻底改进了[CONTRIBUTING.md](https://github.com/dagster-io/dagster/blob/3c2d36054f4014ca8316e533975a538d6eff62c4/docs/CONTRIBUTING.md)文件。出乎意料的是，我们无意中显著提升了Codex的实用性。事实证明，清晰概述代码库中文档编写的层次结构、规范和最佳实践具有重要价值——无论对人类还是机器而言都是如此。

    # 贡献文档指南

    ## 内容规范

    ### 链接处理

    #### 使用完整路径而非相对链接

    Docusaurus有时无法正确渲染相对链接，可能导致用户访问这些链接时偶现404错误。请使用完整路径，例如：

    ```
    更多信息请参阅"[定义资产](/guides/build/assets/defining-assets)"。
    ```

    而非：

    ```
    更多信息请参阅"[定义资产](defining-assets)"。
    ```

    #### 使用无尾部斜杠的Dagster文档链接

    例如使用`/guides/build/assets/defining-assets`而非`/guides/build/assets/defining-assets/`。

    **背景说明：** 带尾部斜杠的Dagster文档链接会自动重定向至无斜杠版本。虽然这对我们无法控制的文档链接有帮助，但自身页面过多重定向可能干扰搜索引擎并引发SEO问题。

    ### API文档规范

    ...

Codex的能力取决于你为它搭建的脚手架。一份结构清晰的CONTRIBUTING.md既是面向人类的文档，也是AI的行动指南。

## 用Codex理解代码

除了编写文档，Codex还能充当随时待命的代码解读器。对于开发者布道师和技术写作者而言，这具有不可估量的价值。在开源项目或拥有大量工程师的项目中，要持续跟进所有正在开发的功能及其运作原理往往非常困难，对于规模较小的开发者布道师和技术写作团队尤其如此。我们发现，Codex提供的最佳协助方式之一是通过解读拉取请求，或引导其关注代码库的特定部分并要求解释。

我们在此发现的一个技巧是利用Codex内部的`gh`命令来解读拉取请求。可以要求它审阅PR描述和差异对比，总结功能实现的原因，并解释应如何向最终用户呈现该功能。

## 单体仓库的力量

这或许是个有争议的观点，但我非常推崇单体仓库模式。当上下文关联至关重要时，将所有内容集中在一个仓库中能极大提升获取所需信息的效率。对Codex而言，这意味着完整的上下文环境：代码、文档和示例全部集中在一处。

尽管有人担心像Codex这样的工具可能无法适应大型仓库的规模，但我的经验表明并非如此。通过使用Codex内部的文件引用功能（`@`），你可以为Codex指定初始子目录或文件作为探索起点。将框架代码与文档置于同一仓库中会带来显著优势：这种设置允许我们指示Codex读取框架代码，并起草可供后续完善的初始文档框架。

以下示例展示了我们如何指示Codex审阅现有拉取请求，并在文档中添加章节说明这些环境变量在部署配置中的具体作用：

    >_ 您正在~/src/dagster目录中使用OpenAI Codex

     请描述任务需求，或尝试以下命令开始：

/init - 创建包含Codex使用说明的AGENTS.md文件
/status - 显示当前会话配置与令牌使用情况
/approvals - 设置Codex无需批准即可执行的操作
/model - 选择使用的模型与推理强度等级

▌ 使用 `gh pr diff <编号>` 审查拉取请求32557的变更，检查新增及现有的
▌ gRPC服务器配置环境变量，随后更新 docs/docs/deployment/oss/oss-instance-configuration.md
▌ 文档页面以梳理配置选项。

> 我将获取PR 32557的差异内容，扫描新增/更新的gRPC相关环境变量，
  并与代码库中现有环境变量使用情况进行交叉核对。

• 执行 gh pr diff 32557 | sed -n '1,200p'
• 执行 gh pr diff 32557 | sed -n '200,400p'
• 展开探索
  └ 在dagster中搜索 DAGSTER_GRPC_[A-Z_]+
    查阅api.py、code_server.py、oss-instance-configuration.md
    搜索 DAGSTER_CODE_SERVER_[A-Z_]+
    查阅constants.py
    搜索 DAGSTER_(REPOSITORY|SCHEDULE|SENSOR)_GRPC_TIMEOUT_SECONDS|
           DAGSTER_GRPC_SHUTDOWN_GRACE_PERIOD
    查阅proxy_server_manager.py

> 接下来，我将扩展实例配置文档中的gRPC服务器章节，
  纳入API gRPC服务器变量及通信超时/限制说明，同时保持文档风格一致

  ...

您可以在[dagster-io/dagster #32558](https://github.com/dagster-io/dagster/pull/32558)查看本次会话生成的拉取请求。

## 跨媒介内容转换

不同受众群体偏好不同的学习形式，但核心知识体系往往相通。为此我们制作了多元化的内容媒介：博客文章、教程指南、在线课程、YouTube视频等。这些材料的核心内容通常可以保持一致，仅需根据目标受众的特点调整呈现方式。

Codex 在不同媒介间的转换表现尤为出色。例如，将教程内容转化为 YouTube 视频脚本，或是将基础教程稍作抽象处理用于博客文章。在下方截图中，您可以看到一个提示词示例，它被用于将我们的示例项目转化为视频脚本。这种方法节省了大量重写时间，同时确保我们在不同渠道的信息传达保持一致性。

    >_ 您正在 ~/src/dagster 中使用 OpenAI Codex

    ▌请审阅示例项目：examples/docs_projects/project_dagster_modal_pipes
    ▌并生成视频脚本来向用户讲解其中涉及的 Dagster 与 Modal 核心概念
    ▌将脚本按章节划分，并包含视频中需要展示的代码片段
    ▌脚本语言风格应兼具趣味性与专业性
    ▌请将内容保存至 MODAL_VIDEO_TRANSCRIPT.md 文件

    > 我将先扫描示例项目以理解其结构和代码
      再开始起草视频脚本

    • 已执行
      └ bash -lc 'ls -la' bash -lc 'ls -la examples/docs_projects/
            project_dagster_modal_pipes' bash -lc "rg --files examples/docs_projects/
            project_dagster_modal_pipes | sed -n '1,120p'"

    • 已探索
      └ 列出 project_dagster_modal_pipes 项目文件
        搜索 rg --files examples/docs_projects/project_dagster_modal_pipes
        读取 README.md, definitions.py, __init__.py, resources.py, constants.py,
             feeds.py, pipeline_factory.py, summarize.py, config.py, transcribe.py,
             hello_dagster.py, verify_cloud_mount.py

    • 已创建 MODAL_VIDEO_TRANSCRIPT.md (+335 -0)

查看完整视频脚本请点击[此处](https://gist.github.com/cmpadden/a371c1300bdc42601a77b3eefb938483)！

## 评估文档覆盖度

我们正在尝试一种更具实验性的 Codex 应用方式——将其作为人类理解的代理工具。

通过将文档作为唯一事实来源和 Codex 的基础上下文，我们可以让它生成代码。例如，用户经常将 Dagster 用于运行和监控其 dbt 数据模型以及其他数据处理代码。

通过提示Codex参考文档并生成此项目的代码，我们可以对生成的代码运行测试套件，以验证其是否按预期运行。如果代码表现符合预期，我们就可以认为我们的文档已充分覆盖了所需内容。如果Codex仅凭我们的文档就能生成可运行的代码，这强烈表明人类同样可以做到，从而间接衡量了文档的完整性。

## 总结

总而言之，Dagster团队发现Codex在创建、审查和翻译教育内容方面提供了巨大帮助。它使我们能够超越原有的能力范围进行扩展，帮助我们在框架演进过程中确保文档覆盖充分，更重要的是，它让我们能够更轻松地支持我们的社区。

Codex强调了上下文和结构的重要性。对我们而言，这意味着需要优化文档架构，以便人类和人工智能都能轻松浏览。这个由人工智能驱动的反馈循环，既改进了我们创建内容的方式，也优化了用户生成框架代码的过程。随着人工智能工具的发展，文档、代码和自动化之间的界限将变得模糊。那些将文档视为结构化数据的团队将拥有显著优势。
