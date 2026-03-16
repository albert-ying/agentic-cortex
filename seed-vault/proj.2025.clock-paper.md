---
id: cp2m5vr8k3n1xw7j4q9tghi
title: Multi-Tissue Epigenetic Clock
desc: 'Published paper on a multi-tissue epigenetic clock with improved cross-tissue accuracy'
status: completed
updated: 1706000000000
created: 1685000000000
---

# Multi-Tissue Epigenetic Clock

## Overview

Developed a pan-tissue epigenetic clock trained on methylation array data from 14 human tissue types. The clock achieves lower median absolute error than existing single-tissue clocks when applied across tissues, and identifies a shared set of 412 CpG sites that track aging universally.

Published in *Genome Biology* (2025).

## Publication

- **Title**: A unified multi-tissue epigenetic clock reveals conserved aging signatures across human organs
- **Authors**: Park J, Patel R, Wu K, Kim S
- **Journal**: Genome Biology, 2025; 26:187
- **DOI**: 10.1186/s13059-025-03412-7 (fictional)
- **Preprint**: bioRxiv 2025.04.15.547890 (fictional)

## People

- [[user.jamie-park]] — First author. Clock model development, analysis, writing.
- [[user.ryan-patel]] — Data preprocessing and cross-validation framework.
- [[user.kevin-wu]] — Statistical analysis of tissue-specific CpG variance.
- [[user.sarah-kim]] — Senior author and advisor.

## Milestones

- [x] Data collection from 14 tissue types (n=8,200 samples)
- [x] Feature selection via elastic net with tissue-stratified CV
- [x] Model training and benchmarking against Horvath, Hannum, PhenoAge
- [x] Cross-tissue validation (MAE: 2.8 years vs. 4.1 for next best)
- [x] Biological pathway analysis of 412 universal CpG sites
- [x] Manuscript draft and revision
- [x] Published in Genome Biology (October 2025)

## Notes

- This work directly motivated [[proj.2026.foundation-model]] — the cross-tissue signal suggested a deeper shared representation worth learning.
- Ryan's preprocessing pipeline was reused for the foundation model data curation.
- Kevin has since moved to Lakeview Institute but remains available for follow-up analyses.
- Related: [[sci.biology.aging-clocks]]
