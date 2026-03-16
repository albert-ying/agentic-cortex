---
id: fm4q8wn2k6r1yp3j7x5tdef
title: Public API Redesign
desc: 'Redesigning the Nimbus public API — RESTful v2 with OpenAPI spec, versioning, and new developer portal'
status: active
updated: 1710050000000
created: 1704000000000
---

# Public API Redesign

## Overview

Nimbus's public API (v1) was built organically over 3 years and has accumulated significant inconsistencies — mixed naming conventions, no versioning strategy, undocumented endpoints, and pagination that works differently across resources. The redesign aims to ship a clean, spec-first v2 API with proper versioning, consistent error handling, rate limiting, and an interactive developer portal.

This is the highest-priority project for the Platform squad in 2026. Customer feedback has consistently flagged API usability as the #1 pain point for integrations.

## Current Status

**Momentum**: HIGH

OpenAPI spec is 70% complete. Backend implementation of core endpoints (projects, tasks, comments) is underway. Frontend API explorer is in design. Versioning strategy decision made: URL-path versioning (`/v2/`). Aiming for developer preview with 5 beta partners by end of April.

## People

- [[user.marcus-johnson]] — Backend implementation lead. Owns the Go service layer and versioning strategy.
- [[user.elena-kowalski]] — Frontend lead. Building the API explorer and developer documentation portal.
- [[user.mei-lin]] — Contributing endpoints for project templates and webhooks.
- [[user.jason-wright]] — Deployment pipeline, canary releases, and feature flag setup.
- [[user.nina-okonkwo]] — Product manager. Owns requirements, customer feedback, and beta program.
- [[user.sam-patel]] — Designer. API explorer UI and documentation design.
- [[user.alex-rivera]] — Tech lead. Architecture decisions, code review, cross-team coordination.

## Milestones

- [x] Audit existing v1 API — document all endpoints, inconsistencies, and breaking changes
- [x] Customer feedback synthesis — 12 interviews on API pain points
- [x] Architecture decision: REST + OpenAPI spec-first approach (over GraphQL)
- [x] Versioning strategy decision: URL-path versioning
- [ ] OpenAPI spec complete for all resources (70% done)
- [ ] Backend implementation of core endpoints (in progress — [[user.marcus-johnson]])
- [ ] API explorer UI (in design — [[user.elena-kowalski]], [[user.sam-patel]])
- [ ] Developer preview program with 5 beta partners (target: end of April)
- [ ] Rate limiting and auth token migration
- [ ] Public launch of v2 API (target: Q3 2026)

## Notes

- 2026-03-14: Sprint planning — scoped next two sprints to finish core endpoint implementation and start API explorer frontend. See [[meet.2026.03.10]].
- 2026-03-12: Marcus and I decided on URL-path versioning after reviewing [[Ben Tran|user.ben-tran]]'s feedback and the Stripe/GitHub API patterns.
- 2026-03-05: Evaluating [[Olivia Chen|user.olivia-chen]]'s openapi-toolkit for spec validation and code generation.
- 2026-02-15: Kicked off project. Priya wants a concrete milestone by end of March — targeting "spec complete + 3 core endpoints working."
- Related: [[sci.engineering.api-design]], [[sci.engineering.distributed-systems]]
