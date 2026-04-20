---
title: "桌面扩展：Claude Desktop的一键MCP服务器安装"
subtitle: "发布日期：2025年6月26日"
date: ""
source: "https://www.anthropic.com/engineering/desktop-extensions"
---

文件扩展名更新

2025年9月11日

Claude Desktop扩展现在使用.mcpb（MCP Bundle）文件扩展名而非.dxt。现有.dxt扩展将继续工作，但我们建议开发者为新扩展使用.mcpb。所有功能保持不变——这只是命名约定的更新。

去年我们发布模型上下文协议（MCP）时，看到开发者构建了出色的本地服务器，让Claude能够访问从文件系统到数据库的各种内容。但我们一直听到同样的反馈：安装过程太复杂。用户需要开发者工具，必须手动编辑配置文件，并且经常在依赖问题上卡住。

今天，我们推出桌面扩展——一种新的打包格式，使MCP服务器的安装变得像点击按钮一样简单。

解决MCP安装问题

本地MCP服务器为Claude Desktop用户解锁了强大的功能。它们可以与本地应用程序交互、访问私有数据并集成开发工具——同时将数据保留在用户的机器上。然而，当前的安装过程造成了重大障碍：

这些摩擦点意味着，尽管MCP服务器功能强大，但对于非技术用户来说仍然基本上无法访问。

介绍桌面扩展

桌面扩展（.mcpb文件）通过将整个MCP服务器——包括所有依赖项——打包成单个可安装包来解决这些问题。以下是用户方面的变化：

之前：

# 首先安装Node.js
npm install -g @example/mcp-server
# 手动编辑~/.claude/claude_desktop_config.json
# 重启Claude Desktop
# 希望它能工作

之后：

就这样。无需终端，无需配置文件，无依赖冲突。

架构概述

桌面扩展是一个zip归档文件，包含本地MCP服务器以及一个manifest.json，后者描述了Claude Desktop和其他支持桌面扩展的应用程序需要了解的所有内容。

extension.mcpb（ZIP归档）
├── manifest.json         # 扩展元数据和配置
├── server/               # MCP服务器实现
│   └── [服务器文件]    
├── dependencies/         # 所有必需的包/库
└── icon.png             # 可选：扩展图标

# 示例：Node.js扩展
extension.mcpb
├── manifest.json         # 必需：扩展元数据和配置
├── server/               # 服务器文件
│   └── index.js          # 主入口点
├── node_modules/         # 捆绑的依赖项
├── package.json          # 可选：NPM包定义
└── icon.png              # 可选：扩展图标

# 示例：Python扩展
extension.mcpb（ZIP文件）
├── manifest.json         # 必需：扩展元数据和配置
├── server/               # 服务器文件
│   ├── main.py           # 主入口点
│   └── utils.py          # 附加模块
├── lib/                  # 捆绑的Python包
├── requirements.txt      # 可选：Python依赖列表
└── icon.png              # 可选：扩展图标

桌面扩展中唯一必需的文件是manifest.json。Claude Desktop处理所有复杂性：

清单包含人类可读的信息（如名称、描述或作者）、功能声明（工具、提示）、用户配置和运行时要求。大多数字段是可选的，因此最小版本非常简短，但实际上，我们期望所有三种支持的扩展类型（Node.js、Python和经典二进制文件/可执行文件）都包含文件：

{
  "mcpb_version": "0.1",                    // 此清单符合的MCPB规范版本
  "name": "my-extension",                   // 机器可读名称（用于CLI、API）
  "version": "1.0.0",                       // 扩展的语义版本
  "description": "A simple MCP extension",  // 扩展功能的简要描述
  "author": {                               // 作者信息（必需）
    "name": "Extension Author"              // 作者姓名（必需字段）
  },
  "server": {                               // 服务器配置（必需）
    "type": "node",                         // 服务器类型："node"、"python"或"binary"
    "entry_point": "server/index.js",       // 主服务器文件的路径
    "mcp_config": {                         // MCP服务器配置
      "command": "node",                    // 运行服务器的命令
      "args": [                             // 传递给命令的参数
        "${__dirname}/server/index.js"      // ${__dirname}被替换为扩展的目录
      ]                              
    }
  }
}

清单规范中提供了许多便利选项，旨在使本地MCP服务器的安装和配置更加容易。服务器配置对象可以以一种方式定义，既为用户定义的配置留出空间（以模板字面量的形式），也为平台特定的覆盖留出空间。扩展开发者可以详细定义他们想要从用户那里收集什么样的配置。

让我们看一个具体的例子，说明清单如何帮助配置。在下面的清单中，开发者声明用户需要提供api_key。Claude不会启用该扩展，直到用户提供该值，将其自动保存在操作系统的密钥库中，并在启动服务器时透明地将${user_config.api_key}替换为用户提供的值。类似地，${__dirname}将被替换为扩展解包目录的完整路径。

{
  "mcpb_version": "0.1",
  "name": "my-extension",
  "version": "1.0.0",
  "description": "A simple MCP extension",
  "author": {
    "name": "Extension Author"
  },
  "server": {
    "type": "node",
    "entry_point": "server/index.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server/index.js"],
      "env": {
        "API_KEY": "${user...key}"
      }
    }
  },
  "user_config": {
    "api_key": {
      "type": "string",
      "title": "API Key",
      "description": "Your API key for authentication",
      "sensitive": true,
      "required": true
    }
  }
}

带有大多数可选字段的完整manifest.json可能如下所示：

{
  "mcpb_version": "0.1",
  "name": "My MCP Extension",
  "display_name": "My Awesome MCP Extension",
  "version": "1.0.0",
  "description": "A brief description of what this extension does",
  "long_description": "A detailed description that can include multiple paragraphs explaining the extension's functionality, use cases, and features. It supports basic markdown.",
  "author": {
    "name": "Your Name",
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
      "description": "Search for files in a directory"
    }
  ],
  "prompts": [
    {
      "name": "poetry",
      "description": "Have the LLM write poetry",
      "arguments": ["topic"],
      "text": "Write a creative poem about the following topic: ${arguments.topic}"
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
      "title": "Allowed Directories",
      "description": "Directories the server can access",
      "multiple": true,
      "required": true,
      "default": ["${HOME}/Desktop"]
    },
    "api_key": {
      "type": "string",
      "title": "API Key",
      "description": "Your API key for authentication",
      "sensitive": true,
      "required": false
    },
    "max_file_size": {
      "type": "number",
      "title": "Maximum File Size (MB)",
      "description": "Maximum file size to process",
      "default": 10,
      "min": 1,
      "max": 100
    }
  }
}

要查看扩展和清单，请参阅MCPB仓库中的示例。

所有必需和可选字段的完整规范可以在我们的开源工具链中找到。

构建您的第一个扩展

让我们走过将现有MCP服务器打包为桌面扩展的过程。我们将使用一个简单的文件系统服务器作为示例。

步骤1：创建清单

首先，为您的服务器初始化一个清单：

npx @anthropic-ai/mcpb init

这个交互式工具会询问您的服务器信息并生成完整的manifest.json。如果您想快速获得最基本的manifest.json，可以使用--yes参数运行该命令。

步骤2：处理用户配置

如果您的服务器需要用户输入（如API密钥或允许的目录），请在清单中声明：

"user_config": {
  "allowed_directories": {
    "type": "directory",
    "title": "Allowed Directories",
    "description": "Directories the server can access",
    "multiple": true,
    "required": true,
    "default": ["${HOME}/Documents"]
  }
}

Claude Desktop将：

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

步骤3：打包扩展

将所有内容打包成.mcpb文件：

npx @anthropic-ai/mcpb pack

此命令：

步骤4：本地测试

将您的.mcpb文件拖入Claude Desktop的设置窗口。您将看到：

高级功能

跨平台支持

扩展可以适应不同的操作系统：

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

动态配置

使用模板字面量获取运行时值：

功能声明

帮助用户提前了解功能：

"tools": [
  {
    "name": "read_file",
    "description": "Read contents of a file"
  }
],
"prompts": [
  {
    "name": "code_review",
    "description": "Review code for best practices",
    "arguments": ["file_path"]
  }
]

扩展目录

我们正在推出一个内置于Claude Desktop的策划扩展目录。用户可以浏览、搜索和一键安装——无需搜索GitHub或审查代码。

虽然我们期望桌面扩展规范以及Claude for macOS和Windows中的实现会随着时间推移而发展，但我们期待看到扩展以多种方式用于扩展Claude能力的有创意的方式。

要提交您的扩展：

构建开放的生态系统

我们致力于围绕MCP服务器的开放生态系统，并相信其被多个应用程序和服务普遍采用的能力使用户受益。遵循这一承诺，我们正在开源桌面扩展规范、工具链以及Claude for macOS和Windows用于实现其自身桌面扩展支持的关键架构和功能。我们希望MCPB格式不仅能为Claude提供更好的本地MCP服务器可移植性，也能为其他AI桌面应用程序提供支持。

我们正在开源：

这意味着：

规范和工具链故意被版本化为0.1，因为我们期待与更大的社区合作来发展和改变格式。我们期待收到您的反馈。

安全和 enterprise 考虑

我们理解扩展引入了新的安全考虑，特别是对于企业。我们为桌面扩展的预览版本内置了几项安全措施：

对于用户

对于企业

有关如何在组织内管理扩展的更多信息，请参阅我们的文档。

入门

准备好构建自己的扩展了吗？以下是入门方法：

对于MCP服务器开发者：查看我们的开发者文档——或者通过在本地MCP服务器目录中运行以下命令来直接开始：

npm install -g @anthropic-ai/mcpb
mcpb init
mcpb pack

对于Claude Desktop用户：更新到最新版本并在设置中寻找扩展部分

对于企业：查看我们的enterprise文档以了解部署选项

使用Claude Code构建

在Anthropic内部，我们发现Claude非常擅长在最少干预的情况下构建扩展。如果您也想使用Claude Code，我们建议您简要说明您希望扩展做什么，然后将以下上下文添加到提示中：

我想将其构建为桌面扩展，简称"MCPB"。请按照以下步骤操作：

1. **仔细阅读规范：**
   - https://github.com/anthropics/mcpb/blob/main/README.md - MCPB架构概述、功能和集成模式
   - https://github.com/anthropics/mcpb/blob/main/MANIFEST.md - 完整的扩展清单结构和字段定义
   - https://github.com/anthropics/mcpb/tree/main/examples - 包括"Hello World"示例的参考实现

2. **创建正确的扩展结构：**
   - 按照MANIFEST.md规范生成有效的manifest.json
   - 使用@modelcontextprotocol/sdk实现具有正确工具定义的MCP服务器
   - 包含适当的错误处理和超时管理

3. **遵循最佳开发实践：**
   - 通过stdio传输实现正确的MCP协议通信
   - 用清晰的模式、验证和一致的JSON响应构建工具
   - 利用此扩展将在本地运行的事实
   - 添加适当的日志记录和调试功能
   - 包含适当的文档和设置说明

4. **测试注意事项：**
   - 验证所有工具调用返回正确结构化的响应
   - 验证清单加载正确且主机集成工作

生成完整的、生产就绪的代码，可以立即测试。专注于防御性编程、清晰的错误消息和遵循确切的MCPB规范以确保与生态系统的兼容性。

结论

桌面扩展代表了用户与本地AI工具交互方式的根本性转变。通过消除安装摩擦，我们使强大的MCP服务器对每个人都可以访问——而不仅仅是开发者。

在内部，我们使用桌面扩展来共享高度实验性的MCP服务器——有些有趣，有些有用。一个团队进行了实验，看看我们的模型直接连接到GameBoy时能走多远，类似于我们的"Claude玩宝可梦"研究。我们使用桌面扩展打包了一个单一扩展，打开了流行的PyBoy GameBoy模拟器并让Claude控制它。我们相信无数机会存在，可以将模型的能力与用户本地机器上已有的工具、数据和应用程序连接起来。

我们迫不及待地想看到您构建的内容。同样带来数千个MCP服务器的创造力现在只需一次点击就能触达数百万用户。准备好分享您的MCP服务器了吗？提交您的扩展以供审核。

想要了解更多？
