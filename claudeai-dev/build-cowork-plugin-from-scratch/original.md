# How to Build a Plugin from Scratch in Cowork (2026 Guide)

Source: https://claudeai.dev/blog/build-cowork-plugin-from-scratch

---

If you want Cowork to do real work for you, plugins are the lever.

As of **February 28, 2026** , we now have a clear official path:

  * Anthropic introduced Cowork on **January 14, 2026**
  * Custom plugin creation/sharing was announced on **January 20, 2026**
  * Enterprise plugin directory updates shipped on **February 24, 2026**
  * Plugin help docs were updated on **February 25, 2026**

This guide combines that official flow with practical lessons from community users so you can build your first useful plugin from scratch.

## What a Cowork plugin should do (before you touch the UI)​

A good first plugin should solve **one narrow, repeated task**.

Bad first plugin idea:

  * “Do my whole marketing strategy”

Good first plugin ideas:

  * “Turn meeting notes into weekly action items with owners and due dates”
  * “Summarize incident logs and output a risk triage table”
  * “Review candidate profile text and return a structured scorecard”

Before building, write this one-line contract:

> Input: what you provide.
>  Output: what the plugin must return every time.

If you cannot define this clearly, your plugin prompt will drift.

* * *

## Step 1) Create the plugin shell in Cowork​

In Cowork, open the plugin area and create a new plugin.

From official docs/help, you can usually:

  * Create from scratch in the Cowork UI
  * Import from local files
  * Install from plugin directory (for existing plugins)

For your first build, choose **from scratch** so you understand each setting.

* * *

## Step 2) Name and description: routing accuracy starts here​

Community builders repeatedly report that plugin selection is heavily influenced by clear naming and description.

Use this format:

  * Name: concrete role (`Incident Triage Reporter`)
  * Description: trigger + scope (`Use when user asks to triage ops incidents from raw logs into severity, owner, and next action.`)

Avoid vague descriptions like “general assistant plugin.”

Why this matters:

  * Cowork must decide when your plugin is relevant
  * Ambiguous descriptions cause wrong plugin activation or no activation

* * *

## Step 3) Write a strict prompt contract​

Your plugin instructions should read like a production runbook.

Minimum structure that works:

  1. Role and objective
  2. Required inputs
  3. Output format (fixed sections/table/JSON-like structure)
  4. Decision rules and prioritization
  5. Safety boundaries and what to do when uncertain

Example skeleton:

    You are Incident Triage Reporter.

    Goal:
    - Convert raw incident notes into a priority triage report.

    Required inputs:
    - incident_log
    - service_name
    - report_time

    Output format:
    - Severity: P0/P1/P2/P3
    - Impact summary (max 3 bullets)
    - Suspected root cause
    - Immediate next action
    - Owner recommendation

    Rules:
    - If evidence is weak, state uncertainty explicitly.
    - Never invent metrics not present in input.
    - Ask one clarifying question if critical context is missing.

Community lesson: shorter, constrained prompts outperform long “do everything” prompts.

* * *

## Step 4) Design for predictable output, not “creative” output​

If a plugin is part of your workflow, consistency is more important than style.

Practical checks:

  * Can teammates skim output in 10 seconds?
  * Can downstream automation parse it?
  * Does the format stay stable across 5 very different test inputs?

If not, tighten instructions and reduce scope.

* * *

## Step 5) Test with real edge cases before sharing​

Do not test only “happy path” input.

Run at least these 5 tests:

  1. Clean, complete input
  2. Missing key field
  3. Contradictory data
  4. Very long/noisy input
  5. Input outside plugin scope

Expected behavior for #5 should be explicit refusal + redirect suggestion.

* * *

## Step 6) Share safely in your workspace​

Official plugin rollout for teams emphasizes controlled sharing and workspace governance.

Before publishing internally:

  * Add a clear “When to use / When not to use” section
  * Add example input/output in plugin docs
  * Set owner and maintenance expectations
  * Version the prompt (`v0.1`, `v0.2`, etc.) with a tiny changelog

This prevents “mystery plugin” drift after a few weeks.

* * *

## Step 7) Iterate from usage signals​

After release, review actual runs weekly:

  * Activation quality (called at the right time?)
  * Output correction rate (how often users rewrite results)
  * Failure patterns (missing context, wrong assumptions)

Then update only one variable per iteration:

  * Description wording
  * Prompt rule
  * Output schema

Small controlled edits beat full rewrites.

* * *

## Official vs community guidance: what to trust most​

Use this priority order:

  1. Official Cowork product + support docs (feature behavior, permissions, rollout)
  2. Official plugin tutorials/reference (format and implementation details)
  3. Community examples (great for edge cases and practical heuristics)

Community posts are useful, but they can go stale quickly as Cowork evolves.

* * *

## Final takeaway​

Your first Cowork plugin should be boring, narrow, and reliable.

If you get these three right:

  * clear trigger description
  * strict output contract
  * disciplined test cases

…you will get real leverage quickly, and your second plugin will be much easier.

## Sources (checked on 2026-02-28)​

### Official​

  * Anthropic: Introducing Cowork (2026-01-14)
<https://www.anthropic.com/news/introducing-cowork>
  * Anthropic: Create and share plugins in Cowork (2026-01-20)
<https://www.anthropic.com/news/create-and-share-plugins-in-cowork>
  * Anthropic: Cowork and plugins for enterprises and financial services (2026-02-24)
<https://www.anthropic.com/news/cowork-and-plugins-for-enterprises-and-financial-services>
  * Claude Support: Use plugins in Cowork (updated 2026-02-25)
<https://support.claude.com/en/articles/11811905-use-plugins-in-cowork>
  * Claude Code docs: How to build a plugin from scratch in Cowork
<https://code.claude.com/tutorials/plugins/how-to-build-a-plugin-from-scratch-in-cowork>

### Community​

  * Reddit (r/ClaudeAI): “I want to create custom skills for Cowork, but they don't work”
<https://www.reddit.com/r/ClaudeAI/comments/1ics9f1/i_want_to_create_custom_skills_for_cowork_but/>
  * YouTube (Zinho): “Claude COWORK Plugins Just Changed EVERYTHING! NEW Plugin Directory Breakdown”
<https://www.youtube.com/watch?v=ftQZiP22TF4>
  * Medium (Dong Liang): “The Fork in the Road: Claude Code vs Cowork…” (2026-02-26)
<https://medium.com/@dongliang_47217/the-fork-in-the-road-claude-code-vs-cowork-which-one-really-fits-your-ai-workflow-in-2026-826c8860748d>