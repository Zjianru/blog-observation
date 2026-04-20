# Conway Timeline: How Anthropic Is Building Always-On Agents

Source: https://claudeai.dev/blog/conway-timeline-how-anthropic-is-building-always-on-agents

---

The most important thing to get right about **Conway** is this:

**Conway is not an officially launched Anthropic product.**

What exists today is a mix of:

  * official Anthropic launches around **Cowork** , **Dispatch** , **computer use** , **scheduled tasks** , and **auto mode**
  * current help-center documentation that shows how those pieces now fit together
  * an **April 1, 2026** third-party report that surfaced an unreleased internal environment called **Conway**

If you only look at the leak, you miss the architecture. If you only look at the official launches, you miss where Anthropic seems to be going.

The technical story is the combination of both.

## Short Answer​

From a systems perspective, Anthropic is clearly moving toward an **always-on agent model**.

Not because Conway has been announced, but because the shipped product stack already contains most of the required primitives:

  * a **persistent thread** that follows you across devices
  * a **desktop runtime** with local file access
  * **scheduled execution**
  * **computer use** when direct integrations are missing
  * **sub-agent coordination**
  * a safer **long-running permission mode**
  * mobile-to-desktop task handoff via **Dispatch**

Conway matters because it appears to package those ideas into a more explicit always-on agent environment.

## What Is Actually Confirmed vs. What Is Not​

Before getting into the timeline, separate the evidence into three buckets.

### Confirmed by Anthropic​

Anthropic has officially shipped or documented:

  * Cowork as a desktop agent environment built on Claude Code's agentic architecture
  * persistent task handoff between phone and desktop through Dispatch
  * scheduled tasks and recurring routines
  * computer use in Cowork and Claude Code
  * auto mode for longer-running Claude Code sessions

### Confirmed by Current Anthropic Docs, but Not As A Single Launch​

Anthropic's current help docs now describe a workflow where:

  * you keep **one continuous thread**
  * Claude can route **development work into Claude Code**
  * Claude can route **knowledge work into Cowork**
  * results come back into the same persistent thread
  * scheduled tasks can run automatically
  * computer use can operate apps on your desktop

That is already very close to an always-on agent runtime, even if Anthropic has not named it that way.

### Reported, But Not Officially Announced​

The **Conway** name comes from a third-party report published on **April 1, 2026**. According to that report, Conway appears to expose:

  * a dedicated **Conway instance**
  * its own sidebar with **Search** , **Chat** , and **System**
  * **extensions**
  * **webhooks**
  * direct connection from **Claude in Chrome**
  * **notifications**

That is the strongest current signal that Anthropic may be building a more explicit always-on agent environment.

But that is still a report about unreleased product work, not an official release.

## The Timeline​

Here is the cleanest technical timeline I can reconstruct from official sources plus the Conway report.

### January 12, 2026: Cowork research preview launches​

Anthropic introduced **Cowork** as "Claude Code for the rest of your work."

The important part was not the UI. It was the runtime model:

  * Claude works directly in folders on your computer
  * Claude can handle **multi-step tasks**
  * Cowork is built on the **same agentic foundations** as Claude Code
  * users can queue tasks and let Claude work more like a coworker than a chat thread

This was the first public sign that Anthropic wanted a broader desktop agent runtime, not just a terminal coding tool.

### January to February 2026: Cowork expands across plans and Windows​

Anthropic expanded Cowork availability across paid plans and then to Windows.

That matters technically because it suggests Cowork was not staying a niche experiment for one power-user tier. Anthropic was hardening the runtime for broader deployment.

### By late March 2026: Cowork docs describe the full local agent runtime​

Anthropic's current Cowork help docs now make the architecture much clearer than the original launch post did.

Cowork is documented as:

  * bringing Claude Code's **agentic capabilities** into Claude Desktop
  * supporting **direct local file access**
  * coordinating **multiple sub-agents in parallel**
  * running tasks for extended periods
  * supporting **scheduled tasks**
  * supporting **projects** with their own files, instructions, and memory
  * running work in a **virtual machine (VM) environment**

That is not a chatbot feature set. It is an agent runtime.

### March 23, 2026: Dispatch and computer use land across Cowork and Code​

This is the biggest public milestone so far.

Anthropic officially described a product state where Claude can:

  * maintain a conversation that follows you from **phone to desktop**
  * use your **computer**
  * remember context across sessions
  * run tasks on a **schedule**
  * work across both **Cowork and Claude Code**

This is the moment where the "always-on" direction becomes hard to deny.

An always-on agent needs two things above all else:

  1. persistence
  2. the ability to act when you are not staring at the session

Dispatch plus computer use is exactly that combination.

### Late March 2026: Dispatch docs add the routing model​

Anthropic's Dispatch support documentation adds an especially important detail:

  * you get **one continuous persistent thread**
  * when you assign a task, Claude decides what kind of work it is
  * **development tasks run in Claude Code**
  * **knowledge work runs in Cowork**

This is a strong architectural clue.

Anthropic is no longer presenting Code and Cowork as isolated products. It is presenting them as **specialized execution surfaces under one task thread**.

That is the kind of separation you would expect in an always-on agent platform:

  * one user-facing thread
  * multiple execution backends
  * unified memory and handoff

### March 24, 2026: Auto mode gives Claude Code a safer long-running path​

One day later, Anthropic launched **auto mode** for Claude Code.

This matters more than it first appears.

Always-on agents are not useful if they stop every few minutes to ask for permission. But fully disabling permissions is unsafe. Auto mode is Anthropic's middle layer:

  * Claude can make some permission decisions on your behalf
  * a classifier screens tool calls before they run
  * safe actions proceed automatically
  * risky actions get blocked or escalated

This is a missing infrastructure piece for unattended or semi-unattended work.

Without something like auto mode, an always-on coding agent is mostly a demo.

### April 1, 2026: Third-party report surfaces Conway​

TestingCatalog published a report claiming Anthropic is testing an internal always-on agent environment called **Conway**.

The reported details are notable because they line up cleanly with the product direction Anthropic has already been shipping:

  * a **standalone instance**
  * extension installation, including `.cnw.zip`
  * **connectors and tools**
  * direct **Claude in Chrome** connection
  * **webhooks** with public URLs that can wake the instance
  * notifications

If accurate, Conway is not a random side project. It looks like the next packaging layer above the runtime Anthropic has already been building in public.

## Why Conway Makes Technical Sense​

If you strip away the product names, Anthropic already has most of the components needed for an always-on agent system.

### 1\. A persistent control thread​

Dispatch provides the user-facing thread that survives device changes.

That thread is important because it becomes the stable control surface:

  * the user issues goals there
  * results come back there
  * approvals can happen there
  * memory can accumulate there

Without that thread, every task is a fresh spawn.

### 2\. Specialized runtimes​

Anthropic has two distinct execution surfaces:

  * **Claude Code** for development work
  * **Cowork** for broader desktop knowledge work

That is already a scheduler-friendly architecture. The system can decide what kind of runtime a task needs instead of forcing one interface to do everything.

### 3\. Triggering beyond foreground chat​

Scheduled tasks and Dispatch push the model beyond reactive chat.

That matters because an always-on agent needs external triggers:

  * time-based triggers
  * user messages from another device
  * possibly service-triggered events

The Conway report becomes especially interesting here because **webhooks** are exactly the next logical trigger surface.

### 4\. Fallback execution through computer use​

Direct integrations are always better than screen control. Anthropic says this explicitly in the computer-use docs: Claude should reach for connectors first, then browser automation, then direct screen interaction.

That ordering is important. It means Anthropic is not building "computer use" as a gimmick. It is treating it as the **last-resort actuator** in a broader action stack.

That is how serious agent systems are usually designed:

  * structured API path first
  * browser path second
  * UI control path last

### 5\. Governance for long-running work​

Auto mode is the first visible sign that Anthropic knows an always-on agent must have a different permission architecture from a foreground assistant.

If Conway is real, it would almost certainly need stronger versions of:

  * policy checks
  * event filtering
  * webhook-level trust boundaries
  * extension sandboxing
  * auditability
  * wake / sleep semantics

That is why the Conway report's mention of **extensions** and **webhooks** is not just feature gossip. Those are the surfaces where governance gets hard.

## The Most Interesting Conway Signals​

Not every leaked detail matters equally.

These are the signals that matter most from a technical perspective.

### Standalone instance​

The phrase "Conway instance" suggests Anthropic is thinking in terms of a **persistent agent container** , not just a chat tab.

That implies lifecycle questions like:

  * when does the instance wake up
  * how long does it stay alive
  * what state persists
  * what resets on restart
  * what can trigger it externally

Those are classic always-on agent questions.

### Extensions​

If the report is accurate, Conway is moving toward an extension model that includes:

  * tools
  * UI tabs
  * context handlers

That is a major shift. It suggests Anthropic may want a first-class plugin architecture for persistent agents, not just a static built-in runtime.

### Webhooks​

This is the single strongest always-on signal in the report.

A webhook means the agent does not just wait for a user prompt in the foreground. It can be awakened by an external system event.

That is the bridge from:

  * "run this when I ask"

to:

  * "run this when the world changes"

If Anthropic really ships webhook-triggered agent instances, that would move Conway from assistant territory into workflow-automation infrastructure.

### Chrome connection​

Anthropic already has Claude for Chrome and browser-based action paths. A direct Conway-to-Chrome bridge would make architectural sense because it would let the always-on instance treat the browser as a durable action surface.

### Notifications​

Notifications sound minor, but they are not.

An always-on agent needs a compact signaling channel for:

  * task finished
  * approval needed
  * trigger failed
  * environment offline
  * schedule skipped

Without notifications, persistent agents become opaque and annoying.

## The Real Technical Reading​

My read is:

**Conway is probably not a brand-new architecture. It is probably Anthropic's attempt to package several already-shipped subsystems into a more explicit persistent-agent environment.**

Those subsystems are already visible:

  * Cowork runtime
  * Claude Code runtime
  * Dispatch thread
  * scheduled tasks
  * computer use
  * mobile handoff
  * safer long-running permissions

Conway, if it ships, would likely be the layer that turns those into a more explicit agent instance model with:

  * durable identity
  * event triggers
  * extension points
  * external wake-up paths
  * unified notifications

That would be a real step up from "Claude can keep working while I step away."

It would become:

**Claude can stay resident as a software system.**

## What Anthropic Still Has To Solve​

This is the part people tend to skip.

Always-on agents are not just a UX problem. They are mostly a systems and safety problem.

Anthropic still has to solve at least five hard things if Conway becomes public.

### 1\. Trigger trust​

Webhook-triggered agents are powerful, but they also create attack surfaces:

  * forged events
  * replayed events
  * poisoned payloads
  * escalation through external services

### 2\. Extension isolation​

An extension model is only useful if third-party logic cannot quietly compromise the instance.

That means Conway would need strong answers for:

  * package trust
  * install permissions
  * tool scoping
  * network boundaries
  * update behavior

### 3\. State hygiene​

Persistent agents accumulate context, and accumulated context goes bad.

Anthropic will need strong mechanisms for:

  * memory pruning
  * project boundaries
  * stale state detection
  * trigger-specific context windows

### 4\. Human control​

The more persistent the agent, the more important fast interruption becomes.

Users will need reliable ways to:

  * pause the instance
  * revoke tools
  * cut connector access
  * disable triggers
  * inspect recent actions

### 5\. Execution visibility​

Foreground chat makes actions easy to observe. Always-on execution does not.

That means audit logs, summaries, traces, and event histories matter much more in a Conway-style system than they do in ordinary chat.

## Final Take​

If you ask, "Did Anthropic officially launch Conway?" the answer is **no**.

If you ask, "Is Anthropic clearly building toward an always-on agent architecture?" the answer is **yes**.

The official product trail already shows the direction:

  * **Cowork** established the desktop agent runtime
  * **Dispatch** established the persistent cross-device thread
  * **scheduled tasks** established time-based automation
  * **computer use** established the fallback actuator layer
  * **auto mode** established safer long-running execution
  * the reported **Conway** environment adds the missing language of instances, webhooks, extensions, and notifications

That is the real technical story.

Conway matters not because it proves Anthropic has finished always-on agents. It matters because it makes Anthropic's product trajectory much easier to see.

## Sources (checked April 3, 2026)​

  * Cowork research preview / product page
<https://claude.com/blog/cowork-research-preview>
  * Get started with Cowork
<https://support.claude.com/en/articles/13345190-get-started-with-cowork>
  * Assign tasks to Claude from anywhere in Cowork
<https://support.claude.com/en/articles/13947068-assign-tasks-to-claude-from-anywhere-in-cowork>
  * Put Claude to work on your computer
<https://claude.com/blog/dispatch-and-computer-use>
  * Let Claude use your computer in Cowork
<https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork>
  * Auto mode for Claude Code
<https://claude.com/blog/auto-mode>
  * TestingCatalog report on Conway
<https://www.testingcatalog.com/exclusive-anthropic-tests-its-own-always-on-conway-agent/>