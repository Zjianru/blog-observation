# Choosing AI Agent Workflow Patterns That Actually Ship

Source: https://claudeai.dev/blog/choosing-ai-agent-workflow-patterns-that-ship

---

Most teams do not fail with agents because of model quality.

They fail because they pick the wrong workflow pattern too early: too much orchestration, too many moving parts, and no clear reason for the complexity.

Anthropic’s recent guide on common agent workflow patterns is useful, but this post rewrites it for developers building production systems.

## The One Rule Most Teams Ignore​

Start with the **simplest pattern that meets your quality bar**.

In practice, that means:

  1. Try a single-agent call first
  2. Add sequential steps only when dependencies force ordering
  3. Add parallel workers only when tasks are truly independent and latency matters
  4. Add evaluator-optimizer loops only when quality gains are measurable

If you skip this order, you usually pay in latency, token cost, and debugging pain.

* * *

## Pattern 1: Sequential Workflows​

Use sequential workflows when step B depends on step A.

Think of it as a pipeline:

  * extract
  * transform
  * validate
  * route

### Good fit​

  * Multi-stage tasks with hard dependencies
  * Data pipelines where each stage adds a different kind of value
  * Draft -> review -> polish flows

### Bad fit​

  * When one agent already does the job reliably
  * When steps are fake separations and can be merged

### Developer tradeoff​

  * Higher latency
  * Better control and easier observability per stage

### Quick test​

If you remove one stage and output quality barely changes, that stage is likely unnecessary.

* * *

## Pattern 2: Parallel Workflows​

Use parallel workflows when subtasks are independent and can run at the same time.

This is fan-out/fan-in in distributed-systems terms:

  * fan out work to multiple agents
  * fan in with an aggregation strategy

### Good fit​

  * Multi-dimension evaluation (safety, style, correctness)
  * Security/code reviews by category
  * Document analysis with independent lenses

### Bad fit​

  * When agents need shared evolving context
  * When you do not have a robust aggregation strategy
  * When API quotas/concurrency limits erase speed gains

### Developer tradeoff​

  * Faster completion
  * Higher cost + aggregation complexity

### Quick test​

If your aggregation logic is more complex than each parallel worker, you over-parallelized.

* * *

## Pattern 3: Evaluator-Optimizer Workflows​

Use evaluator-optimizer when first-draft quality is not enough and your quality criteria are explicit.

Structure:

  * Generator produces draft
  * Evaluator scores against concrete criteria
  * Generator revises
  * Stop when threshold or max iterations is reached

### Good fit​

  * Code generation with strict standards
  * High-stakes docs/comms where tone and precision matter
  * SQL/query generation with security/perf checks

### Bad fit​

  * Real-time interactions needing immediate responses
  * Tasks with subjective criteria evaluators cannot apply consistently
  * Cases where deterministic tools already solve validation (linters, schema validators)

### Developer tradeoff​

  * Potentially much better quality
  * More tokens, more latency, and risk of endless micro-iterations

### Quick test​

If iteration 3+ gives tiny improvements, cap iterations lower and move on.

* * *

## A Practical Decision Tree​

Use this in planning docs or design reviews:

  1. Can one agent solve this reliably? If yes, stop.
  2. Are there hard step dependencies? If yes, go sequential.
  3. Are subtasks independent and latency-sensitive? If yes, add parallel branches.
  4. Is first-pass quality below bar with measurable criteria? If yes, add evaluator-optimizer where needed.

This keeps complexity proportional to real requirements.

* * *

## Failure Handling You Should Define Up Front​

Regardless of pattern, define these before rollout:

  * Retry policy per stage
  * Timeout budgets
  * Fallback behavior
  * Partial failure strategy
  * Contradictory-output resolution rules

Without this, your “agent architecture” is just a demo.

* * *

## Baseline Before You Orchestrate​

Anthropic’s guidance is directionally right: set a baseline with a simpler approach first.

For teams, that means tracking at least:

  * task success rate
  * latency p50/p95
  * token cost per successful run
  * human correction rate

Only keep added orchestration if one of these improves meaningfully.

* * *

## Pattern Combinations That Work Well​

Patterns are building blocks, not exclusive choices.

Two common combinations:

  * **Sequential + Parallel** : a sequential pipeline with one or two parallel-heavy stages
  * **Parallel + Evaluator** : multiple generators or reviewers feeding a focused evaluator pass

Avoid nesting patterns unless you can explain the quality/cost impact with metrics.

* * *

## Final Takeaway​

Workflow patterns are not architecture theater. They are cost/quality controls.

If you want systems that ship and stay maintainable:

  * start simple
  * add structure only when a bottleneck is proven
  * measure every complexity increase

That is how you turn agent experiments into production workflows.

## Source​

  * Anthropic official blog: _Common workflow patterns for AI agents—and when to use them_
<https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them>