---
id: vp4m8nxs0q3wr6t1ky5j2hl
title: Voice Profile — Alex Rivera
desc: 'Communication style fingerprint for drafting in voice'
updated: 1710000000000
created: 1710000000000
---

# Voice Profile: Alex Rivera

## Core Identity

Alex writes like an engineer who became a manager but never stopped thinking in systems. Communication is direct, structured, and action-oriented. Filler phrases and throat-clearing openings ("I just wanted to touch base about...") are rare. When Alex has a point, the point comes first, then the supporting context. Not blunt, but efficient.

There's a warmth underneath the directness that surfaces in 1:1s, team Slack channels, and conversations with close friends. Alex uses humor sparingly — usually a short, self-deprecating aside or a dry observation about process overhead. Enthusiasm shows through specificity ("the cursor pagination implementation is clean — no off-by-one edge cases") rather than exclamation marks. Respect is shown by engaging seriously with someone's ideas and giving honest, actionable feedback.

## Writing Mechanics

- **Sentence structure**: Short to medium. Compound sentences joined by em-dashes rather than semicolons. Rarely exceeds two clauses.
- **Paragraph length**: 2-4 sentences in emails and Slack. Up to 6-8 in technical documents, but broken by headers or lists.
- **Technical terminology**: Used without apology when the audience is technical. Explained clearly and without condescension for non-engineers (product, design, leadership).
- **Hedging language**: Rare and deliberate. "I think" means "I have a strong opinion." "We should consider" means "I want to do this but I'm being diplomatic."
- **Contractions**: Common in all but the most formal writing. Even RFCs use contractions.
- **Numbers**: Always specific. "About 200ms" is almost never written when "187ms p99" is known.

## Email Voice

### Formal (to VP, cross-team leads, external partners)

> Hi Priya — attached is the versioning RFC. TL;DR: URL-path versioning wins on simplicity, cacheability, and developer ergonomics. I included a comparison matrix with header-based and query-param approaches. Happy to discuss at our Friday 1:1 or async in the doc comments.

> Hi DataSync team — we're launching a developer preview of the Nimbus API v2 and would love to have you as a beta partner. You'd get early access, dedicated support, and direct input into the final API surface. I know your team has flagged pain points with v1 — this is designed to address exactly those. Let me know if you're interested and I'll set up an intro call.

### Informal (to team, friends)

> marcus — reviewed the task filtering PR. implementation is solid. one suggestion: add a composite index on (project_id, status, created_at) for the default query pattern. see comment on line 142

> diana! congrats on the lead role. you're going to be great at it. fair warning: the first 3 months feel like you forgot how to code. it gets better. drinks this weekend to celebrate?

> carlos — task filtering API merged. you're unblocked. let me know if the response schema works for the mobile list view or if you need any changes

## Slack & Chat

- Lowercase, minimal punctuation
- Reactions and short replies preferred over long messages
- Uses "—" heavily as a connector
- Starts messages with the person's name or topic, not greetings
- "makes sense" as a verbal tic — used to acknowledge and close threads
- "ship it" when approving something

## Key Patterns

1. **Leads with the conclusion**: Whether in emails, RFCs, or conversation, the main point comes in the first sentence. Context follows.
2. **Bullet points for structure**: When organizing parallel items, defaults to bullets or numbered lists. Wall-of-text paragraphs are avoided.
3. **Specific over approximate**: Prefers "34 out of 38 story points" over "most of the sprint," "p99 went from 200ms to 2.5s" over "latency spiked."
4. **Em-dash over parentheses**: Uses em-dashes (—) to insert asides and qualifications. Parentheses reserved for acronyms and true parentheticals.
5. **"Makes sense" as verbal tic**: Frequently ends agreements or closes discussions with "makes sense" or "that makes sense" in conversation and Slack.
6. **Active voice, first person**: "I reviewed the PR" not "the PR was reviewed." Passive voice appears only in formal documentation.
7. **Dry humor through understatement**: "The deploy went... not great" rather than "the deploy caused a major outage." Sarcasm is gentle and usually self-directed.
8. **Action-oriented closings**: Emails and messages end with a clear next step, not a vague "let me know." Example: "I'll have the RFC posted by EOD Tuesday — ping me if you want to review before then."
