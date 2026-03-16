---
id: prd8v2kx7m3nq1w5j9t4abc
title: Protein Binder Design for Aging Aggregates
desc: 'Designing novel protein binders targeting age-related protein aggregates using computational and experimental approaches'
status: active
updated: 1710100000000
created: 1700000000000
---

# Protein Binder Design for Aging Aggregates

## Overview

Computational design of de novo protein binders that target misfolded protein aggregates implicated in age-related neurodegeneration. The project combines structure-based design with high-throughput experimental screening to identify candidates with therapeutic potential.

The core hypothesis is that rationally designed binders can selectively recognize aggregated conformations over native monomers, enabling targeted clearance without disrupting normal protein function.

## Current Status

**Momentum**: HIGH

The computational screening phase is complete. We identified 47 candidate binders from an initial library of ~12,000 designs. Experimental validation via yeast surface display is underway in [[user.david-lee]]'s hands, with preliminary binding data expected by end of March.

## People

- [[user.sarah-kim]] — PI and project advisor. Secured funding through the Westfield Aging Initiative.
- [[user.david-lee]] — Lead experimentalist. Running yeast display selections and SPR validation.
- [[user.jamie-park]] — Computational design lead. Rosetta-based pipeline and scoring.

## Milestones

- [x] Literature review and target selection (amyloid-beta, tau, alpha-synuclein conformations)
- [x] Structural modeling of aggregate epitopes
- [x] Computational binder library generation (~12,000 designs)
- [x] Scoring and filtering to top 47 candidates
- [ ] Yeast surface display screening (in progress — [[user.david-lee]])
- [ ] SPR binding affinity measurements
- [ ] Cryo-EM structural validation of top 3 hits
- [ ] Manuscript draft

## Notes

- 2026-03-10: Presented screening results at lab meeting. Sarah suggested prioritizing tau binders given new structural data from the Thornton lab. See [[meet.2026.03.10]].
- 2026-02-18: Completed Rosetta scoring. 47 designs pass binding energy and shape complementarity thresholds.
- 2026-01-15: Settled on three aggregate targets after discussion with David. Alpha-synuclein deprioritized due to conformational heterogeneity.
- Related: [[sci.protein-design.alphafold]], [[sci.biology.aging-clocks]]
