---
id: dj2603113dw7q0vtn4z8a6s
title: '2026-03-11'
desc: ''
updated: 1710000000000
created: 1710000000000
---

## State & Open Questions

- Focus: finish tau binder filtering and send David the prioritized list
- Need to start thinking seriously about K99 specific aims — Sarah mentioned it twice now
- Question: should I include the Chronos Bio advisory work on my biosketch?

## Timeline

| Time | Activity | Duration | Key Detail |
|------|----------|----------|------------|
| 9:00 | VS Code — protein-design | 3h | Completed tau-specific filtering pipeline; 12 candidates confirmed |
| 12:00 | Slack — David | 15m | Sent prioritized candidate list with structural annotations |
| 12:15 | Lunch — desk | 30m | Sandwich while reading papers |
| 12:45 | Chrome — K99 resources | 1.5h | Read NIH K99 guide, sample aims, success stories |
| 14:15 | VS Code — k99-draft | 1h | Created outline for specific aims page |
| 15:15 | Zoom — 1:1 with Sarah | 30m | Discussed K99 framing: computational aging biology angle |
| 15:45 | Slack — lab channel | 15m | Emma shared updated loss curves; still plateaued |
| 16:00 | VS Code — emma-clock-debug | 1h | Looked at Emma's model code; found a data leakage issue |
| 17:00 | Chrome — email | 30m | Responded to [[Rachel Brown\|user.rachel-brown]] about cohort data access |

## People

- [[David Lee|user.david-lee]] — sent him the 12 tau-specific binder candidates with Rosetta scores and structural notes
- [[Sarah Kim|user.sarah-kim]] — 1:1 meeting; agreed K99 should frame around "computational design of aging interventions," combining protein binders + clock prediction
- [[Emma Zhang|user.emma-zhang]] — found data leakage in her training pipeline (validation samples leaking into training set via shared patients); she was relieved
- [[Rachel Brown|user.rachel-brown]] — she can share Lakeview cohort metadata by next week; full data needs IRB amendment

## Tasks

- [x] Complete tau-specific binder filtering
- [x] Send prioritized list to David
- [x] 1:1 with Sarah about K99
- [x] Debug Emma's clock model (found data leakage)
- [ ] Draft K99 specific aims page (started outline)
- [ ] Follow up with Rachel about IRB timeline

## Day Summary

Major progress day. Finished the tau binder filtering pipeline and got the prioritized 12 candidates to David. Had a productive K99 conversation with Sarah — the framing of "computational design of aging interventions" bridges both the protein binder and clock prediction threads of my work nicely. Also helped Emma find a nasty data leakage bug in her clock model, which should unstick her training.

## Notes

- The K99 framing is coming together. Sarah's suggestion to unify the two threads (structural biology + ML clocks) under an "aging interventions" umbrella is smart and fundable.
- Data leakage is such a common trap in biological ML. Emma's leak was subtle — shared patient IDs across train/val splits, so the model was memorizing patient-level patterns. Classic.
