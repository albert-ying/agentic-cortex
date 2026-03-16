---
id: fm4q8wn2k6r1yp3j7x5tdef
title: Multi-Omic Aging Foundation Model
desc: 'Building a foundation model for multi-omic aging prediction across tissues and species'
status: active
updated: 1710050000000
created: 1704000000000
---

# Multi-Omic Aging Foundation Model

## Overview

Pre-training a transformer-based foundation model on large-scale multi-omic data (methylation, transcriptomics, proteomics, metabolomics) to learn unified representations of biological aging. The goal is a single model that can predict tissue-specific aging rates, identify intervention targets, and transfer across species.

This builds on the clock work from [[proj.2025.clock-paper]] but generalizes from methylation-only to arbitrary omic inputs through a modality-agnostic tokenization scheme.

## Current Status

**Momentum**: MEDIUM

Data preprocessing is complete across 4 omic modalities and 12 tissue types from public repositories. Model architecture (cross-modal transformer with modality embeddings) is designed but training has not yet begun — blocked on compute allocation from the Westfield HPC queue.

## People

- [[user.emma-zhang]] — Model architecture and training pipeline. Designed the cross-modal attention mechanism.
- [[user.ryan-patel]] — Data curation and preprocessing. Built the multi-omic tokenizer.
- [[user.jamie-park]] — Project lead. Overall direction and biological interpretation.
- [[user.sarah-kim]] — Advisor. Providing feedback on biological validity of learned features.

## Milestones

- [x] Survey of public multi-omic aging datasets
- [x] Data download and harmonization (GEO, TCGA, GTEx-fictional)
- [x] Modality-agnostic tokenizer implementation
- [x] Cross-modal transformer architecture design
- [ ] HPC compute allocation (pending — submitted request 2026-03-05)
- [ ] Pre-training on combined dataset (~2M samples)
- [ ] Fine-tuning on age prediction benchmarks
- [ ] Zero-shot transfer to mouse aging data
- [ ] Manuscript preparation

## Notes

- 2026-03-10: Discussed architecture at lab meeting. Ryan flagged potential batch effects between GEO and TCGA preprocessing. Need normalization pass before training. See [[meet.2026.03.10]].
- 2026-03-05: Submitted HPC allocation request. Estimated 4 weeks for approval.
- 2026-02-20: Emma finalized the cross-modal attention design. Uses separate projection heads per modality feeding into shared transformer layers.
- Related: [[sci.ml.transformers]], [[sci.biology.aging-clocks]]
