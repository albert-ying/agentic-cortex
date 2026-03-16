# I Let OpenClaw Run My Life for a Week. No One Noticed (Yet).

*Kejun Albert Ying | March 2026*

---

Last week my AI drafted 12 emails in my voice, briefed me every morning with my calendar and stale follow-ups, caught a promise I forgot I made three weeks ago, and prepared meeting context before I asked for it. Nobody on the receiving end knew. A collaborator replied to one of the AI-drafted emails within 4 minutes — normal cadence, normal tone, no "wait, did a robot write this?" Nobody flagged anything. Not my advisor, not my collaborators, not the conference organizer I nearly ghosted.

The entire system is markdown files.

No fine-tuning. No vector database. No embeddings. No retrieval-augmented generation pipeline. Hierarchical plaintext files in a directory, read by an AI agent at session start. That's it. I'm open-sourcing the whole thing.

---

## The Problem Nobody Talks About

Every AI tool forgets you exist between sessions.

ChatGPT, Copilot, Claude — doesn't matter. You open a new conversation, and the first five minutes are wasted re-explaining who you are, what you're working on, who the people in your life are, what happened last time. You paste in context. You re-describe your preferences. You say "remember, I told you last week..." and it doesn't, because it can't.

This is insane. We've built models that can reason about protein folding and prove mathematical theorems, and they can't remember that I prefer single line breaks in emails.

The real bottleneck isn't intelligence. LLMs are smart enough. The bottleneck is **memory** — persistent, structured, auditable memory that survives between sessions and accumulates over time. The model weights don't need to change. The context does.

So I built a system where the context is always there, always current, and always mine.

---

## The Architecture: Five Layers of Plaintext

The system has five layers, and every single one is a markdown file you can open in any text editor.

**Layer 1 — Senses.** MCP servers connect the AI to Gmail, Google Calendar, and Screenpipe (a local screen + audio recorder). These are the raw data pipes. The AI can read my inbox, check my calendar, and review what I was working on last night — all through standardized tool calls, all with my permission on each action.

**Layer 2 — Sync Engine.** Source adapters query the MCP servers and normalize the data into structured diffs: three new calendar events, one email thread with a reply, a mention of a collaborator's name in a Screenpipe transcript. These diffs flow into the vault.

**Layer 3 — The Vault.** This is the long-term memory. Hierarchical markdown files with naming conventions the AI navigates natively. `user.sarah-kim.md` is a person. `proj.2026.protein-design.md` is a project. `meet.2026.03.14.md` is a meeting. No embeddings needed — the AI finds things by knowing where to look, the same way you would.

**Layer 4 — Command Center.** A working memory file (`_working-memory.md`) tracks what's hot right now — today's calendar, live tasks, stale follow-ups. A context model tracks medium-term state — project momentum, collaborator threads, open decisions. Three tiers of memory: hot, warm, cold. All plaintext.

**Layer 5 — Behavior.** A `CLAUDE.md` file defines who the AI is and how it operates. Skills give it reusable capabilities (email drafting, meeting prep, daily briefing). Auto-memory accumulates learned preferences across sessions. A feedback loop turns corrections into permanent behavioral changes.

The whole thing is git-diffable. I can see exactly what changed between Tuesday and Wednesday in my AI's understanding of the world.

---

## Three Things That Actually Happened

These aren't hypotheticals. These happened last week.

### The Morning Briefing

I open my terminal, start a session, and without typing anything beyond "hey" I get:

> **FOCUS**: Protein binder design — 12 candidates in yeast display pipeline, screening this week. K99 specific aims need Aim 1 preliminary data.
>
> **TODAY**: 10:00 call with Tom (career advice), 14:00 writing block (K99 significance), 16:00 yoga.
>
> **STALE**: Alex Novak — Chronos Bio SAB interest, sent Mar 13, no reply. Consider gentle follow-up. Kevin Wu — cohort metadata received, data use agreement not yet sent.
>
> **MOMENTUM**: Protein design HIGH. K99 MEDIUM. Review article LOW but on track (deadline Apr 15).

The AI assembled this from my calendar, my inbox, my vault notes, and the context model from yesterday's session. I didn't ask for any of it. It just runs. The stale follow-ups alone save me from dropping relationships I care about.

### The Email Draft

A collaborator emails about clock validation data. I say "draft a reply to Kevin." The AI finds the email thread via the Gmail MCP server. It checks Kevin's vault profile — computational epidemiologist, joint project on methylation clocks, last contact March 10, open thread about a data use agreement. It reads our last meeting notes. It drafts:

> Hi Kevin — thanks for the metadata file. I'll run validation against our 2,400-sample cohort this week. Before I start: can you confirm the column names match the schema in your last email? Specifically looking for `cg_id`, `beta_value`, and `sample_age`. Also — I still owe you the signed DUA. Sending by Friday.

One-line review. One "y" to approve the Gmail draft. Done. The tone is mine — direct, specific, leading with what matters. No "I hope this email finds you well." Not ever.

### The Forgotten Promise

Three weeks ago, at a conference, I told a contact I'd send her my preprint on causal aging clocks. Then I flew home, got buried in protein design experiments, and forgot. Completely.

The AI didn't forget. In my morning briefing: **Overdue Follow-Up: Send preprint to Anna Mueller (21 days).** It pulled this from a meeting note I made at the conference — `meet.2026.02.23.md` — where I'd written "promised Anna the causal clock preprint." The staleness sweep caught it, flagged it, surfaced it. I would have lost that relationship over something that took two minutes to fix.

---

## The Feedback Loop — The Part That Surprised Me

I accidentally built RLHF for my personal AI.

Here's what I mean. In machine learning, you improve a model by giving it reward signals — labeled data, human preferences, loss gradients. You need GPUs, datasets, training pipelines. It's a whole infrastructure.

In this system, **natural language corrections are the reward signal.** When I tell the AI "don't double-space after paragraphs in emails," it saves the correction with three things: the rule, **why** the rule exists (recipients could tell the email was AI-drafted from the spacing), and **how to apply** it (all email drafts, all registers). Next session, it reads that file and the behavior changes permanently. No training run. No fine-tuning. No GPU.

The mapping is direct:

- `CLAUDE.md` = base policy
- Skills = sub-policies
- My corrections = reward signal
- Feedback memory files = gradient updates
- AI behavior next session = updated weights

Over 10 sessions, I accumulated about 18 feedback memories. By session 15, the AI's drafts were indistinguishable from my own writing. It knew my pet peeves, my formatting preferences, my communication register for each relationship tier. Not because anyone fine-tuned a model — because markdown files accumulated in a directory, and the AI read them every time.

The part that surprised me: the AI doesn't just memorize rules. It captures the **principle** behind each correction. I told it "never `git init` at `~/`" and explained that a prior `.git` there ballooned to 52GB from tracking binary-heavy subdirectories. Later, when I asked it to initialize a repo in a directory full of `.h5` files, it hesitated and warned me — even though no rule mentioned `.h5` files. It had generalized from the principle. That's judgment, not just compliance.

---

## Safety, in 30 Seconds

Everything is local. The AI drafts emails; it never sends them. Chat messages go to my clipboard; I paste. Every behavioral rule is a line in a markdown file — delete the line, the behavior stops. I can `grep` my entire AI's knowledge base in three seconds. The attack surface is: what the AI can read on my disk, and what I approve it to do. Both are auditable. Try saying that about any other system.

---

## Build Your Own

The [repo](https://github.com/Albert-Ying/agentic-cortex) has everything: a seed vault with example notes, skills, a setup script. Clone it, run `setup.sh`, and you have a working system in 30 minutes. Chapters 1-3 give you persistent memory and a structured vault. Chapter 4 adds the command center briefing. Chapters 5-9 are incremental — add email, calendar, screenpipe, voice profiles, and the feedback loop over days or weeks.

The system works with Claude Code, OpenClaw, Cursor, Windsurf, or any agent that reads `CLAUDE.md` and supports MCP. The notes are just markdown. The memory is just files. The AI is whatever model you want — what matters is the persistent context layer around it.

I've been running this for weeks now. Every session starts where the last one ended. Every correction sticks. Every person, project, and follow-up lives in a file I own. The AI doesn't forget, doesn't drift, and doesn't need re-explaining. It just picks up where we left off and tells me what I need to know.

Nobody's noticed yet. But I notice — every morning, when I sit down and the AI already knows what matters.

[**GitHub: agentic-cortex**](https://github.com/Albert-Ying/agentic-cortex)
