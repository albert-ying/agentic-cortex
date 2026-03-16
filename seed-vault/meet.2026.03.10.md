---
id: mt1g3lab4k8n2rw6x5jstu
title: Sprint Planning — Platform Squad
desc: 'Bi-weekly sprint planning — API redesign focus, mobile app sync, production issue retro'
date: '2026-03-10'
attendees:
  - '[[user.alex-rivera]]'
  - '[[user.marcus-johnson]]'
  - '[[user.elena-kowalski]]'
  - '[[user.jason-wright]]'
  - '[[user.mei-lin]]'
  - '[[user.carlos-reyes]]'
  - '[[user.nina-okonkwo]]'
  - '[[user.sam-patel]]'
updated: 1710100000000
created: 1710070000000
---

# Sprint Planning — Platform Squad — 2026-03-10

## Agenda

1. Previous sprint retro (Sprint 14)
2. API redesign progress and next sprint scope
3. Mobile app status check
4. Production latency issue — post-mortem
5. General updates

## Discussion

### Sprint 14 Retro

Velocity was good — 34 out of 38 story points completed. The 4-point miss was the webhook endpoint spec, which got blocked by an open question about retry semantics. Nina will resolve with customer input this week.

### API Redesign

[[user.marcus-johnson]] walked through the backend progress: projects, tasks, and comments endpoints are implemented and passing integration tests. Next priority is the task filtering API (which [[user.carlos-reyes]] needs for the mobile app) and webhook delivery.

[[user.elena-kowalski]] showed early wireframe implementation of the API explorer. [[user.sam-patel]] presented the design for the interactive "try it" panel. Team feedback: looks great, but needs syntax highlighting for request/response bodies.

[[user.mei-lin]] shipped her first endpoint (project templates). Code review went well — Marcus noted clean error handling.

Decision: Sprint 15 scope = task filtering API + webhook spec + API explorer frontend scaffold.

### Mobile App

[[user.carlos-reyes]] demoed the current build: task list, detail view, and basic navigation are working. Push notification integration is next. Blocked on the task filtering API from Marcus — targeting end of Sprint 15.

### Production Latency Issue

Thursday's latency spike (p99 went from 200ms to 2.5s for 45 minutes). [[user.jason-wright]] ran the post-mortem: root cause was PostgreSQL connection pool exhaustion during a traffic spike from a large customer's integration sync. Fix: added PgBouncer in transaction mode and increased pool limits. Also added better alerting — Datadog will now page at p99 > 500ms.

## Action Items

- [ ] [[user.marcus-johnson]]: Implement task filtering API endpoint (by 2026-03-17)
- [ ] [[user.elena-kowalski]]: Scaffold API explorer frontend with syntax highlighting (by 2026-03-20)
- [ ] [[user.mei-lin]]: Start webhook endpoint implementation (by 2026-03-20)
- [ ] [[user.jason-wright]]: Finalize PgBouncer rollout to all environments (by 2026-03-14)
- [ ] [[user.nina-okonkwo]]: Resolve webhook retry semantics with customer feedback (by 2026-03-14)
- [ ] [[user.carlos-reyes]]: Continue push notification integration; consume task filtering API once available

## Notes

- Next sprint planning: 2026-03-24
- Priya wants a demo of the API explorer at the engineering all-hands on March 28
- Nina is scheduling beta partner onboarding for the last week of April
