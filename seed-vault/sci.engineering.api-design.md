---
id: sc2m9trans4k7n1pw3x5jmno
title: REST vs GraphQL API Design
desc: 'Comparison of API design approaches and principles for public APIs'
domain: engineering
subdomain: api-design
updated: 1709500000000
created: 1695000000000
---

# REST vs GraphQL API Design

## Overview

When redesigning the Nimbus public API, we evaluated REST, GraphQL, and gRPC. This note captures the decision rationale and key design principles we adopted.

## Decision: REST + OpenAPI

We chose REST with OpenAPI spec-first design. The reasoning:

1. **Customer familiarity**: 90% of our integrators are small-to-mid dev teams. REST is what they know. GraphQL adds a learning curve that's not justified for our data model.
2. **Caching**: REST's HTTP caching semantics (ETags, Cache-Control) are well-understood and work at the CDN layer. GraphQL caching is significantly more complex.
3. **Tooling maturity**: OpenAPI has a massive ecosystem — code generation, documentation, testing, mocking. GraphQL tooling is good but narrower.
4. **Rate limiting simplicity**: Per-endpoint rate limiting is straightforward with REST. GraphQL query complexity analysis is an ongoing headache for API providers.

GraphQL would have made sense if our data model had deep, flexible relationships that customers query in varied patterns. Our model is relatively flat (projects → tasks → comments) and REST handles it cleanly.

## Key Design Principles

- **Spec-first development**: OpenAPI spec is the source of truth. Code is generated from the spec, not the other way around. Using [[Olivia Chen|user.olivia-chen]]'s openapi-toolkit for validation.
- **Consistent resource naming**: Plural nouns, lowercase, kebab-case. `/v2/projects/{id}/tasks`, not `/v2/getProjectTasks`.
- **Pagination**: Cursor-based pagination everywhere. No offset/limit — it breaks under concurrent writes.
- **Error responses**: RFC 7807 Problem Details format. Every error has a `type`, `title`, `status`, `detail`, and `instance`.
- **Versioning**: URL-path versioning (`/v2/`). Clean, explicit, and cache-friendly.
- **Idempotency**: Required `Idempotency-Key` header for all mutating requests.
- **Filtering**: Consistent query parameter syntax. `?status=active&assignee=user_123&sort=-created_at`.

## References

- Stripe API Design Guide (internal reference for consistency patterns)
- GitHub REST API v3 (pagination and error handling patterns)
- Google API Design Guide (resource-oriented design)

## Related Projects

- [[proj.2026.api-redesign]] — Implementing these principles in the v2 API
