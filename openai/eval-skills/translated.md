# 系统化评估智能体技能：Evals 实践指南

来源：https://developers.openai.com/blog/eval-skills

---

当你为 Codex 这类智能体迭代优化某项技能时，往往难以判断改进是否真实有效，还是仅仅改变了其行为模式。某个版本感觉响应更快，另一版本似乎更稳定，但随后可能出现性能倒退：技能未被触发、遗漏必要步骤，或残留多余文件。

本质上，技能是面向大语言模型的[结构化提示与指令集合](https://developers.openai.com/codex/skills)。持续提升技能可靠性的最佳方式，是采用与[评估其他大语言模型应用提示](https://platform.openai.com/docs/guides/evaluation-best-practices)相同的标准化评估流程。

_Evals_（评估的简称）通过检验模型输出及其生成过程是否符合预期目标，将主观的“这个版本是否更好？”（或依赖直觉判断）转化为可量化的具体问题：

* 智能体是否成功调用了该技能？
* 是否执行了预期命令？
* 产出的结果是否符合你关注的规范？

具体而言，一次评估包含：输入提示 → 记录运行过程（轨迹与产物） → 执行少量检查项 → 生成可纵向对比的评分。

实践中，智能体技能评估类似于轻量级端到端测试：运行智能体，记录行为轨迹，并依据简明规则对结果进行评分。

本文将逐步演示 Codex 的标准化评估流程：从明确定义成功标准开始，逐步引入确定性检查与量规评分体系，使改进效果（与性能衰退）清晰可辨。

## 1. 编写技能前先定义成功标准

在开发具体技能前，首先用可量化的术语描述“成功”的定义。有效的分类方法是将检查项划分为几个维度：

*   **结果目标：** 任务是否完成？应用能否运行？
*   **过程目标：** Codex 是否调用了该技能并遵循了你预期的工具和步骤？
*   **风格目标：** 输出是否符合你要求的规范？
*   **效率目标：** 它是否在过程中没有出现反复折腾（例如，不必要的命令或过度的令牌使用）？

保持这份清单简短，并聚焦于必须通过的检查项。目标并非预先编码所有偏好，而是捕捉你最关心的行为。

例如，在这篇文章中，指南评估了一个用于设置演示应用的技能。有些检查是具体的：它运行了 `npm install` 吗？它创建了 `package.json` 吗？指南将这些检查与一个结构化的风格评估标准配对，以评估规范和布局。

这种混合是刻意的。你希望获得快速、有针对性的信号，以便尽早发现特定的回归问题，而不是在最后给出一个单一的通过/失败判定。

## 2\. 创建技能

一个 Codex 技能是一个包含 `SKILL.md` 文件的目录，该文件包含 YAML 前置元数据（`name`、`description`），后面是定义技能行为的 Markdown 指令，以及可选的资源和脚本。名称和描述的重要性可能超出你的想象。它们是 Codex 用来决定*是否*调用该技能以及*何时*将 `SKILL.md` 的其余部分注入到代理上下文中的主要信号。如果这些信息模糊或承载过多，技能将无法可靠触发。

最快的入门方法是使用 Codex 内置的技能创建器（[它本身也是一个技能](https://github.com/openai/skills/tree/main/skills/.system/skill-creator)）。它会引导你完成：

    $skill-creator

创建器会询问你该技能的作用、何时应触发，以及它是仅指令型还是脚本支持型（仅指令型是默认推荐）。要了解更多关于创建技能的信息，[请查阅文档](/codex/skills#create-a-skill)。

### 一个示例技能

本文使用了一个特意简化的示例：一个以可预测、可重复的方式设置小型 React 演示应用的技能。

该技能将：

* 使用 Vite 的 React + TypeScript 模板搭建项目脚手架
* 通过官方 Vite 插件方式配置 Tailwind CSS
* 强制采用最小化、一致的文件结构
* 明确定义"完成标准"，便于直观评估成果

以下为简洁草案，可粘贴至：

* `.codex/skills/setup-demo-app/SKILL.md`（仓库作用域），或
* `~/.codex/skills/setup-demo-app/SKILL.md`（用户作用域）

    ---
    name: setup-demo-app
    description: 搭建具有精简统一项目结构的 Vite + React + Tailwind 演示应用
    ---

    ## 使用场景

    适用于需要快速创建 UI 实验或问题复现的新演示应用。

    ## 构建目标

    创建 Vite React TypeScript 应用并配置 Tailwind。保持极简风格。

    搭建后的项目结构：

    - src/
      - main.tsx（入口文件）
      - App.tsx（根组件）
      - components/
        - Header.tsx
        - Card.tsx
      - index.css（Tailwind 导入文件）
    - index.html
    - package.json

    样式要求：

    - 使用 TypeScript 组件
    - 仅使用函数式组件
    - 采用 Tailwind 类进行样式设计（不使用 CSS 模块）
    - 不引入额外 UI 库

    ## 实施步骤

    1. 使用 Vite 的 React TS 模板搭建项目：
       npm create vite@latest demo-app -- --template react-ts

    2. 安装依赖：
       cd demo-app
       npm install

    3. 通过 Vite 插件安装配置 Tailwind：
       - npm install tailwindcss @tailwindcss/vite
       - 将 tailwind 插件添加至 vite.config.ts
       - 在 src/index.css 中替换内容为：
         @import "tailwindcss";

    4. 实现最小化 UI：
       - Header：应用标题与简短副标题
       - Card：可复用的卡片容器
       - App：渲染 Header 组件及 2 个含占位文本的 Card 组件

    ## 完成标准

    - npm run dev 成功启动
    - package.json 文件存在
    - src/components/Header.tsx 与 src/components/Card.tsx 文件存在

此示例技能刻意采用明确的技术主张。若无清晰约束，则无法进行具体评估。

## 3\. 手动触发技能以暴露隐藏假设

由于技能调用高度依赖于 `SKILL.md` 中的**名称**和**描述**，首要检查的是 `setup-demo-app` 技能是否在预期场景下被触发。

初期阶段，请通过 `/skills` 斜杠命令或使用 `$` 前缀引用该技能，在真实仓库或临时目录中显式激活它，并观察其执行中断的位置。这正是发现疏漏的关键环节：包括技能完全未被触发、触发过于频繁，或虽执行但偏离预设步骤的情况。

此阶段的目标并非追求速度或完善度，而是挖掘技能可能隐含的预设条件，例如：

  * **触发条件预设**：诸如“快速搭建 React 演示项目”这类本应触发 `setup-demo-app` 却未触发的指令，或“添加 Tailwind 样式”等过于泛化的指令意外触发该技能。

  * **环境预设**：技能默认在空目录中运行，或假定 `npm` 可用且优先于其他包管理器。

  * **执行流程预设**：智能体因假设依赖已安装而跳过 `npm install`，或在 Vite 项目创建前就配置 Tailwind。

当需要使这些运行过程可复现时，请切换到 `codex exec` 命令。该工具专为自动化和持续集成设计：它将执行进度流式输出至 `stderr`，仅将最终结果写入 `stdout`，从而更易于脚本化、捕获和检查运行过程。

默认情况下，`codex exec` 在受限沙箱中运行。若任务需写入文件，请使用 `--full-auto` 参数执行。作为通用原则，尤其在自动化场景中，应采用完成工作所需的最低权限。

基础手动运行示例如下：

    codex exec --full-auto \
      '使用 $setup-demo-app 技能在此目录中创建项目。'

这轮初步实践的重点不在于验证正确性，而在于发现边界情况。在此过程中进行的每次手动修正——无论是补充缺失的 `npm install`、修正 Tailwind 配置，还是收紧触发描述——都可能成为后续评估的候选案例，从而能在规模化评估前锁定预期行为。

## 4\. 使用少量针对性提示集及早发现回归问题

评估测试无需庞大基准也能创造价值。针对单一技能，仅需10–20条提示组成的小型测试集，就足以在早期暴露回归问题并验证改进效果。

建议从一个小型CSV文件开始，随着开发或使用过程中遇到实际故障案例逐步扩充。每一行应代表一个你关注的情境：需要验证`setup-demo-app`技能是否应当被触发，以及触发后的成功表现标准。

例如，初始的`evals/setup-demo-app.prompts.csv`文件可能如下所示：

    id,should_trigger,prompt
    test-01,true,"使用$setup-demo-app技能创建名为`devday-demo`的演示应用"
    test-02,true,"搭建包含Tailwind的极简React演示应用用于快速UI实验"
    test-03,true,"创建小型演示应用以展示Responses API功能"
    test-04,false,"为现有React应用添加Tailwind样式"

这些测试案例分别验证不同维度：

  * **显式调用测试（`test-01`）**
该提示直接指明技能名称。用于确保Codex在被明确要求时能正确调用`setup-demo-app`，并验证技能名称、描述或指令的修改不会破坏直接调用功能。

  * **隐式调用测试（`test-02`）**
该提示精确描述技能针对的场景（搭建React+Tailwind极简演示），但未提及技能名称。用于测试`SKILL.md`中的名称与描述是否足够清晰，使Codex能自主选择该技能。

  * **情境化调用测试（`test-03`）**
该提示添加了领域上下文（Responses API），但仍需要相同的基础搭建流程。用于验证技能在真实场景的轻度干扰提示中能否正常触发，并确保生成的应用仍符合预期的结构和规范。

*   **负向控制组（`test-04`）**
    此提示词**不应**调用 `setup-demo-app`。这是一个常见的相邻请求（“为现有应用添加 Tailwind”），可能会无意中匹配技能的描述（“React + Tailwind 演示”）。包含至少一个 `should_trigger=false` 的用例有助于捕捉**误报**，即 Codex 过于急切地选择了该技能，在用户只想对现有项目进行增量更改时，却搭建了一个新项目。

    这种混合是刻意的。一些评估应确认技能在被显式调用时行为正确；另一些则应检查技能在用户完全未提及该技能的真实世界提示词中是否被激活。

    当你发现遗漏（即未能触发技能的提示词）或输出偏离预期的案例时，将它们作为新行添加进来。久而久之，这个小型 CSV 文件就成为了 `setup-demo-app` 技能必须持续正确处理场景的动态记录。

    久而久之，这个小型数据集就成为了该技能必须持续正确处理内容的动态记录。

## 5\. 开始使用轻量级确定性评分器

这是评估步骤的核心：使用 `codex exec --json`，以便你的评估工具能够对**实际发生的情况**进行评分，而不仅仅是判断最终输出看起来是否正确。

当你启用 `--json` 时，`stdout` 会变成一个结构化事件的 JSONL 流。这使得编写直接关联到你关心行为的确定性检查变得非常直接，例如：

*   它运行了 `npm install` 吗？
*   它创建了 `package.json` 吗？
*   它是否以预期的顺序调用了预期的命令？

这些检查是特意设计为轻量级的。在你添加任何基于模型的评分之前，它们能为你提供快速、可解释的信号。

### 一个最小的 Node.js 运行器

一个“足够好”的方法如下所示：

1.  对于每个提示词，运行 `codex exec --json --full-auto "<prompt>"`
2.  将 JSONL 追踪记录保存到磁盘
3.  解析追踪记录并对事件运行确定性检查

    // evals/run-setup-demo-app-evals.mjs
    import { spawnSync } from "node:child_process";
    import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
    import path from "node:path";

function runCodex(prompt, outJsonlPath) {
  const res = spawnSync(
    "codex",
    [
      "exec",
      "--json", // 必需：输出结构化事件
      "--full-auto", // 允许文件系统更改
      prompt,
    ],
    { encoding: "utf8" }
  );

  mkdirSync(path.dirname(outJsonlPath), { recursive: true });

  // 启用 --json 时 stdout 为 JSONL 格式
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

// 确定性检查：是否创建了 `package.json`？
function checkPackageJsonExists(projectDir) {
  return existsSync(path.join(projectDir, "package.json"));
}

// 单次运行示例
const projectDir = process.cwd();
const tracePath = path.join(projectDir, "evals", "artifacts", "test-01.jsonl");

const prompt =
  "使用 $setup-demo-app 技能创建一个名为 demo-app 的演示应用";

runCodex(prompt, tracePath);

const events = parseJsonl(readFileSync(tracePath, "utf8"));

console.log({
  ranNpmInstall: checkRanNpmInstall(events),
  hasPackageJson: checkPackageJsonExists(path.join(projectDir, "demo-app")),
});

此处的核心价值在于**所有操作都是确定且可调试的**。

如果检查失败，您可以打开 JSONL 文件查看具体执行过程。每个命令执行都会按顺序显示为 `item.*` 事件。这使得回归问题能够被直接解释和修复，而这正是当前阶段所需要的。

## 6. 使用 Codex 进行定性检查与基于量规的评分

确定性检查回答的是“它完成基本操作了吗？”，但无法回答“它是否按你想要的方式完成了？”

对于像 `setup-demo-app` 这类技能，许多要求是定性的：组件结构、样式规范，或者 Tailwind 是否遵循预期配置。这些很难仅通过基础的文件存在性检查或命令计数来捕捉。

一个务实的解决方案是在评估流程中添加第二个由模型辅助的步骤：

  1. 运行设置技能（这会将代码写入磁盘）
  2. 对生成的代码仓库运行**只读风格检查**
  3. 要求生成**结构化响应**，以便你的测试框架能稳定评分

Codex 通过 `--output-schema` 直接支持此功能，该参数可将最终响应约束为你定义的 JSON 模式。

### 小型评分模式架构

首先定义一个小型模式，用于捕获你关注的检查项。例如创建 `evals/style-rubric.schema.json`：

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

该模式提供了稳定的字段（`overall_pass`、`score`、逐项检查结果），你可以对这些字段进行组合、差异比较和长期追踪。

### 风格检查提示词

接下来运行第二次 `codex exec`，该命令**仅检查代码仓库**并输出符合评分模式的 JSON 响应：

执行以下命令：

    codex exec \
      "评估 demo-app 仓库是否符合以下要求：
       - 存在 Vite + React + TypeScript 项目
       - Tailwind 通过 @tailwindcss/vite 配置，且 CSS 导入 tailwindcss
       - src/components 目录包含 Header.tsx 和 Card.tsx 文件
       - 组件为函数式组件，并使用 Tailwind 工具类进行样式设置（不使用 CSS 模块）
       以 JSON 格式返回评估结果，包含检查项 ID：vite、tailwind、structure、style。" \
      --output-schema ./evals/style-rubric.schema.json \
      -o ./evals/artifacts/test-01.style.json

这正是 `--output-schema` 的实用之处。相比难以解析或比较的自由格式文本，您将获得一个可预测的 JSON 对象，便于您的评估框架在多次运行中进行评分。

如果您后续将此评估套件迁移至 CI 环境，Codex GitHub Action 明确支持通过 `codex-args` 传递 `--output-schema` 参数，从而可在自动化工作流中强制执行相同的结构化输出。

## 7\. 随着技能成熟扩展评估体系

一旦核心循环建立完成，您可以根据技能发展的重点方向扩展评估内容。从小处着手，仅在能真正提升置信度的环节逐步增加深度检查。

示例如下：

  * **命令计数与无效操作：** 统计 JSONL 跟踪记录中的 `command_execution` 条目，以检测代理开始循环或重复执行命令的回归问题。`turn.completed` 事件中也包含令牌使用量信息。

  * **令牌预算：** 跟踪 `usage.input_tokens` 和 `usage.output_tokens` 数据，以发现意外的提示膨胀问题，并比较不同版本间的效率差异。

  * **构建检查：** 在技能执行完成后运行 `npm run build`。这提供了更强的端到端验证信号，能捕获损坏的导入或错误配置的工具链。

  * **运行时冒烟测试：** 启动 `npm run dev` 并通过 `curl` 访问开发服务器，若已有轻量级 Playwright 测试也可运行。建议选择性使用此方法，虽能增强置信度但会增加时间成本。

  * **仓库整洁度：** 确保运行过程未生成多余文件，且 `git status --porcelain` 输出为空（或符合明确的允许清单）。

*   **沙盒与权限回归测试：** 验证技能在运行时是否仍能正常工作，且未超出您预期的权限范围。一旦实现自动化，最小权限默认原则至关重要。

模式始终如一：先进行快速检查以解释行为，仅当能降低风险时，才增加更慢、更复杂的检查。

## 8. 关键要点

这个简单的 `setup-demo-app` 示例展示了从“感觉更好”到“有据可依”的转变：运行智能体，记录发生的情况，并通过一组简洁的检查进行评分。一旦形成此循环，每次调整都更容易验证，每次回归都清晰可见。以下是要点总结：

*   **衡量关键指标。** 良好的评估能让回归问题清晰可见，失败原因易于解释。
*   **从可检查的完成定义开始。** 使用 `$skill-creator` 快速启动，然后逐步收紧指令，直至成功标准明确无误。
*   **评估应基于行为。** 通过 `codex exec --json` 捕获 JSONL 日志，并针对 `command_execution` 事件编写确定性检查。
*   **在规则不足时善用 Codex。** 结合 `--output-schema` 添加结构化、基于量表的评估，以可靠地评判风格与规范。
*   **让真实失败驱动测试覆盖。** 每次手动修复都是一个信号。将其转化为测试，确保技能持续正确运行。
