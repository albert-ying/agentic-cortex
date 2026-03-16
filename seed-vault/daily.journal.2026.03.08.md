---
id: dj2603080xk4m7rqn1v9w3p
title: '2026-03-08'
desc: ''
updated: 1710000000000
created: 1710000000000
---

## State & Open Questions

- Primary focus: getting the tau binder docking runs finished before Monday lab meeting
- Need to decide whether to include the alpha-synuclein controls in the presentation
- Open question: is the Rosetta energy threshold too aggressive? 47 candidates might be too narrow

## Timeline

| Time | Activity | Duration | Key Detail |
|------|----------|----------|------------|
| 9:30 | VS Code — protein-design | 3h | Reran Rosetta docking with relaxed energy cutoff |
| 12:30 | Chrome — literature search | 45m | Read two papers on tau fibril polymorphs |
| 13:15 | Lunch break | 45m | Ate at the Quad cafe |
| 14:00 | Terminal — cluster jobs | 1h | Submitted batch scoring on Westfield HPC |
| 15:00 | Slack — lab channel | 30m | Discussed screening timeline with [[David Lee\|user.david-lee]] |
| 15:30 | VS Code — protein-design | 2h | Wrote analysis script for binding energy distributions |
| 17:30 | Papers — reading | 1h | Reviewed Anna's recent preprint on aggregate binders |

## People

- [[David Lee|user.david-lee]] — confirmed yeast display plates arrive Tuesday; discussed whether to add tau-P301S mutant
- [[Anna Mueller|user.anna-mueller]] — read her new preprint on aggregate-selective nanobodies; worth citing in our manuscript

## Tasks

- [x] Rerun docking with -1.5 REU cutoff instead of -2.0
- [x] Submit batch jobs to HPC cluster
- [ ] Compile binding energy distributions for Monday presentation
- [ ] Email [[Kevin Wu|user.kevin-wu]] about accessing clock validation cohort data

## Day Summary

Spent most of the day on computational work for [[proj.2026.protein-design]]. Relaxing the energy cutoff brought the candidate pool from 47 to 83 designs, which gives David more to work with experimentally. Also caught up on literature — Anna Mueller's preprint from Heidelberg has some relevant methodology we should reference.

## Notes

- The relaxed cutoff feels right. 47 was probably leaving good candidates on the table. Sarah will want justification for the threshold change though — need to prepare a comparison plot.
- Saturday work session, but productive. The quiet lab is good for deep computational focus.
