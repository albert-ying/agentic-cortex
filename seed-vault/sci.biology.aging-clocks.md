---
id: sc1b7aging3k9m2nqw5xjkl
title: Epigenetic Aging Clocks
desc: 'Overview of epigenetic clocks for biological age estimation'
domain: biology
subdomain: aging
updated: 1710000000000
created: 1690000000000
---

# Epigenetic Aging Clocks

## Overview

Epigenetic clocks are mathematical models that estimate biological age from DNA methylation patterns at specific CpG sites. They have become central tools in aging research for measuring the rate of biological aging and evaluating interventions.

## Key Concepts

- **Chronological vs. biological age**: Clocks measure deviation from expected methylation state for a given chronological age
- **First-generation clocks**: Trained to predict chronological age (Horvath 2013, Hannum 2013)
- **Second-generation clocks**: Trained to predict mortality/morbidity outcomes (PhenoAge, GrimAge)
- **Third-generation clocks**: Causal/interventional clocks (DunedinPACE — pace of aging)
- **Pan-tissue vs. tissue-specific**: Some clocks generalize across tissues, others are optimized for blood or specific organs
- **CpG site selection**: Typically 300-500 sites selected via penalized regression (elastic net)
- **Acceleration**: Residual of predicted age minus chronological age, associated with disease risk
- **Intervention readout**: Caloric restriction, reprogramming, and senolytics show clock reversal in model organisms

## Related Papers

- Horvath S (2013). DNA methylation age of human tissues and cell types. *Genome Biology*.
- Hannum G et al. (2013). Genome-wide methylation profiles reveal quantitative views of human aging rates. *Molecular Cell*.
- Levine ME et al. (2018). An epigenetic biomarker of aging for lifespan and healthspan. *Aging*.
- Belsky DW et al. (2022). DunedinPACE, a DNA methylation biomarker of the pace of aging. *eLife*.

## Related Projects

- [[proj.2025.clock-paper]] — Our multi-tissue clock extending these ideas across 14 tissue types
- [[proj.2026.foundation-model]] — Generalizing clock concepts to multi-omic foundation models
