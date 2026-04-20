---
title: "在Claude开发者平台上推出高级工具使用功能"
subtitle: "发布日期：2025年11月24日"
date: ""
source: "https://www.anthropic.com/engineering/advanced-tool-use"
---

AI代理的未来是模型能够无缝地使用数百或数千个工具。一个集成git操作、文件操作、包管理器、测试框架和部署管道的IDE助手。一个同时连接Slack、GitHub、Google Drive、Jira、公司数据库和数十个MCP服务器的运营协调器。

为了构建有效的代理，它们需要使用无限制的工具库，而不会将每个定义都塞入上下文。我们在关于使用MCP进行代码执行的博客文章中讨论了工具结果和定义有时在代理读取请求之前可能消耗50,000+个tokens。代理应该按需发现和加载工具，只保留与当前任务相关的内容。

代理还需要从代码中调用工具的能力。当使用自然语言工具调用时，每次调用都需要一次完整的推理过程，中间结果堆积在上下文中，不管它们是否有用。代码是编排逻辑（如循环、条件语句和数据转换）的自然选择。代理需要根据手头的任务灵活选择代码执行和推理。

代理还需要从示例中学习正确的工具使用，而不仅仅是模式定义。JSON模式定义了什么是结构上有效的，但无法表达使用模式：何时包含可选参数、哪些组合有意义，或者您的API期望什么约定。

今天，我们发布三个功能来实现这一点：

在内部测试中，我们发现这些功能帮助我们构建了使用传统工具使用模式不可能实现的东西。例如，Excel版Claude使用编程工具调用来读取和修改包含数千行的电子表格，而不会使模型的上下文窗口过载。

基于我们的经验，我们相信这些功能为您使用Claude构建的内容开辟了新的可能性。

工具搜索工具

挑战

MCP工具定义提供重要的上下文，但随着更多服务器连接，这些tokens会累积。考虑一个五服务器设置：

那是58个工具，在对话开始之前就消耗了大约55K个tokens。添加更多服务器，如Jira（仅此一个就使用约17K个tokens），您很快就会接近100K+个tokens的开销。在Anthropic，我们看到工具定义在优化之前消耗了134K个tokens。

但令牌成本不是唯一的问题。最常见的失败是错误的工具选择和错误的参数，特别是当工具名称相似时，如notification-send-user与notification-send-channel。

```

```

我们的解决方案

工具搜索工具不是预先加载所有工具定义，而是按需发现工具。Claude只看到实际需要用于当前任务的工具。

工具搜索工具相比Claude传统方法的122,800个tokens保留了191,300个tokens的上下文。

传统方法：

使用工具搜索工具：

这代表了在保持对完整工具库访问的同时，token使用量减少85%。内部测试显示，在处理大型工具库时，MCP评估的准确性显著提高。Opus 4从49%提高到74%，Opus 4.5在使用工具搜索工具后从79.5%提高到88.1%。

工具搜索工具如何工作

工具搜索工具让Claude动态发现工具，而不是预先加载所有定义。您向API提供所有工具定义，但用defer_loading: true标记工具以使其可按需发现。延迟的工具最初不会加载到Claude的上下文中。Claude只看到工具搜索工具本身加上defer_loading: false的工具（您最关键、最常用的工具）。

```

```

当Claude需要特定功能时，它会搜索相关工具。工具搜索工具返回匹配工具的引用，这些引用在Claude的上下文中扩展为完整定义。

例如，如果Claude需要与GitHub交互，它会搜索"github"，只有github.createPullRequest和github.listIssues被加载——而不是您来Slack、Jira和Google Drive的其他50+个工具。

```

```

这样，Claude可以访问您的完整工具库，同时只支付实际需要的工具的token成本。

提示缓存说明：工具搜索工具不会破坏提示缓存，因为延迟的工具完全从初始提示中排除。它们只有在Claude搜索后才会添加到上下文中，因此您的系统提示和核心工具定义保持可缓存。

实施：

{
  "tools": [
    // 包含一个工具搜索工具（regex、BM25或自定义）
    {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},

    // 标记要按需发现的工具
    {
      "name": "github.createPullRequest",
      "description": "Create a pull request",
      "input_schema": {...},
      "defer_loading": true
    }
    // ... 数百个带有defer_loading: true的延迟工具
  ]
}

```

对于MCP服务器，您可以延迟加载整个服务器，同时保持特定的高使用工具加载：

{
  "type": "mcp_toolset",
  "mcp_server_name": "google-drive",
  "default_config": {"defer_loading": true}, # 延迟加载整个服务器
  "configs": {
    "search_files": {
"defer_loading": false
    }  // 保持最常用工具加载
  }
}

```

Claude开发者平台开箱即提供基于regex和BM25的搜索工具，但您也可以使用嵌入或其他策略实现自定义搜索工具。

何时使用工具搜索工具

像任何架构决策一样，启用工具搜索工具涉及权衡。该功能在工具调用之前添加了一个搜索步骤，因此当上下文节省和准确性改进超过额外延迟时，它提供最佳ROI。

在以下情况下使用：

在以下情况下收益较少：

编程工具调用

挑战

随着工作流变得越来越复杂， traditional tool calling创建了两个基本问题：

```

我们的解决方案

编程工具调用使Claude能够通过代码而不是通过单独的API往返来编排工具。不是让Claude一次请求一个工具，每个结果返回到其上下文，Claude编写调用多个工具、处理其输出并控制哪些信息实际进入其上下文窗口的代码。

Claude擅长编写代码，通过让它用Python表达编排逻辑而不是通过自然语言工具调用，您可以获得更可靠、更精确的控制流。循环、条件语句、数据转换和错误处理在代码中都是明确的，而不是隐含在Claude的推理中。

示例：预算合规检查

考虑一个常见的业务任务："哪些团队成员超出了Q3差旅预算？"

您有三个可用工具：

```

```

传统方法：

使用编程工具调用：

不是每个工具结果返回给Claude，Claude编写一个Python脚本来编排整个工作流。脚本在代码执行工具（沙盒环境）中运行，在需要工具结果时暂停。当您通过API返回工具结果时，它们由脚本处理，而不是由模型消耗。脚本继续执行，Claude只看到最终输出。

编程工具调用使Claude能够通过代码而不是通过单独的API往返来编排工具，允许并行工具执行。

以下是Claude为预算合规任务编写的编排代码的样子：

team = await get_team_members("engineering")

# 获取每个唯一级别的预算
levels = list(set(m["level"] for m in team))
budget_results = await asyncio.gather(*[
    get_budget_by_level(level) for level in levels
])

# 创建查找字典：{"junior": budget1, "senior": budget2, ...}
budgets = {level: budget for level, budget in zip(levels, budget_results)}

# 并行获取所有费用
expenses = await asyncio.gather(*[
    get_expenses(m["id"], "Q3") for m in team
])

# 找出超出差旅预算的员工
exceeded = []
for member, exp in zip(team, expenses):
    budget = budgets[member["level"]]
    total = sum(e["amount"] for e in exp)
    if total > budget["travel_limit"]:
        exceeded.append({
            "name": member["name"],
            "spent": total,
            "limit": budget["travel_limit"]
        })

print(json.dumps(exceeded))

```

Claude的上下文只接收最终结果：超出预算的两到三个人。2000+个明细项目、中间合计和预算查找不会影响Claude的上下文，将消耗从200KB的原始费用数据减少到仅1KB的结果。

效率提升是显著的：

生产工作流涉及杂乱的数据、条件逻辑和需要扩展的操作。编程工具调用让Claude以编程方式处理这些复杂性，同时将其注意力保持在可操作的结果而不是原始数据处理上。

编程工具调用如何工作

1. 将工具标记为可从代码调用

添加code_execution到工具，并设置allowed_callers以选择加入编程执行：

{
  "tools": [
    {
      "type": "code_execution_20250825",
      "name": "code_execution"
    },
    {
      "name": "get_team_members",
      "description": "Get all members of a department...",
      "input_schema": {...},
      "allowed_callers": ["code_execution_20250825"] # 选择加入编程工具调用
    },
    {
      "name": "get_expenses",
	...
    },
    {
      "name": "get_budget_by_level",
	...
    }
  ]
}

```

API将这些工具定义转换为Claude可以调用的Python函数。

2. Claude编写编排代码

不是一次请求一个工具，Claude生成Python代码：

{
  "type": "server_tool_use",
  "id": "srvtoolu_abc",
  "name": "code_execution",
  "input": {
    "code": "team = get_team_members('engineering')\n..." # 上面的代码示例
  }
}

```

3. 工具执行而不影响Claude的上下文

当代码调用get_expenses()时，您会收到一个带有caller字段的工具请求：

{
  "type": "tool_use",
  "id": "toolu_xyz",
  "name": "get_expenses",
  "input": {"user_id": "emp_123", "quarter": "Q3"},
  "caller": {
    "type": "code_execution_20250825",
    "tool_id": "srvtoolu_abc"
  }
}

```

您提供结果，该结果在代码执行环境中处理，而不是在Claude的上下文中处理。此请求-响应循环为代码中的每个工具调用重复。

4. 只有最终输出进入上下文

代码运行时，只有代码的结果返回给Claude：

{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_abc",
  "content": {
    "stdout": "[{\"name\": \"Alice\", \"spent\": 12500, \"limit\": 10000}...]"
  }
}

```

这就是Claude看到的全部，不是沿途处理的2000+个费用明细项目。

何时使用编程工具调用

编程工具调用为您的工作流添加了代码执行步骤。当token节省、延迟改进和准确性提高相当可观时，这个额外开销是值得的。

在以下情况下最有益：

在以下情况下收益较少：

工具使用示例

挑战

JSON模式擅长定义结构——类型、必需字段、允许的枚举——但它无法表达使用模式：何时包含可选参数、哪些组合有意义，或者您的API期望什么约定。

考虑一个支持工单API：

{
  "name": "create_ticket",
  "input_schema": {
    "properties": {
      "title": {"type": "string"},
      "priority": {"enum": ["low", "medium", "high", "critical"]},
      "labels": {"type": "array", "items": {"type": "string"}},
      "reporter": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "name": {"type": "string"},
          "contact": {
            "type": "object",
            "properties": {
              "email": {"type": "string"},
              "phone": {"type": "string"}
            }
          }
        }
      },
      "due_date": {"type": "string"},
      "escalation": {
        "type": "object",
        "properties": {
          "level": {"type": "integer"},
          "notify_manager": {"type": "boolean"},
          "sla_hours": {"type": "integer"}
        }
      }
    },
    "required": ["title"]
  }
}

```

该模式定义了什么是有效的，但留下了未解答的关键问题：

```

```

这些歧义可能导致格式错误的工具调用和不一致的参数使用。

我们的解决方案

工具使用示例让您可以直接在工具定义中提供示例工具调用。不是仅仅依赖模式，您向Claude展示具体的使用模式：

{
    "name": "create_ticket",
    "input_schema": { /* same schema as above */ },
    "input_examples": [
      {
        "title": "Login page returns 500 error",
        "priority": "critical",
        "labels": ["bug", "authentication", "production"],
        "reporter": {
          "id": "USR-12345",
          "name": "Jane Smith",
          "contact": {
            "email": "jane@acme.com",
            "phone": "+1-555-0123"
          }
        },
        "due_date": "2024-11-06",
        "escalation": {
          "level": 2,
          "notify_manager": true,
          "sla_hours": 4
        }
      },
      {
        "title": "Add dark mode support",
        "labels": ["feature-request", "ui"],
        "reporter": {
          "id": "USR-67890",
          "name": "Alex Chen"
        }
      },
      {
        "title": "Update API documentation"
      }
    ]
  }

```

从这三个示例中，Claude了解到：

在我们自己的内部测试中，工具使用示例将复杂参数处理的准确性从72%提高到90%。

何时使用工具使用示例

工具使用示例将tokens添加到您的工具定义中，因此当准确性提高超过额外成本时，它们最有价值。

在以下情况下最有益：

在以下情况下收益较少：

最佳实践

构建能够进行真实世界操作的代理意味着同时处理规模、复杂性和精确性。这三个功能共同解决工具使用工作流中的不同瓶颈。以下是如何有效组合它们。

战略性地分层功能

并非每个代理都需要对给定任务使用所有三个功能。从您最大的瓶颈开始：

这种专注方法让您解决限制代理性能的特定约束，而不是预先添加复杂性。

然后根据需要分层附加功能。它们是互补的：工具搜索工具确保找到正确的工具，编程工具调用确保高效执行，工具使用示例确保正确的调用。

为更好的发现设置工具搜索工具

工具搜索匹配名称和描述，因此清晰、描述性的定义可以提高发现准确性。

// 好
{
    "name": "search_customer_orders",
    "description": "Search for customer orders by date range, status, or total amount. Returns order details including items, shipping, and payment info."
}

// 差
{
    "name": "query_db_orders",
    "description": "Execute order query"
}

```

添加系统提示指导，让Claude知道可用的内容：

You have access to tools for Slack messaging, Google Drive file management, 
Jira ticket tracking, and GitHub repository operations. Use the tool search 
to find specific capabilities.

```

保持三到五个最常用的工具始终加载，其余延迟。这平衡了常用操作的即时访问和所有其他内容的按需发现。

为正确的执行设置编程工具调用

由于Claude编写代码来解析工具输出，因此要清楚地记录返回格式。这帮助Claude编写正确的解析逻辑：

{
    "name": "get_orders",
    "description": "Retrieve orders for a customer.
Returns:
    List of order objects, each containing:
    - id (str): Order identifier
    - total (float): Order total in USD
    - status (str): One of 'pending', 'shipped', 'delivered'
    - items (list): Array of {sku, quantity, price}
    - created_at (str): ISO 8601 timestamp"
}

```

有关受益于编程编排的选择加入工具，请参见下文。

为参数准确性设置工具使用示例

为行为清晰度制作示例：

入门

这些功能在beta中可用。要启用它们，添加beta header并包含您需要的工具：

client.beta.messages.create(
    betas=["advanced-tool-use-2025-11-20"],
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    tools=[
        {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
        {"type": "code_execution_20250825", "name": "code_execution"},
        # Your tools with defer_loading, allowed_callers, and input_examples
    ]
)

```

有关详细的API文档和SDK示例，请参阅我们的：

这些功能将工具使用从简单的函数调用转向智能编排。随着代理处理跨越数十个工具和大型数据集的更复杂工作流，动态发现、高效执行和可靠调用成为基础。

我们期待看到您构建的内容。

致谢

由Bin Wu撰写，感谢Adam Jones、Artur Renault、Henry Tay、Jake Noble、Noah Picard、Sam Jiang和Claude开发者平台团队的贡献。这项工作建立在Chris Gorgolewski、Daniel Jiang、Jeremy Fox和Mike Lambert的开创性研究之上。我们还从AI生态系统中汲取灵感，包括Joel Pobar的LLMVM、Cloudflare的代码模式和MCP代码执行。特别感谢Andy Schumeister、Hamish Kerr、Keir Bradwell、Matt Bleifer和Molly Vorwerck的支持。
