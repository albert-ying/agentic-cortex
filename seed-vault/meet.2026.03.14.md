---
id: mt2h7adv5k9n3sw1x6jvwx
title: '1:1 with Priya Sharma'
desc: 'Weekly 1:1 — API redesign progress, team health, career growth'
date: '2026-03-14'
attendees:
  - '[[user.alex-rivera]]'
  - '[[user.priya-sharma]]'
updated: 1710400000000
created: 1710380000000
---

# 1:1 with Priya Sharma — 2026-03-14

## Agenda

1. API redesign: progress toward end-of-March milestone
2. Production incident follow-up
3. Team health and Mei Lin's ramp-up
4. Career: Staff engineer path discussion

## Discussion

### API Redesign Progress

Priya is happy with the momentum. Core endpoints are implemented, versioning strategy is locked, and the API explorer design looks strong. The end-of-March milestone ("spec complete + 3 core endpoints working") is on track.

She asked about the beta partner program timeline. I confirmed Nina is targeting last week of April for onboarding the first 5 partners. Priya wants at least one "lighthouse customer" — a well-known company using the v2 API that we can reference publicly.

### Production Incident

Priya appreciated the fast post-mortem from Jason. She asked two questions: (1) why didn't our monitoring catch it sooner? (2) what's the systemic fix beyond PgBouncer? I explained that the alerting gap is now closed (Datadog page at p99 > 500ms) and that the systemic fix is the connection pooling architecture change that's part of the API redesign infrastructure work.

She flagged this as a talking point for the board update — "proactive reliability investment" framing.

### Team Health

Mei Lin is ramping well — shipped her first endpoint this week and Marcus is a good mentor for her. Priya suggested giving Mei more ownership on a bounded feature area (webhooks) to accelerate her growth.

Carlos is doing great on mobile but starting to feel isolated as the only mobile engineer. Priya is considering whether to hire a second mobile developer in Q3 if the app gets traction.

Elena and Sam continue to be a strong design-engineering pair.

### Staff Engineer Path

Priya brought this up proactively. If the API redesign ships well and I demonstrate cross-team influence (specifically: getting the Growth squad to adopt the v2 API), she'd support a Staff promotion in the fall cycle.

Key areas to demonstrate: (1) technical leadership beyond my squad, (2) written communication (RFCs, architecture docs), (3) mentoring impact (Mei's growth is a good signal).

She suggested I write up the API versioning decision as a company-wide RFC to increase visibility.

## Action Items

- [ ] [[user.alex-rivera]]: Write API versioning RFC and circulate to engineering org (by 2026-03-21)
- [ ] [[user.alex-rivera]]: Identify lighthouse customer candidate for beta program (discuss with Nina)
- [ ] [[user.alex-rivera]]: Give Mei ownership of webhook feature area
- [ ] [[user.priya-sharma]]: Evaluate mobile team headcount for Q3 planning
- [ ] [[user.priya-sharma]]: Include API redesign in board reliability narrative

## Notes

- Next 1:1 scheduled for 2026-03-21
- Priya mentioned the engineering all-hands demo on March 28 — I should present the API redesign progress
- The Staff path conversation is encouraging. Need to be more intentional about cross-team visibility.
