系统地用 Evals 测试代理技能

A practical guide to turning agent skills into something you can test, score, and improve over time.

作者：Dominik Kundel、Gabriel Chua

当你正在迭代像 Codex 这样的代理的技能时，很难判断你是否真的在改进它或者只是在改变它的行为。一个版本感觉更快，另一个似乎更可靠，然后回归悄悄出现：技能没有触发，它跳过一个必需的步骤，或者它留下多余的文件。

从本质上讲，技能是为 LLM 提供的有组织的提示和指令集合。随着时间推移改进技能最可靠的方法是与你评估任何其他 LLM 应用提示的方式相同。

Evals（评估的简称）检查模型的输出以及它为产生输出而采取的步骤是否符合你的预期。不是问"这感觉更好吗？"（或依靠直觉），evals 让你问具体问题，比如：

代理是否调用了技能？
它是否运行了预期的命令？
它是否产生了符合你关心的约定的输出？

具体来说，一个 eval 是：提示 → 捕获的运行（追踪 + 产物）→ 一小套检查 → 一个你可以随时间比较的分数。

在实践中，代理技能的 evals 看起来很像轻量级端到端测试：你运行代理，记录发生的事情，并根据一小套规则对结果打分。

这篇文章通过 Codex 带你了解一个清晰的模式，从定义成功开始，然后添加确定性检查和基于评分标准的分级，以便改进（和回归）是清晰的。

1. 在写技能之前定义成功

在编写技能本身之前，用你可以实际测量的术语写下"成功"的含义。思考这个问题的一个有用方式是将你的检查分成几类：

结果目标：任务完成了吗？应用运行了吗？
流程目标：Codex 是否调用了技能并遵循你预期的工具和步骤？
风格目标：输出是否符合你要求的约定？
效率目标：它是否在不折腾的情况下到达（例如，不必要的命令或过多 token 使用）？

保持这个列表小而专注于必须通过的检查。目标不是预先编码每个偏好，而是捕获你最关心的行为。

在本文中，例如，指南评估了一个设置演示应用的技能。一些检查是具体的。它运行了 npm install 吗？它创建了 package.json 吗？指南将这些与结构化风格评分标准配对，以评估约定和布局。

这种混合是有意的。你需要快速、有针对性的信号来早期发现特定回归，而不是在最后得到单一通过/失败判定。

2. 创建技能

Codex 技能是一个包含 SKILL.md 文件的目录，其中包括 YAML 前置事项（名称、描述），然后是定义技能行为的 Markdown 指令以及可选资源和脚本。名称和描述比看起来更重要。它们是 Codex 用来决定是否调用技能以及何时将 SKILL.md 的其余部分注入代理上下文的原始信号。如果这些模糊或重载，技能将无法可靠触发。

最快的入门方法是使用 Codex 内置的技能创建器（它本身也是一个技能）。它引导你：

$skill-creator

创建器询问你技能做什么，什么时候应该触发，以及它是指令式还是脚本支持（指令式是默认建议）。要了解有关创建技能的更多信息，请查看文档。

一个示例技能

这篇文章使用了一个有意的最小示例：一个以可预测、可重复方式设置小型 React 演示应用的技能。

该技能将：

使用 Vite 的 React + TypeScript 模板脚手架项目
使用官方 Vite 插件方法配置 Tailwind CSS
强制执行最小、一致的文件结构
定义清晰的"完成定义"，以便成功易于评估

以下是一个紧凑的草稿，你可以粘贴到：

.codex/skills/setup-demo-app/SKILL.md（仓库范围），或
~/.codex/skills/setup-demo-app/SKILL.md（用户范围）。

---
name: setup-demo-app
description: Scaffold a Vite + React + Tailwind demo app with a small, consistent project structure.
---

## 何时使用

![](images/eval-skills_00.png)

当需要一个新鲜的演示应用进行快速 UI 实验或复现时使用。

## 构建什么

创建一个 Vite React TypeScript 应用并配置 Tailwind。保持最小化。

设置后的项目结构：

- src/
  - main.tsx（入口）
  - App.tsx（根 UI）
  - components/
    - Header.tsx
    - Card.tsx
  - index.css（Tailwind 导入）
- index.html
- package.json

风格要求：

- TypeScript 组件
- 仅使用函数组件
- 使用 Tailwind 类进行样式设计（无 CSS 模块）
- 无额外的 UI 库

## 步骤

1. 使用 React TS 模板通过 Vite 脚手架：
   npm create vite@latest demo-app -- --template react-ts

2. 安装依赖：
   cd demo-app
   npm install

3. 使用 Vite 插件安装和配置 Tailwind。
   - npm install tailwindcss @tailwindcss/vite
   - 将 tailwind 插件添加到 vite.config.ts
   - 在 src/index.css 中，将内容替换为：
     @import "tailwindcss";

4. 实现最小 UI：
   - Header：应用标题和简短副标题
   - Card：可重用的卡片容器
   - App：渲染 Header + 2 个带有占位符文本的 Card

## 完成定义

- npm run dev 成功启动
- package.json 存在
- src/components/Header.tsx 和 src/components/Card.tsx 存在

这个示例技能故意采取固执己见的立场。没有明确的约束，就没有具体的东西可以评估。

3. 手动触发技能以暴露隐藏的假设

因为技能调用很大程度上取决于 SKILL.md 中的名称和描述，第一件要检查的事情是 setup-demo-app 技能是否在你期望时触发。

早期，明确激活技能，通过 /skills 斜杠命令或使用 $ 前缀引用它，在真实仓库或临时目录中，并观察它在哪里中断。这是你发现错误的地方：技能根本不触发、太热情地触发，或者运行但偏离预期步骤的情况。

在这个阶段，你不是在优化速度或抛光。你正在寻找技能做出的隐藏假设，例如：

触发假设：像"设置一个快速 React 演示"这样的提示应该调用 setup-demo-app 但没有，或者更通用的提示（"添加 Tailwind 样式"）无意间触发了它。

环境假设：技能假设它在空目录中运行，或者 npm 可用且比其他包管理器更受欢迎。

执行假设：代理跳过 npm install，因为它假设依赖已经安装，或者在 Vite 项目存在之前配置 Tailwind。

一旦你准备好使这些运行可重复，切换到 codex exec。它专为自动化和 CI 设计：它将进度流式传输到 stderr，只将最终结果写入 stdout，这使得运行更容易脚本化、捕获和检查。

默认情况下，codex exec 在受限沙盒中运行。如果你的任务需要写文件，使用 --full-auto 运行。作为一般规则，尤其是在自动化时，使用完成任务所需的最小权限。

一个基本的手动运行可能如下：

codex exec --full-auto \
  'Use the $setup-demo-app skill to create the project in this directory.'

这第一次动手通过更多是关于验证正确性而不是发现边缘情况。你在这里做的每个手动修复，例如添加缺少的 npm install、更正 Tailwind 设置或收紧触发描述，都是未来 eval 的候选者，这样你就可以在大规模评估之前锁定预期行为。

4. 使用小而有针对性的提示集来早期发现回归

你不需要大型基准来从 evals 中获取价值。对于单个技能，10-20 个提示的小集合足以早期发现回归并确认改进。

从一个小的 CSV 开始，随着你在开发或使用过程中遇到真实失败时逐渐增加。每一行应该代表你关心 setup-demo-app 技能是否激活的情况，以及当它激活时成功是什么样的。

例如，初始 evals/setup-demo-app.prompts.csv 可能看起来像这样：

id,should_trigger,prompt
test-01,true,"Create a demo app named `devday-demo` using the $setup-demo-app skill"
test-02,true,"Set up a minimal React demo app with Tailwind for quick UI experiments"
test-03,true,"Create a small demo app to showcase the Responses API"
test-04,false,"Add Tailwind styling to my existing React app"

这些案例中的每一个都测试略有不同的东西：

显式调用（test-01）
此提示直接命名技能。它确保 Codex 可以在被要求时调用 setup-demo-app，并且技能名称、描述或指令的更改不会破坏直接使用。

隐式调用（test-02）
此提示准确描述技能针对的场景，设置最小的 React + Tailwind 演示，而不提及技能名称。它测试 SKILL.md 中的名称和描述是否足够强，以便 Codex 自己选择技能。

上下文调用（test-03）
此提示添加了域上下文（Responses API），但仍需要相同的底层设置。它检查技能在真实的、稍微嘈杂的提示中是否触发，以及生成的应用是否仍然符合预期的结构和约定。

负面对照（test-04）
此提示不应调用 setup-demo-app。这是一个常见的相邻请求（"将 Tailwind 添加到现有应用"），可能无意间匹配技能的描述（"React + Tailwind 演示"）。包含至少一个 should_trigger=false 案例有助于捕获误报，即 Codex 太热情地选择技能并在用户想要对现有应用进行增量更改时脚手架一个新项目。

这种混合是有意的。一些 evals 应该确认技能在显式调用时表现正确；其他则应该检查它在用户根本不提及技能的现实提示中激活。

当你发现错误、未能触发技能的提示或输出偏离你期望的情况时，将它们添加为新行。随着时间的推移，这个小 CSV 成为了 setup-demo-app 技能必须继续正确的场景的活记录。

5. 使用轻量级确定性评分器入门

这是评估步骤的核心：使用 codex exec --json 这样你的 eval 工具可以评估实际发生了什么，而不仅仅是最终输出看起来是否正确。

当你启用 --json 时，stdout 变成结构化事件的 JSONL 流。这使得编写与你关心的行为直接相关的确定性检查变得直接，例如：

它运行了 npm install 吗？
它创建了 package.json 吗？
它是否以预期顺序调用了预期的命令？

这些检查故意是轻量级的。它们在你添加任何基于模型的评分之前给你快速、可解释的信号。

一个最小的 Node.js 运行器

一个"足够好"的方法如下：

对于每个提示，运行 codex exec --json --full-auto "<prompt>"
将 JSONL 追踪保存到磁盘
解析追踪并对事件运行确定性检查

// evals/run-setup-demo-app-evals.mjs
import { spawnSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import path from "node:path";

function runCodex(prompt, outJsonlPath) {
  const res = spawnSync(
    "codex",
    [
      "exec",
      "--json", // REQUIRED: emit structured events
      "--full-auto", // Allow file system changes
      prompt,
    ],
    { encoding: "utf8" }
  );
  mkdirSync(path.dirname(outJsonlPath), { recursive: true });
  // stdout is JSONL when --json is enabled
  writeFileSync(outJsonlPath, res.stdout, "utf8");
  return { exitCode: res.status ?? 1, stderr: res.stderr };
}

function parseJsonl(jsonlText) {
  return jsonlText
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

// 确定性检查：代理是否运行了 `npm install`？
function checkRanNpmInstall(events) {
  return events.some(
    (e) =>
      (e.type === "item.started" || e.type === "item.completed") &&
      e.item?.type === "command_execution" &&
      typeof e.item?.command === "string" &&
      e.item.command.includes("npm install")
  );
}

// 确定性检查：`package.json` 是否被创建？
function checkPackageJsonExists(projectDir) {
  return existsSync(path.join(projectDir, "package.json"));
}

// 示例单案例运行
const projectDir = process.cwd();
const tracePath = path.join(projectDir, "evals", "artifacts", "test-01.jsonl");
const prompt =
  "Create a demo app named demo-app using the $setup-demo-app skill";
runCodex(prompt, tracePath);

const events = parseJsonl(readFileSync(tracePath, "utf8"));
console.log({
  ranNpmInstall: checkRanNpmInstall(events),
  hasPackageJson: checkPackageJsonExists(path.join(projectDir, "demo-app")),
});

这里的价值在于一切都是确定性的和可调试的。

如果检查失败，你可以打开 JSONL 文件并准确查看发生了什么。每个命令执行都显示为 item.* 事件，按顺序排列。这使得回归直接解释和修复，这正是你在这个阶段想要的。

6. 使用 Codex 和基于评分标准的分级进行定性检查

确定性检查回答"它做了基础工作吗？"但它们不回答"它是以你想要的方式做的吗？"

对于像 setup-demo-app 这样的技能，许多要求是定性的：组件结构、样式约定或 Tailwind 是否遵循预期的配置。这些很难用基本文件存在检查或命令计数来捕获。

一个务实的解决方案是在你的 eval 管道中添加第二个模型辅助步骤：

运行设置技能（这将代码写入磁盘）
对结果仓库运行只读样式检查
需要一个你的工具可以一致评分的结构化响应

Codex 通过 --output-schema 直接支持这一点，它将最终响应约束为你定义的 JSON Schema。

一个小的评分标准 schema

首先定义一个捕获你关心的检查的小 schema。例如，创建 evals/style-rubric.schema.json：

{
  "type": "object",
  "properties": {
    "overall_pass": { "type": "boolean" },
    "score": { "type": "integer", "minimum": 0, "maximum": 100 },
    "checks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "pass": { "type": "boolean" },
          "notes": { "type": "string" }
        },
        "required": ["id", "pass", "notes"],
        "additionalProperties": false
      }
    }
  },
  "required": ["overall_pass", "score", "checks"],
  "additionalProperties": false
}

这个 schema 给你稳定的字段（overall_pass、score、每次检查结果），你可以随时间组合、diff 和跟踪。

样式检查提示

接下来，运行第二个只检查仓库并发出符合评分标准 JSON 响应的 codex exec：

codex exec \
  "Evaluate the demo-app repository against these requirements:
   - Vite + React + TypeScript project exists
   - Tailwind is configured via @tailwindcss/vite and CSS imports tailwindcss
   - src/components contains Header.tsx and Card.tsx
   - Components are functional and styled with Tailwind utility classes (no CSS modules)
   Return a rubric result as JSON with check ids: vite, tailwind, structure, style." \
  --output-schema ./evals/style-rubric.schema.json \
  -o ./evals/artifacts/test-01.style.json

这就是 --output-schema 的方便之处。不是难以解析或比较的自由形式文本，你得到一个可预测的 JSON 对象，你的 eval 工具可以在多次运行中评分。

如果你后来将此 eval 套件移入 CI，Codex GitHub Action 明确支持通过 codex-args 传递 --output-schema，所以你可以在自动化工作流程中强制执行相同的结构化输出。

7. 随着技能成熟扩展你的 evals

一旦你有了核心循环，你可以在对你的技能最重要的方向上扩展你的 evals。从小开始，然后仅在增加真正信心的地方添加更深的检查。

一些例子包括：

命令计数和折腾：在 JSONL 追踪中计数 command_execution 项目，以捕获代理开始循环或重新运行命令时的回归。Token 使用量也可在 turn.completed 事件中获得。

Token 预算：跟踪 usage.input_tokens 和 usage.output_tokens 以发现意外的提示膨胀并在版本之间比较效率。

构建检查：技能完成后运行 npm run build。这充当更强的端到端信号，并捕获断开的导入或配置错误的工具。

运行时冒烟检查：启动 npm run dev 并用 curl 击中开发服务器，或者如果你已经有的话，运行一个轻量级 Playwright 检查。选择性地使用它。它增加了信心但需要时间。

仓库清洁度：确保运行不生成不需要的文件，git status --porcelain 是空的（或匹配明确的允许列表）。

沙盒和权限回归：验证技能仍然可以在不超出你预期的权限升级的情况下工作。一旦你自动化，最小权限默认值最重要。

模式是一致的：从解释行为的快速检查开始，然后仅在降低风险时添加更慢、更重的检查。

8. 关键要点

这个小的 setup-demo-app 示例展示了从"感觉更好"到"证明"的转变：运行代理，记录发生了什么，并用一小套检查对其进行评分。一旦那个循环存在，每个调整都更容易确认，每个回归都变得清晰。以下是关键要点：

测量重要的事情。好的 evals 使回归清晰，失败可解释。
从可检查的完成定义开始。使用 $skill-creator 引导，然后收紧指令直到成功是明确的。
以行为为基础。用 codex exec --json 捕获 JSONL 并对 command_execution 事件编写确定性检查。
在规则不足的地方使用 Codex。添加结构化的、基于评分标准的通过与 --output-schema 来可靠地评分风格和约定。
让真实失败驱动覆盖。每个手动修复都是一个信号。将其转换为测试，以便技能继续正确处理它。
