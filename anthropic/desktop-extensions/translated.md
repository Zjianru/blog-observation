# 桌面扩展：为Claude Desktop提供一键式MCP服务器安装

来源：https://www.anthropic.com/engineering/desktop-extensions

---

* 文件扩展名更新

2025年9月11日

Claude桌面扩展现在使用.mcpb（MCP捆绑包）文件扩展名替代之前的.dxt扩展名。现有的.dxt扩展将继续有效，但我们建议开发者未来在新扩展中使用.mcpb扩展名。所有功能保持不变——这纯粹是命名规范的更新。

—

去年我们发布模型上下文协议（MCP）时，看到开发者构建了令人惊叹的本地服务器，让Claude能够访问从文件系统到数据库的各种资源。但我们不断听到同样的反馈：安装过程过于复杂。用户需要安装开发工具、手动编辑配置文件，还经常因依赖问题而卡住。

今天，我们推出桌面扩展——一种新的打包格式，让安装MCP服务器变得像点击按钮一样简单。

### 解决MCP安装难题

本地MCP服务器为Claude桌面用户解锁了强大的功能。他们可以与本地应用程序交互、访问私有数据、集成开发工具——同时所有数据都保留在用户设备上。然而，当前的安装过程存在显著障碍：

  * **需要开发工具**：用户需要安装Node.js、Python或其他运行时环境
  * **手动配置**：每个服务器都需要编辑JSON配置文件
  * **依赖管理**：用户必须解决包冲突和版本不匹配问题
  * **缺乏发现机制**：寻找有用的MCP服务器需要在GitHub上搜索
  * **更新复杂**：保持服务器最新意味着需要手动重新安装

这些痛点意味着，尽管MCP服务器功能强大，但对非技术用户来说基本上难以使用。

### 推出桌面扩展

桌面扩展（`.mcpb`文件）通过将整个MCP服务器——包括所有依赖项——打包成单个可安装包来解决这些问题。以下是用户将体验到的变化：

**之前：**

# 首先安装 Node.js
npm install -g @example/mcp-server
# 手动编辑 ~/.claude/claude_desktop_config.json 文件
# 重启 Claude Desktop
# 希望它能正常工作

**之后：**

  1. 下载 `.mcpb` 文件
  2. 双击通过 Claude Desktop 打开
  3. 点击"安装"

就这么简单。无需终端操作，无需配置文件，没有依赖冲突。

## 架构概览

桌面扩展是一个包含本地 MCP 服务器及 `manifest.json` 文件的压缩包，该清单文件描述了 Claude Desktop 和其他支持桌面扩展的应用程序需要了解的所有信息。

    extension.mcpb (ZIP 压缩包)
    ├── manifest.json         # 扩展元数据和配置
    ├── server/               # MCP 服务器实现
    │   └── [服务器文件]
    ├── dependencies/         # 所有必需的包/库
    └── icon.png             # 可选：扩展图标

    # 示例：Node.js 扩展
    extension.mcpb
    ├── manifest.json         # 必需：扩展元数据和配置
    ├── server/               # 服务器文件
    │   └── index.js          # 主入口点
    ├── node_modules/         # 捆绑的依赖项
    ├── package.json          # 可选：NPM 包定义
    └── icon.png              # 可选：扩展图标

    # 示例：Python 扩展
    extension.mcpb (ZIP 文件)
    ├── manifest.json         # 必需：扩展元数据和配置
    ├── server/               # 服务器文件
    │   ├── main.py           # 主入口点
    │   └── utils.py          # 附加模块
    ├── lib/                  # 捆绑的 Python 包
    ├── requirements.txt      # 可选：Python 依赖列表
    └── icon.png              # 可选：扩展图标

桌面扩展中唯一必需的文件是 manifest.json。Claude Desktop 会处理所有复杂事项：

  * **内置运行时**：我们随 Claude Desktop 内置了 Node.js，消除了外部依赖
  * **自动更新**：当有新版本可用时，扩展会自动更新
  * **安全密钥管理**：API 密钥等敏感配置存储在操作系统密钥链中

清单包含人类可读信息（如名称、描述或作者）、功能声明（工具、提示）、用户配置以及运行时要求。大多数字段都是可选的，因此最小化版本相当简短，不过在实践中，我们期望所有三种受支持的扩展类型（Node.js、Python 和经典二进制文件/可执行文件）都包含以下文件：

    {
      "mcpb_version": "0.1",                    // 此清单遵循的 MCPB 规范版本
      "name": "my-extension",                   // 机器可读名称（用于 CLI、API）
      "version": "1.0.0",                       // 扩展的语义版本号
      "description": "一个简单的 MCP 扩展",     // 扩展功能的简要描述
      "author": {                               // 作者信息（必需）
        "name": "扩展作者"                      // 作者姓名（必需字段）
      },
      "server": {                               // 服务器配置（必需）
        "type": "node",                         // 服务器类型："node"、"python" 或 "binary"
        "entry_point": "server/index.js",       // 主服务器文件路径
        "mcp_config": {                         // MCP 服务器配置
          "command": "node",                    // 运行服务器的命令
          "args": [                             // 传递给命令的参数
            "${__dirname}/server/index.js"      // ${__dirname} 会被替换为扩展目录路径
          ]
        }
      }
    }

复制

清单规范中提供了许多便捷选项，旨在简化本地 MCP 服务器的安装和配置过程。服务器配置对象的定义方式既支持通过模板字面量形式收集用户自定义配置，也支持平台特定的覆盖设置。扩展开发者可以详细定义他们希望从用户那里收集何种配置信息。

让我们通过一个具体示例来看看清单如何协助配置。在下面的清单中，开发者声明用户需要提供 `api_key`。Claude 在用户提供该值之前不会启用扩展，并会自动将其保存在操作系统的密钥保险库中，同时在启动服务器时透明地将 `${user_config.api_key}` 替换为用户提供的值。类似地，`${__dirname}` 将被替换为扩展解压目录的完整路径。

    {
      "mcpb_version": "0.1",
      "name": "my-extension",
      "version": "1.0.0",
      "description": "一个简单的 MCP 扩展",
      "author": {
        "name": "扩展作者"
      },
      "server": {
        "type": "node",
        "entry_point": "server/index.js",
        "mcp_config": {
          "command": "node",
          "args": ["${__dirname}/server/index.js"],
          "env": {
            "API_KEY": "${user_config.api_key}"
          }
        }
      },
      "user_config": {
        "api_key": {
          "type": "string",
          "title": "API 密钥",
          "description": "用于身份验证的 API 密钥",
          "sensitive": true,
          "required": true
        }
      }
    }

复制

一个包含大部分可选字段的完整 `manifest.json` 可能如下所示：

{
  "mcpb_version": "0.1",
  "name": "My MCP Extension",
  "display_name": "我的超棒 MCP 扩展",
  "version": "1.0.0",
  "description": "关于此扩展功能的简要描述",
  "long_description": "详细的描述，可包含多个段落，解释扩展的功能、使用场景和特性。支持基础 Markdown 格式。",
  "author": {
    "name": "您的姓名",
    "email": "yourname@example.com",
    "url": "https://your-website.com"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/your-username/my-mcp-extension"
  },
  "homepage": "https://example.com/my-extension",
  "documentation": "https://docs.example.com/my-extension",
  "support": "https://github.com/your-username/my-extension/issues",
  "icon": "icon.png",
  "screenshots": [
    "assets/screenshots/screenshot1.png",
    "assets/screenshots/screenshot2.png"
  ],
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"],
      "env": {
        "ALLOWED_DIRECTORIES": "${user_config.allowed_directories}"
      }
    }
  },
  "tools": [
    {
      "name": "search_files",
      "description": "在目录中搜索文件"
    }
  ],
  "prompts": [
    {
      "name": "poetry",
      "description": "让大语言模型创作诗歌",
      "arguments": ["topic"],
      "text": "围绕以下主题创作一首富有创意的诗歌：${arguments.topic}"
    }
  ],
  "tools_generated": true,
  "keywords": ["api", "automation", "productivity"],
  "license": "MIT",
  "compatibility": {
    "claude_desktop": ">=1.0.0",
    "platforms": ["darwin", "win32", "linux"],
    "runtimes": {
      "node": ">=16.0.0"
    }
  },
  "user_config": {
    "allowed_directories": {
      "type": "directory",
      "title": "允许访问的目录",
      "description": "服务器可访问的目录"
    }

"multiple": true,
          "required": true,
          "default": ["${HOME}/Desktop"]
        },
        "api_key": {
          "type": "string",
          "title": "API密钥",
          "description": "用于身份验证的API密钥",
          "sensitive": true,
          "required": false
        },
        "max_file_size": {
          "type": "number",
          "title": "最大文件大小（MB）",
          "description": "要处理的最大文件大小",
          "default": 10,
          "min": 1,
          "max": 100
        }
      }
    }

"multiple": true,
"required": true,
"default": ["${HOME}/桌面"]

        },
        "api_key": {
          "type": "string",
          "title": "API密钥",
          "description": "用于身份验证的API密钥",
          "sensitive": true,
          "required": false
        },
        "max_file_size": {
          "type": "number",
          "title": "最大文件大小（MB）",
          "description": "要处理的最大文件大小",
          "default": 10,
          "min": 1,
          "max": 100
        }
      }
    }

要查看扩展和清单示例，请参考[MCPB仓库中的示例](https://github.com/anthropics/dxt/tree/main/examples)。

`manifest.json`中所有必需和可选字段的完整规范可在我们的[开源工具链](https://github.com/anthropics/dxt/blob/main/MANIFEST.md)中找到。

### 构建你的第一个扩展

让我们逐步学习如何将现有的MCP服务器打包为桌面扩展。我们将以简单的文件系统服务器为例。

#### 步骤1：创建清单

首先，为你的服务器初始化一个清单：

    npx @anthropic-ai/mcpb init

这个交互式工具会询问你的服务器信息并生成完整的manifest.json。如果你想快速生成最基本的manifest.json，可以使用--yes参数运行该命令。

#### 步骤2：处理用户配置

如果你的服务器需要用户输入（如API密钥或允许的目录），请在清单中声明：

    "user_config": {
      "allowed_directories": {
        "type": "directory",
        "title": "允许访问的目录",
        "description": "服务器可以访问的目录",
        "multiple": true,
        "required": true,
        "default": ["${HOME}/文档"]
      }
    }

Claude桌面版将：

  * 显示用户友好的配置界面
  * 在启用扩展前验证输入
  * 安全存储敏感值
  * 根据开发者配置，通过参数或环境变量将配置传递给服务器

在下面的示例中，我们将用户配置作为环境变量传递，但它也可以是一个参数。

    "server": {
       "type": "node",
       "entry_point": "server/index.js",
       "mcp_config": {
       "command": "node",
       "args": ["${__dirname}/server/index.js"],
       "env": {
          "ALLOWED_DIRECTORIES": "${user_config.allowed_directories}"
       }
       }
    }

复制

#### 步骤 3：打包扩展

将所有内容打包成 `.mcpb` 文件：

    npx @anthropic-ai/mcpb pack

复制

此命令：

  1. 验证您的清单
  2. 生成 `.mcpb` 归档文件

#### 步骤 4：本地测试

将您的 `.mcpb` 文件拖入 Claude Desktop 的设置窗口。您将看到：

  * 关于您扩展的可读信息
  * 所需的权限和配置
  * 一个简单的“安装”按钮

### 高级功能

#### 跨平台支持

扩展可以适配不同的操作系统：

    "server": {
      "type": "node",
      "entry_point": "server/index.js",
      "mcp_config": {
        "command": "node",
        "args": ["${__dirname}/server/index.js"],
        "platforms": {
          "win32": {
            "command": "node.exe",
            "env": {
              "TEMP_DIR": "${TEMP}"
            }
          },
          "darwin": {
            "env": {
              "TEMP_DIR": "${TMPDIR}"
            }
          }
        }
      }
    }

复制

#### 动态配置

使用模板字面量获取运行时值：

  * `${__dirname}`：扩展的安装目录
  * `${user_config.key}`：用户提供的配置
  * `${HOME}, ${TEMP}`：系统环境变量

#### 功能声明

帮助用户预先了解功能：

    "tools": [
      {
        "name": "read_file",
        "description": "读取文件内容"
      }
    ],
    "prompts": [
      {
        "name": "code_review",
        "description": "审查代码以遵循最佳实践",
        "arguments": ["file_path"]
      }
    ]

复制

### 扩展目录

我们推出时，将在Claude桌面版中内置一个精选扩展目录。用户可以浏览、搜索并一键安装——无需在GitHub上搜寻或审核代码。

虽然我们预计桌面扩展规范以及在macOS和Windows版Claude中的实现会随时间演进，但我们期待看到扩展能以各种创意方式拓展Claude的能力。

提交扩展的步骤：

  1. 确保遵循提交表格中的指南
  2. 在Windows和macOS系统上进行测试
  3. [提交您的扩展](https://docs.google.com/forms/d/14_Dmcig4z8NeRMB_e7TOyrKzuZ88-BLYdLvS6LPhiZU/edit)
  4. 我们的团队将审核质量和安全性

### 构建开放生态系统

我们致力于围绕MCP服务器构建开放生态系统，并相信其被多种应用和服务广泛采用的能力已使社区受益。基于这一承诺，我们将开源桌面扩展规范、工具链，以及macOS和Windows版Claude用于实现桌面扩展支持的模式和关键功能。我们希望MCPB格式不仅能提升本地MCP服务器在Claude中的可移植性，也能惠及其他AI桌面应用。

我们将开源：

  * 完整的MCPB规范
  * 打包和验证工具
  * 参考实现代码
  * TypeScript类型和模式

这意味着：

  * **对于MCP服务器开发者**：一次打包，即可在任何支持MCPB的环境中运行
  * **对于应用开发者**：无需从零构建即可添加扩展支持
  * **对于用户**：在所有支持MCP的应用中获得一致的体验

该规范和工具链特意标记为0.1版本，因为我们期待与更广泛的社区合作，共同演进和改进这一格式。我们期待您的反馈。

### 安全与企业考量

我们理解扩展会带来新的安全考量，尤其对企业用户而言。我们在桌面扩展的预览版中内置了多项防护措施：

#### 对于用户

*   敏感数据始终保存在操作系统密钥链中
*   自动更新功能
*   可审计已安装的扩展程序

#### 企业功能

*   支持组策略（Windows）和移动设备管理（macOS）
*   可预装经批准的扩展程序
*   可屏蔽特定扩展程序或发布者
*   可完全禁用扩展目录
*   可部署私有扩展目录

如需了解如何在组织内管理扩展程序，请参阅我们的[文档](https://support.anthropic.com/en/articles/10949351-getting-started-with-model-context-protocol-mcp-on-claude-for-desktop)。

### 快速开始

准备好构建自己的扩展程序了吗？以下是如何开始：

**面向MCP服务器开发者**：请查阅我们的[开发者文档](https://github.com/anthropics/dxt)——或直接在本地MCP服务器目录中运行以下命令立即开始：

    npm install -g @anthropic-ai/mcpb
    mcpb init
    mcpb pack

复制

**面向Claude桌面用户**：更新至最新版本，在设置中查找"扩展程序"部分

**面向企业用户**：请查阅我们的企业部署文档了解部署选项

### 使用Claude Code进行构建

在Anthropic内部，我们发现Claude能够以最少的人工干预出色地构建扩展程序。如果您也想使用Claude Code，建议简要说明您希望扩展程序实现的功能，然后在提示词中添加以下上下文：

    我想将此构建为桌面扩展程序，简称"MCPB"。请遵循以下步骤：

    1. **仔细阅读规范文档：**
       - https://github.com/anthropics/mcpb/blob/main/README.md - MCPB架构概述、功能特性和集成模式
       - https://github.com/anthropics/mcpb/blob/main/MANIFEST.md - 完整的扩展清单结构和字段定义
       - https://github.com/anthropics/mcpb/tree/main/examples - 参考实现（包含"Hello World"示例）

2. **创建规范的扩展结构：**
       - 按照 MANIFEST.md 规范生成有效的 manifest.json 文件
       - 使用 @modelcontextprotocol/sdk 实现 MCP 服务器，并正确定义工具
       - 包含完善的错误处理和超时管理机制

    3. **遵循最佳开发实践：**
       - 通过 stdio 传输实现规范的 MCP 协议通信
       - 采用清晰的结构化工具定义，包含模式验证和一致的 JSON 响应格式
       - 充分利用扩展将在本地运行的特点进行优化
       - 添加适当的日志记录和调试功能
       - 包含完整的文档和安装配置说明

    4. **测试注意事项：**
       - 验证所有工具调用都能返回正确结构的响应
       - 确保清单文件正确加载且与宿主程序集成正常

    生成完整、可用于生产环境的代码，确保能够立即测试。重点关注防御性编程、清晰的错误提示信息，并严格遵循 MCPB 规范以保证与生态系统的兼容性。

### 结语

桌面扩展代表了用户与本地 AI 工具交互方式的根本性变革。通过消除安装障碍，我们正在让强大的 MCP 服务器变得人人可用——而不仅仅是开发者专属。

在内部，我们正使用桌面扩展来共享高度实验性的 MCP 服务器——有些充满趣味，有些极具实用价值。其中一个团队尝试探索当我们的模型直接连接到 GameBoy 时能达到何种程度，类似于我们之前进行的["Claude 玩宝可梦"研究](https://www.anthropic.com/news/visible-extended-thinking)。我们通过桌面扩展打包了一个独立扩展程序，该程序能够启动流行的 [PyBoy](https://github.com/Baekalfen/PyBoy) GameBoy 模拟器，并让 Claude 获得控制权。我们相信，将模型能力与用户本地机器上已有的工具、数据和应用程序相连接，存在着无限可能。


我们迫不及待想看到您的创作成果。曾经为我们带来数千个MCP服务器的创造力，如今只需一次点击就能触达数百万用户。准备好分享您的MCP服务器了吗？[提交扩展进行审核](https://forms.gle/tyiAZvch1kDADKoP9)

[![带有复杂几何形状和精细表面纹理的咬合拼图](images/desktop-extensions_01.svg)想要了解更多？探索课程](https://anthropic.skilljar.com/)
