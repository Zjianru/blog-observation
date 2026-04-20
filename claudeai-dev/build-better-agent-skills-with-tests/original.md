# Build Better Agent Skills with Test-Measure-Refine

Source: https://claudeai.dev/blog/build-better-agent-skills-with-tests

---

Most agent skills fail for a boring reason: we edit prompts, rerun once, and call it “better.”

Anthropic’s latest Skill Creator update pushes a more engineering-style loop: **test first, measure behavior, then refine**. If you build internal agent workflows, this is the shift that actually matters.

This post rewrites the official announcement into a developer workflow you can run every week.

## The Core Idea: Stop Prompting Blindly​

The official update is not just “better prompt generation.” It is a quality loop:

  1. Define measurable behavior up front
  2. Generate a test suite from that behavior
  3. Run evaluations against old/new versions
  4. Use evaluator feedback to remove conflicts and dead instructions
  5. Iterate with evidence, not vibe checks

If that sounds like CI for prompts, that is exactly the point.

* * *

## What Changed in Skill Creator (Developer Version)​

From the official post, these are the practical changes worth caring about:

  * **Golden prompts before implementation** You write (or co-create) concrete prompts that represent real tasks. These become your baseline cases.

  * **`test-creator` for automatic skill tests** Skill Creator can generate tests from your requirements, so you are not hand-writing every case from scratch.

  * **Integrated skill evaluator** Evaluator feedback highlights instruction conflicts, overlap, and weak areas so you can tighten the skill spec.

  * **Refinement based on quality signal** You are expected to loop through multiple versions, measuring changes against test outputs, not just “feels better” judgments.

This is a better fit for engineers because it treats skills like versioned artifacts, not one-shot prompts.

* * *

## A Practical Workflow You Can Use​

### Step 1) Write acceptance criteria like API behavior​

Before editing any skill text, write expected behavior in strict form:

  * Input shape
  * Output schema
  * Must-do rules
  * Must-not-do rules
  * Failure behavior (what to do when context is missing)

If your criteria are fuzzy, your tests will be fuzzy.

### Step 2) Build a golden prompt set from real incidents​

Use real logs, tickets, or requests from your team. Include:

  * Normal case
  * Noisy/ambiguous case
  * Missing-context case
  * Out-of-scope case

These are your regression suite. Keep them small but high signal.

### Step 3) Generate and run tests​

Use Skill Creator + `test-creator` to generate structured skill tests. Then run both:

  * Current production skill
  * Candidate updated skill

Compare output quality against the same test set.

### Step 4) Run evaluator feedback and prune instructions​

Look for repeated failure patterns:

  * Contradictory instructions
  * Overly broad instructions
  * Hidden assumptions
  * Output formatting instability

Refine only one or two variables per iteration so you can attribute improvements.

### Step 5) Promote only if metrics improve​

Do not ship because one example looked good. Promote only when:

  * Pass rate improves on the full suite
  * Failure modes are reduced, not shifted
  * Output format remains stable across edge cases

* * *

## Where Teams Usually Get Stuck​

These are common failure modes we see in real developer teams:

  * **Too many rules in one skill** A single mega-skill trying to do summarization, planning, classification, and policy interpretation usually degrades quickly.

  * **No versioned test data** If golden prompts are not versioned, you cannot trust trend lines.

  * **No refusal behavior** Skills should define what to do when data is insufficient or out-of-scope.

  * **Refining with no hypothesis** “Let’s tweak wording” without a measurable hypothesis wastes cycles.

* * *

## A Better Mental Model​

Treat a skill like this:

  * Prompt text = implementation
  * Golden prompts = unit tests
  * Evaluator + test runs = regression checks
  * Release note = changelog

Once teams adopt this model, skill quality becomes predictable.

* * *

## Minimal Template for Your Next Skill PR​

Use this structure in your internal PR description:

    ## Goal
    What user job this skill solves.

    ## Behavior Contract
    - Inputs
    - Outputs
    - Guardrails
    - Refusal policy

    ## Test Set
    - Golden prompts: N
    - Edge cases included: yes/no

    ## Results
    - Baseline pass rate: X%
    - Candidate pass rate: Y%
    - Known regressions: ...

    ## Decision
    Promote / Hold / Roll back

This makes skill changes reviewable by the same standards you use for code changes.

* * *

## Final Takeaway​

The best part of Anthropic’s Skill Creator update is not “smarter generation.”

It is that skills now fit a developer-native lifecycle:

**design - > test -> evaluate -> refine -> release**

If your team builds serious agent workflows, this is how you stop prompt drift and start shipping reliable skills.

## Source​

  * Anthropic official blog: _Improving Skill Creator: Test, measure, and refine agent skills_
<https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills>