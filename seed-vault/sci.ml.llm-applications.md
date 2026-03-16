---
id: sc3p5alpha6k2n8qw4x1jpqr
title: LLM Integration Patterns for SaaS
desc: 'Patterns for integrating LLMs into SaaS product features'
domain: ml
subdomain: llm-applications
updated: 1709000000000
created: 1707000000000
---

# LLM Integration Patterns for SaaS

## Overview

Notes on practical patterns for integrating LLMs (GPT-4, Claude, open-source models) into SaaS products. Focus is on product management / project management use cases relevant to Nimbus.

## Use Cases We're Exploring

1. **Smart task summarization**: Given a task with 50+ comments, generate a concise status summary. Low risk, high value. Ship this first.
2. **Natural language task creation**: "Create a task for Marcus to review the API versioning PR by Friday" → structured task with assignee, due date, and labels.
3. **Sprint retrospective synthesis**: Summarize a sprint's completed tasks, blockers, and velocity trends into a readable retro doc.
4. **API documentation generation**: Given an OpenAPI spec, generate human-readable documentation with examples. Relevant to [[proj.2026.api-redesign]].

## Architecture Patterns

- **Prompt engineering over fine-tuning**: For our scale (mid-size SaaS), prompt engineering with GPT-4 or Claude is more practical than fine-tuning. The data volume doesn't justify fine-tuning costs, and prompt-based approaches are easier to iterate.
- **Structured output via function calling**: Use OpenAI/Anthropic function calling to get structured JSON responses. Avoids brittle regex parsing of free-text outputs.
- **Streaming for UX**: Stream LLM responses for any user-facing feature. Waiting 5-10 seconds for a complete response kills the experience.
- **Caching**: Cache identical prompts with a TTL. Task summaries don't change frequently — cache for 1 hour and invalidate on new comments.
- **Cost management**: GPT-4 is expensive at scale. Use GPT-3.5-turbo or Claude Haiku for high-volume, low-complexity tasks (summarization). Reserve GPT-4/Claude Opus for complex reasoning (natural language parsing).
- **Fallback strategy**: LLM responses should enhance, not gate, core functionality. If the LLM is down or returns garbage, the feature degrades gracefully — show the raw data instead of the summary.

## Evaluation

- **Automated evals**: Build a test suite of input/expected-output pairs. Run on every prompt change. Use LLM-as-judge for open-ended quality assessment.
- **Human review**: Sample 5% of production responses weekly for quality review. Flag hallucinations and edge cases.

## Notes

- Nina ([[user.nina-okonkwo]]) is pushing for task summarization as the first LLM feature in Q3. I agree — it's bounded, useful, and low risk.
- Need to evaluate whether to use OpenAI, Anthropic, or self-host an open model. My instinct: start with Claude API for quality, revisit cost at scale.
- Privacy: customer task data goes to the LLM. Need to ensure our DPA covers this and offer an opt-out for enterprise customers.
