---
id: prd8v2kx7m3nq1w5j9t4abc
title: Nimbus Mobile Companion App
desc: 'Building the first Nimbus mobile app — task management, notifications, and project views'
status: active
updated: 1710100000000
created: 1705000000000
---

# Nimbus Mobile Companion App

## Overview

Nimbus has been web-only since launch. Customer demand for mobile access has been the #2 most-requested feature for two years running. The mobile companion app will provide task management, push notifications, and project overview — not a full parity port, but the core workflows people need on the go.

Built in React Native for iOS and Android. Leveraging the new v2 API endpoints from [[proj.2026.api-redesign]] as they land.

## Current Status

**Momentum**: MEDIUM

Architecture and core navigation are in place. Task list and detail views are functional in a dev build. Push notifications integration is in progress. Blocked on some v2 API endpoints not being ready yet — mobile needs the new task filtering API that Marcus hasn't built yet.

## People

- [[user.carlos-reyes]] — Mobile lead and primary developer. React Native + Swift.
- [[user.sam-patel]] — Mobile design. Wireframes and interaction patterns.
- [[user.nina-okonkwo]] — Product manager. MVP scope and launch plan.
- [[user.alex-rivera]] — Tech lead oversight. Cross-project coordination with API redesign.

## Milestones

- [x] React Native project setup and CI pipeline
- [x] Core navigation and app shell
- [x] Task list and detail views
- [ ] Push notification integration (in progress — [[user.carlos-reyes]])
- [ ] Project overview dashboard
- [ ] Offline mode for task updates
- [ ] Internal beta (target: end of April)
- [ ] TestFlight / Play Store internal testing (target: May)
- [ ] Public launch (target: Q3 2026, alongside API v2)

## Notes

- 2026-03-12: Architecture review with Carlos. Decided on React Native over Flutter after evaluating both. RN gives better code sharing with our existing web React codebase.
- 2026-03-05: Carlos flagged dependency on the v2 task filtering API. Added to API redesign backlog as a priority.
- 2026-02-20: Nina's customer research shows top mobile use cases: (1) quick task status checks, (2) notification triage, (3) commenting on tasks from phone. Not project creation or complex views.
- Dependency: [[proj.2026.api-redesign]] — mobile app consumes v2 API endpoints
