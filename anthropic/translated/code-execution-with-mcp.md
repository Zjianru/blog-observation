---
title: "使用MCP进行代码执行：构建更高效的代理"
subtitle: "发布日期：2025年11月4日"
date: ""
source: "https://www.anthropic.com/engineering/code-execution-with-mcp"
---

模型上下文协议（MCP）是一个将AI代理连接到外部系统的开放标准。将代理连接到工具和数据传统上需要为每个配对创建自定义集成，造成碎片化和重复努力，使扩展真正连接的系统变得困难。MCP提供了一个通用协议——开发者只需在代理中实现一次MCP，就可以解锁整个集成生态系统。

自2024年11月推出MCP以来，采用速度很快：社区已经构建了数千个MCP服务器，SDK可用于所有主要编程语言，行业已将MCP作为将代理连接到工具和实施数据的实际标准。

如今开发者通常构建可以访问数十个MCP服务器上的数百或数千个工具的代理。然而，随着连接工具数量的增长，预先加载所有工具定义并将中间结果传递通过上下文窗口会减慢代理速度并增加成本。

在这篇博客中，我们将探讨代码执行如何使代理能够更高效地与MCP服务器交互，在使用更少tokens的同时处理更多工具。

工具导致的过度token消耗使代理效率降低

随着MCP使用规模的扩大，有两种常见模式会增加代理成本和延迟：

1. 工具定义使上下文窗口过载

大多数MCP客户端将所有工具定义直接加载到上下文中，使用直接工具调用语法向模型公开。这些工具定义可能如下所示：

gdrive.getDocument
     描述：从Google Drive检索文档
     参数：
                documentId (必需，字符串)：要检索的文档的ID
                fields (可选，字符串)：要返回的特定字段
     返回：带有标题、正文内容、元数据、权限等的文档对象

```

salesforce.updateRecord
    描述：在Salesforce中更新记录
    参数：
               objectType (必需，字符串)：Salesforce对象类型（Lead、Contact、Account等）
               recordId (必需，字符串)：要更新的记录的ID
               data (必需，对象)：要使用新值更新的字段
     返回：带有确认的更新记录对象

```

工具描述占用更多上下文窗口空间，增加响应时间和成本。在代理连接到数千个工具的情况下，它们需要在读取请求之前处理数十万个tokens。

2. 中间工具结果消耗额外tokens

大多数MCP客户端允许模型直接调用MCP工具。例如，您可能问您的代理："从Google Drive下载我的会议记录并附加到Salesforce潜在客户。"

模型会发出如下调用：

TOOL CALL: gdrive.getDocument(documentId: "abc123")
        → 返回 "讨论了Q4目标...\n[完整记录文本]"
           （加载到模型上下文中）

TOOL CALL: salesforce.updateRecord(
			objectType: "SalesMeeting",
			recordId: "00Q5f000001abcXYZ",
 			data: { "Notes": "讨论了Q4目标...\n[完整记录文本写出]" }
		)
		（模型需要再次将整个记录文本写入上下文）

```

每个中间结果都必须通过模型。在这个示例中，完整的会议记录要经过两次处理。对于2小时的销售会议，这可能意味着处理额外的50,000个tokens。更大的文档甚至可能超过上下文窗口限制，破坏工作流。

对于大型文档或复杂数据结构，模型在工具调用之间复制数据时更容易出错。

MCP客户端将工具定义加载到模型的上下文窗口中，并编排一个消息循环，其中每个工具调用和结果在操作之间通过模型传递。

使用MCP进行代码执行提高上下文效率

随着代码执行环境对代理变得越来越常见，一个解决方案是将MCP服务器呈现为代码API而不是直接工具调用。然后代理可以编写代码与MCP服务器交互。这种方法同时解决了两个挑战：代理可以只加载它们需要的工具，并在将结果传递回模型之前在执行环境中处理数据。

有很多方法可以做到这一点。一种方法是从连接的MCP服务器生成所有可用工具的文件树。使用TypeScript的实现如下：

servers
├── google-drive
│   ├── getDocument.ts
│   ├── ... (其他工具)
│   └── index.ts
├── salesforce
│   ├── updateRecord.ts
│   ├── ... (其他工具)
│   └── index.ts
└── ... (其他服务器)

```

然后每个工具对应一个文件，如下所示：

// ./servers/google-drive/getDocument.ts
import { callMCPTool } from "../../../client.js";

interface GetDocumentInput {
  documentId: string;
}

interface GetDocumentResponse {
  content: string;
}

/* 从Google Drive读取文档 */
export async function getDocument(input: GetDocumentInput): Promise<GetDocumentResponse> {
  return callMCPTool<GetDocumentResponse>('google_drive__get_document', input);
}

```

我们上面的Google Drive到Salesforce示例变成以下代码：

// 从Google Docs读取记录并添加到Salesforce潜在客户
import * as gdrive from './servers/google-drive';
import * as salesforce from './servers/salesforce';

const transcript = (await gdrive.getDocument({ documentId: 'abc123' })).content;
await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { Notes: transcript }
});

```

代理通过探索文件系统来发现工具：列出./servers/目录以找到可用的服务器（如google-drive和salesforce），然后读取它需要特定工具文件（如getDocument.ts和updateRecord.ts）以了解每个工具的接口。这让代理只加载当前任务所需的定义。这将token使用从150,000个tokens减少到2,000个——时间和成本节省98.7%。

```

```

Cloudflare发布了类似的研究结果，称使用MCP进行代码执行为"代码模式"。核心洞察是相同的：LLM擅长编写代码，开发者应该利用这一优势来构建更高效地与MCP服务器交互的代理。

使用MCP进行代码执行的好处

使用MCP进行代码执行使代理能够通过按需加载工具、在数据到达模型之前进行过滤，并在单个步骤中执行复杂逻辑来更高效地使用上下文。使用这种方法还有安全和状态管理的好处。

渐进式披露

模型擅长导航文件系统。将工具呈现为文件系统上的代码允许模型按需读取工具定义，而不是预先全部读取。

或者，可以向服务器添加search_tools工具来查找相关定义。例如，当使用上面使用的假设Salesforce服务器时，代理搜索"salesforce"，只加载那些它需要用于当前任务的工具。在search_tools工具中包含一个detail_level参数，允许代理选择所需的详细程度（如仅名称、名称和描述，或带有模式的完整定义）也有助于代理节省上下文并有效地找到工具。

```

上下文高效的工具有结果

在处理大型数据集时，代理可以在代码中过滤和转换结果后再返回。考虑获取10,000行电子表格：

// 没有代码执行——所有行都通过上下文流动
TOOL CALL: gdrive.getSheet(sheetId: 'abc123')
        → 在上下文中返回10,000行以手动过滤

// 使用代码执行——在执行环境中过滤
const allRows = await gdrive.getSheet({ sheetId: 'abc123' });
const pendingOrders = allRows.filter(row => 
  row["Status"] === 'pending'
);
console.log(`Found ${pendingOrders.length} pending orders`);
console.log(pendingOrders.slice(0, 5)); // 仅记录前5行以供审查

```

代理看到五行而不是10,000行。类似的模式适用于聚合、跨多个数据源的连接或提取特定字段——所有这些都不会膨胀上下文窗口。

更强大且上下文高效的控制流

循环、条件语句和错误处理可以使用熟悉的代码模式来完成，而不是链接单独的工具调用。例如，如果您需要在Slack中发送部署通知，代理可以编写：

let found = false;
while (!found) {
  const messages = await slack.getChannelHistory({ channel: 'C123456' });
  found = messages.some(m => m.text.includes('deployment complete'));
  if (!found) await new Promise(r => setTimeout(r, 5000));
}
console.log('Deployment notification received');

```

这种方法比通过代理循环交替使用MCP工具调用和睡眠命令更高效。

此外，能够编写一个被执行的条件树也节省了"到第一个token"的延迟：代理不必等待模型评估if语句，而是可以让代码执行环境来处理这个。

隐私保护操作

当代理使用MCP进行代码执行时，中间结果默认保留在执行环境中。这样，代理只看到您明确记录或返回的内容，这意味着您不希望与模型共享的数据可以流经您的工作流，而不会进入模型的上下文。

对于更敏感的工作负载，代理框架可以自动对敏感数据进行分词。例如，假设您需要将客户联系详情从电子表格导入Salesforce。代理编写：

const sheet = await gdrive.getSheet({ sheetId: 'abc123' });
for (const row of sheet.rows) {
  await salesforce.updateRecord({
    objectType: 'Lead',
    recordId: row.salesforceId,
    data: { 
      Email: row.email,
      Phone: row.phone,
      Name: row.name
    }
  });
}
console.log(`Updated ${sheet.rows.length} leads`);

```

MCP客户端在数据到达模型之前拦截数据并对其进行分词：

// 代理会看到的内容，如果它记录了sheet.rows:
[
  { salesforceId: '00Q...', email: '[EMAIL_1]', phone: '[PHONE_1]', name: '[NAME_1]' },
  { salesforceId: '00Q...', email: '[EMAIL_2]', phone: '[PHONE_2]', name: '[NAME_2]' },
  ...
]

```

然后，当数据在另一个MCP工具调用中共享时，它通过MCP客户端中的查找进行反分词。真实的电子邮件地址、电话号码和姓名从Google Sheets流向Salesforce，但从不通过模型。这防止代理意外记录或处理敏感数据。您也可以使用此功能定义确定性安全规则，选择数据可以流向和来自何处。

状态持久化和技能

具有文件系统访问权限的代码执行允许代理在操作之间维护状态。代理可以将中间结果写入文件，使它们能够恢复工作并跟踪进度：

const leads = await salesforce.query({ 
  query: 'SELECT Id, Email FROM Lead LIMIT 1000' 
});
const csvData = leads.map(l => `${l.Id},${l.Email}`).join('\n');
await fs.writeFile('./workspace/leads.csv', csvData);

// 稍后执行从停止的地方继续
const saved = await fs.readFile('./workspace/leads.csv', 'utf-8');

```

代理还可以将它们自己的代码持久化为可重用函数。一旦代理为一个任务开发了工作代码，它可以保存该实现以供将来使用：

// 在 ./skills/save-sheet-as-csv.ts
import * as gdrive from './servers/google-drive';
export async function saveSheetAsCsv(sheetId: string) {
  const data = await gdrive.getSheet({ sheetId });
  const csv = data.map(row => row.join(',')).join('\n');
  await fs.writeFile(`./workspace/sheet-${sheetId}.csv`, csv);
  return `./workspace/sheet-${sheetId}.csv`;
}

// 稍后在任何代理执行中：
import { saveSheetAsCsv } from './skills/save-sheet-as-csv';
const csvPath = await saveSheetAsCsv('abc123');

```

这与技能的概念紧密相关，技能是用于模型的可重用指令、脚本和资源的文件夹，以提高在专业任务上的性能。向这些保存的函数添加SKILL.md文件会创建一个结构化的技能，模型可以引用和使用。随着时间的推移，这允许您的代理构建一个更高级能力的工具箱，逐步改进它最有效地工作所需的脚手架。

请注意，代码执行引入了自己的复杂性。运行代理生成的代码需要一个安全的执行环境，具有适当的沙箱、资源限制和监控。这些基础设施要求增加了直接工具调用避免的运营开销和安全考虑。代码执行的好处——减少token成本、更低延迟和改进的工具组合——应与这些实施成本进行权衡。

总结

MCP为代理连接许多工具和系统提供了基础协议。然而，一旦连接了太多服务器，工具定义和结果可能会消耗过多tokens，降低代理效率。

虽然这里的许多问题感觉是新颖的——上下文管理、工具组合、状态持久化——但它们都有来自软件工程的已知解决方案。代码执行将这些成熟的模式应用于代理，让它们使用熟悉的编程构造来更高效地与MCP服务器交互。如果您实施这种方法，我们鼓励您与MCP社区分享您的发现。

致谢

本文由Adam Jones和Conor Kelly撰写。感谢Jeremy Fox、Jerome Swannack、Stuart Ritchie、Molly Vorwerck、Matt Samuels和Maggie Vo对本文草稿的反馈。
