---
id: dj2603080xk4m7rqn1v9w3p
title: '2026-03-08'
desc: ''
updated: 1710000000000
created: 1710000000000
---

## State & Open Questions

- Saturday — catching up on technical reading and prep for Monday sprint planning
- Need to finalize the API versioning proposal before the sprint planning meeting
- Open question: should we adopt openapi-toolkit or stick with our custom spec validation?

## Timeline

| Time | Activity | Duration | Key Detail |
|------|----------|----------|------------|
| 10:00 | Chrome — reading | 1.5h | Read Stripe's API versioning blog post and GitHub's API evolution strategy |
| 11:30 | Slack — Ben Tran | 30m | DM thread about API versioning — he recommended URL-path over header-based |
| 12:00 | Lunch break | 1h | Breakfast tacos at Veracruz on South Congress |
| 13:00 | VS Code — api-versioning-doc | 2h | Drafted the versioning strategy proposal document |
| 15:00 | Terminal — testing | 1h | Prototyped URL-path routing in a branch to validate the approach |
| 16:00 | Chrome — openapi-toolkit | 45m | Evaluated Olivia Chen's library; looks solid, good Go integration |
| 16:45 | GitHub — PRs | 30m | Reviewed Marcus's service mesh refactor PR |

## People

- [[Ben Tran|user.ben-tran]] — great DM thread about versioning strategies; he shared how Vercel handles it internally and recommended URL-path. Also connected me to [[Olivia Chen|user.olivia-chen]]'s openapi-toolkit.

## Tasks

- [x] Read Stripe and GitHub API versioning approaches
- [x] Draft versioning strategy proposal
- [x] Prototype URL-path routing
- [x] Review Marcus's PR
- [ ] Evaluate openapi-toolkit more thoroughly (started, need to test with our schema)

## Day Summary

Productive Saturday. Got the versioning strategy proposal drafted — I'm now firmly in the URL-path versioning camp after reading how Stripe and GitHub handle it and getting Ben's perspective from Vercel. Also discovered Olivia Chen's openapi-toolkit which could save us serious work on spec validation.

## Notes

- URL-path versioning wins on simplicity: `/v2/projects` is self-documenting, cacheable at CDN, and doesn't require header inspection. The "but URLs should identify resources not versions" argument is theoretically correct and practically irrelevant.
- openapi-toolkit looks promising. Need to test it with our actual schema before committing.
