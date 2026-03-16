---
id: sc3p5alpha6k2n8qw4x1jpqr
title: AlphaFold and Protein Structure Prediction
desc: 'AlphaFold system for protein structure prediction and its impact on design'
domain: protein-design
subdomain: structure-prediction
updated: 1709000000000
created: 1692000000000
---

# AlphaFold and Protein Structure Prediction

## Overview

AlphaFold (DeepMind) solved the protein structure prediction problem for single-chain proteins, achieving atomic-level accuracy. AlphaFold2 uses an attention-based architecture with multiple sequence alignments (MSAs) and structural templates, while AlphaFold3 extends to complexes, nucleic acids, and small molecules. These tools have transformed computational protein design by providing reliable structure predictions as starting points for binder and enzyme engineering.

## Key Concepts

- **Evoformer module**: Processes MSA and pair representations through alternating row/column attention
- **Structure module**: Iteratively refines 3D coordinates using invariant point attention (IPA)
- **Confidence metrics**: pLDDT (per-residue confidence), PAE (predicted aligned error for domain relationships)
- **AlphaFold2 vs. AlphaFold3**: AF3 handles protein-protein, protein-DNA, and protein-ligand complexes
- **ColabFold**: Accelerated AlphaFold pipeline using MMseqs2 for MSA generation
- **RoseTTAFold**: Independent two-track architecture with comparable accuracy
- **Design applications**: Predicted structures used as templates for Rosetta-based binder design, hallucination, and diffusion models (RFdiffusion)
- **Limitations**: Less reliable for disordered regions, conformational ensembles, and allosteric states

## Related Papers

- Jumper J et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*.
- Abramson J et al. (2024). Accurate structure prediction of biomolecular interactions with AlphaFold 3. *Nature*.
- Watson JL et al. (2023). De novo design of protein structure and function with RFdiffusion. *Nature*.

## Related Projects

- [[proj.2026.protein-design]] — Uses AlphaFold-predicted aggregate structures as design targets
