---
id: sc1b7dsptr3k9m2nqw5xjkl
title: Distributed Systems Patterns
desc: 'Key distributed systems concepts relevant to API platform design'
domain: engineering
subdomain: distributed-systems
updated: 1710000000000
created: 1690000000000
---

# Distributed Systems Patterns

## Overview

Notes on distributed systems patterns relevant to building reliable API platforms and SaaS infrastructure. Most of this comes from practical experience at Nimbus and reading from Kleppmann, Nygard, and various conference talks.

## Key Concepts

- **CAP theorem**: In practice, the choice is between consistency and availability during network partitions. For Nimbus's use case (project management), we favor availability — eventual consistency is acceptable for most operations.
- **Circuit breaker pattern**: Prevents cascading failures when downstream services are unhealthy. We use this between our API gateway and internal microservices. Nygard's *Release It!* is the canonical reference.
- **Rate limiting strategies**: Token bucket vs. sliding window. We chose sliding window with Redis for the v2 API — more predictable behavior for customers and easier to reason about.
- **Idempotency keys**: Essential for safe retries on non-GET requests. The v2 API requires idempotency keys for all POST/PUT/PATCH endpoints. Stripe's implementation is the gold standard.
- **Event sourcing vs. CRUD**: Considered event sourcing for the task activity log. Decided against full event sourcing — too complex for our scale — but adopted an append-only activity stream pattern.
- **Connection pooling**: The production latency spike (March 2026) was caused by PostgreSQL connection pool exhaustion under load. PgBouncer in transaction mode solved it.
- **Observability**: Structured logging (JSON) + distributed tracing (OpenTelemetry) + metrics (Datadog). The three pillars.
- **Graceful degradation**: API should return partial results rather than 500 errors when non-critical subsystems are down.

## Reading List

- Kleppmann M (2017). *Designing Data-Intensive Applications*. O'Reilly.
- Nygard M (2018). *Release It! Design and Deploy Production-Ready Software*. 2nd edition. Pragmatic Bookshelf.
- Burns B (2018). *Designing Distributed Systems*. O'Reilly.

## Related Projects

- [[proj.2026.api-redesign]] — Applying these patterns to the v2 API platform
- [[proj.2025.auth-migration]] — Circuit breaker and graceful degradation were key during the migration rollout
