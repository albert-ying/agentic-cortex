---
id: mt1g3lab4k8n2rw6x5jstu
title: Lab Group Meeting
desc: 'Weekly lab meeting — protein design update, foundation model progress, clock follow-up'
date: '2026-03-10'
attendees:
  - '[[user.jamie-park]]'
  - '[[user.sarah-kim]]'
  - '[[user.david-lee]]'
  - '[[user.emma-zhang]]'
  - '[[user.ryan-patel]]'
updated: 1710100000000
created: 1710070000000
---

# Lab Group Meeting — 2026-03-10

## Agenda

1. Protein binder design screening results ([[user.david-lee]])
2. Foundation model architecture and data status ([[user.emma-zhang]], [[user.ryan-patel]])
3. Clock paper follow-up — reviewer response and citation tracking
4. General announcements

## Discussion

### Protein Binder Design

[[user.david-lee]] presented the computational screening results: 47 candidates passed binding energy and shape complementarity thresholds from the initial 12,000-design library. Top hits cluster around two epitope regions on the tau fibril surface.

[[user.sarah-kim]] suggested prioritizing tau binders given new cryo-EM structural data from the Thornton lab (Westfield structural biology). The alpha-synuclein candidates can be revisited later.

David will begin yeast surface display selections next week. Expects preliminary binding data by end of March.

### Foundation Model

[[user.emma-zhang]] walked through the cross-modal transformer architecture: separate projection heads per modality feeding into shared transformer layers with modality embeddings.

[[user.ryan-patel]] flagged potential batch effects between GEO and TCGA data. The preprocessing pipelines use different normalization strategies. Agreed to add a batch correction step (ComBat or equivalent) before training begins.

HPC allocation request submitted March 5 — estimated 4-week wait.

### Clock Paper Follow-Up

The Genome Biology paper has 12 citations since October. Two groups have applied our clock to intervention studies. Sarah suggested reaching out to both for potential collaboration.

## Action Items

- [ ] [[user.david-lee]]: Start yeast display selections for tau binder candidates (by 2026-03-17)
- [ ] [[user.ryan-patel]]: Add batch correction to preprocessing pipeline (by 2026-03-14)
- [ ] [[user.jamie-park]]: Email the two citing groups about potential collaboration
- [ ] [[user.emma-zhang]]: Benchmark modality embedding approach against simple concatenation baseline
- [ ] [[user.sarah-kim]]: Share Thornton lab cryo-EM preprint with the group

## Notes

- Next lab meeting: 2026-03-17
- Sarah reminded everyone that grant progress reports are due April 1
