# I Let OpenClaw Run My Life for a Week. No One Noticed (Yet).

*Kejun Albert Ying | March 2026*

---

## The Premise

What happens when an AI agent has access to everything you know — your projects, your people, your calendar, your communication patterns — and learns from every correction you give it?

Not a chatbot with memory bolted on. Not RAG over your documents. A persistent agent that reads the same structured knowledge you maintain, writes in your voice, and accumulates behavioral refinements across sessions the way a model accumulates gradient updates during training.

I built this system over the past month with [OpenClaw](https://github.com/Albert-Ying/agentic-cortex), an open-source CLI agent framework. Last week, it drafted 12 emails, ran morning briefings surfacing stale follow-ups and project momentum, caught a promise I'd forgotten three weeks prior, and prepared meeting context before I asked. Nobody on the receiving end flagged anything. The emails sounded like me because, in a meaningful sense, the agent *had become* me — same memory, same taste, same voice.

This post explains the architecture and the three technical ideas that make it work: a feedback loop that functions like RLHF without training, voice profile extraction from communication history, and ambient context capture via Screenpipe.

---

## Architecture in Brief

The system is five layers of plaintext markdown, version-controlled in git. No vector database. No embeddings. No fine-tuning.

1. **Senses** — MCP servers connecting to Gmail, Google Calendar, and Screenpipe (local screen + audio recording). These are read-only data pipes with human approval gates on every action.
2. **Sync Engine** — Source adapters that normalize raw data into structured diffs: new calendar events, email threads with replies, collaborator mentions in transcripts. These flow into the vault.
3. **Vault** — The long-term memory, and the key architectural decision. Dot-separated filenames encode type, time, and relationships: `user.priya-sharma.md` is a person, `proj.2026.api-redesign.md` is a project, `meet.2026.03.14.md` is a meeting. The naming convention IS the schema — no database, no embeddings. The agent navigates the entire knowledge graph through glob patterns: `user.*.md` finds all people, `meet.*.md` + grep for a name finds all meetings with that person. Cross-links inside notes create the graph edges. Your filesystem becomes a queryable knowledge graph with zero infrastructure. This is borrowed from [Dendron](https://www.dendron.so/)'s hierarchy, but the pattern works with any file-based notes.
4. **Command Center** — Working memory (`_working-memory.md`) tracks what's hot right now: today's calendar, active tasks, stale follow-ups. A context model tracks medium-term state: project momentum, collaborator threads, open decisions. Three tiers — hot, warm, cold — all plaintext.
5. **Behavior Layer** — A `CLAUDE.md` file defines the agent's operating rules. Skills provide reusable capabilities. Auto-memory files accumulate learned preferences across sessions. A feedback loop converts corrections into permanent behavioral changes.

Everything is `git diff`-able. You can inspect exactly what changed in the agent's world model between Tuesday and Wednesday. The full architecture is in the [repo](https://github.com/Albert-Ying/agentic-cortex).

---

## The Feedback Loop: RLHF Without Training

This is the most interesting part of the system, and it emerged almost by accident.

In standard RLHF, you improve a model's behavior through labeled preference data, reward modeling, and policy optimization. It requires GPU clusters, curated datasets, and training infrastructure. The conceptual goal is simple — human feedback should produce lasting behavioral change — but the engineering is heavy.

The feedback loop in this system achieves the same conceptual goal through a different mechanism. When I correct the agent — "don't double-space after paragraphs in emails" — the correction gets persisted as a structured memory entry containing three things:

1. **The rule**: single line breaks in all email drafts.
2. **The rationale**: double spacing signals AI-generated text to recipients who know my style.
3. **The scope**: all email drafts, all communication registers.

Next session, the agent reads this file alongside all other accumulated feedback. The behavior changes permanently. No training run. No weight update. The correction propagates through context, not through gradients.

The analogy maps cleanly:

| RLHF | Feedback Loop |
|------|--------------|
| Base model weights | `CLAUDE.md` (base policy) |
| Human preference labels | Natural language corrections |
| Reward model | Rationale field in feedback entries |
| Policy gradient update | Feedback file written to disk |
| Updated model | Agent reading updated context next session |

The key difference is generalization. Standard RLHF requires many examples to shift a model's distribution. Here, a single correction with a well-articulated rationale generalizes immediately, because the agent can reason about the principle. One correction about git repositories and large binary files ("never `git init` at `~/` — a prior `.git` there ballooned to 52GB from tracking binary-heavy subdirectories") later caused the agent to independently warn about initializing a repo in a directory full of `.h5` files. No rule mentioned `.h5` files. The agent had extracted the principle — large binary files and git don't mix — and applied it to a novel situation.

After roughly 15 sessions and 18 accumulated feedback entries, the agent's email drafts became indistinguishable from my own. It learned formatting preferences, communication register calibration per relationship tier, domain-specific vocabulary choices, and stylistic constraints I hadn't explicitly articulated — it inferred them from the pattern of corrections.

This is what makes plaintext feedback more powerful than it sounds: the corrections compound. Each one narrows the agent's behavioral space, and because the agent reads *all* of them at session start, the combined effect is multiplicative, not additive.

---

## Voice Profile Extraction

An agent that remembers your schedule and projects is useful. An agent that writes like you is transformative.

The voice profile is a structured document extracted from real communication data — sent emails, chat messages, meeting notes. The extraction process analyzes thousands of messages across communication channels, identifying patterns in:

- **Register calibration**: How formality, warmth, and technical depth shift based on the recipient. An email to an advisor reads differently from a message to a close collaborator, which reads differently from a note to a conference organizer.
- **Structural habits**: Sentence length distributions, paragraph patterns, greeting and sign-off conventions, the specific ways you transition between topics.
- **Vocabulary fingerprint**: Domain terms you use versus avoid, filler phrases that signal your voice, characteristic constructions.
- **Cross-language patterns**: For multilingual users, how you code-switch, which terms stay in which language, how tone shifts across languages.

The resulting document is a detailed specification of how you communicate, organized by register and channel. The agent reads it at session start and applies it to every draft. The effect is immediate — the first draft is close, and the feedback loop handles the remaining delta.

This matters because the failure mode of most AI-drafted communication isn't factual error. It's uncanny valley. The email is *almost* right but uses a greeting you'd never use, or structures the ask in a way that's subtly off. Recipients don't consciously notice, but the interaction feels different. A precise voice profile eliminates that gap.

---

## Screenpipe: Ambient Context Without Manual Logging

The weakest link in any personal knowledge system is input. People don't log consistently. They forget to take meeting notes. They don't record what they were working on at 2 AM when an idea struck.

[Screenpipe](https://github.com/mediar-ai/screenpipe) solves this by recording screen content and audio continuously on the local machine. The system's sync engine queries Screenpipe's local API, extracts structured events — applications used, documents opened, conversations transcribed — and flows them into the vault.

The practical effect: the agent knows what you were working on yesterday even if you didn't tell it. It can reconstruct context from screen recordings, identify when you were deep in a particular codebase, notice that you spent three hours on a paper draft, or flag that a collaborator's name appeared in a video call transcript. This becomes the raw material for daily journal generation — automated activity logs with key moments preserved as screenshots and clips.

The privacy model is strict. Screenpipe runs entirely locally. Recordings never leave the machine. The agent accesses them through a local API with the same permission gates as every other action. You can delete any recording at any time, and the vault entries derived from it remain as standalone notes — the dependency is one-directional.

---

## The Shared Memory Model

The deeper insight beneath all of this is about what happens when an AI agent shares your memory — not a summary of your memory, not a retrieval over your memory, but your actual structured knowledge, maintained in the same format you'd maintain it yourself.

The agent has the same memory as you. In many cases, more precise memory. It knows when you last contacted each collaborator, what was discussed, what was promised. It tracks 400+ people profiles, each with interaction history, relationship context, and open threads. It maintains project state across months. It catches things you've forgotten because it reads the complete context every session while you, being human, rely on incomplete recall.

This changes the interaction model fundamentally. You stop managing the AI and start working *with* it. The morning briefing isn't a feature you configured — it's what naturally happens when an agent has full situational awareness and a directive to surface what matters. The stale follow-up detection isn't a reminder system — it's a consequence of the agent knowing your relationship graph and noticing gaps.

---

## Safety

Everything runs locally. The agent drafts emails but never sends them. Chat messages go to the clipboard for manual pasting. Every behavioral rule is a line in a markdown file — delete the line, the behavior stops. The full knowledge base is greppable in seconds. The attack surface is what the agent can read on disk and what you approve it to do. Both are auditable, both are transparent. The [repo](https://github.com/Albert-Ying/agentic-cortex) documents the threat model in detail.

---

## Try It

The [repo](https://github.com/Albert-Ying/agentic-cortex) includes a seed vault, skills, and a setup script. Clone it, run `setup.sh`, and you have a working system in 30 minutes. The tutorial walks through nine chapters — from basic persistent memory to the full command center with email, calendar, screenpipe, voice profiles, and the feedback loop.

The system works with Claude Code, OpenClaw, Cursor, Windsurf, or any agent framework that reads `CLAUDE.md` and supports MCP. The notes are markdown. The memory is files. The intelligence is whatever model you choose. What matters is the persistent context layer around it.

[**GitHub: agentic-cortex**](https://github.com/Albert-Ying/agentic-cortex)
