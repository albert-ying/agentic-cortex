---
id: sc2m9trans4k7n1pw3x5jmno
title: Transformers for Biological Sequences
desc: 'Transformer architectures adapted for protein, DNA, and multi-omic data'
domain: ml
subdomain: transformers
updated: 1709500000000
created: 1695000000000
---

# Transformers for Biological Sequences

## Overview

Transformer models, originally developed for NLP, have been successfully adapted for biological sequence modeling. Protein language models (ESM, ProtTrans), genomic models (Enformer, Nucleotide Transformer), and multi-omic models apply self-attention to capture long-range dependencies in biological data.

## Key Concepts

- **Self-attention over sequences**: Captures relationships between distant residues/bases without fixed window sizes
- **Protein language models**: ESM-2, ProtTrans — pre-trained on millions of protein sequences, embeddings encode structure and function
- **Genomic transformers**: Enformer predicts gene expression from DNA sequence; Nucleotide Transformer handles variable-length genomic inputs
- **Tokenization strategies**: k-mer tokenization for DNA, single amino acid tokens for proteins, modality-specific tokenizers for multi-omic data
- **Cross-modal attention**: Mechanism for integrating heterogeneous data types (e.g., methylation + expression) in a shared representation space
- **Pre-training objectives**: Masked language modeling (MLM) for sequences, contrastive learning for multi-modal alignment
- **Fine-tuning for downstream tasks**: Age prediction, variant effect prediction, protein fitness landscapes
- **Scaling laws**: Larger models trained on more data consistently improve biological prediction tasks

## Related Papers

- Rives A et al. (2021). Biological structure and function emerge from scaling unsupervised learning. *PNAS*.
- Avsec Z et al. (2021). Effective gene expression prediction from sequence by integrating long-range interactions. *Nature Methods*.
- Dalla-Torre H et al. (2023). The Nucleotide Transformer. *Nature Methods*.

## Related Projects

- [[proj.2026.foundation-model]] — Our cross-modal transformer for multi-omic aging prediction
- [[proj.2026.protein-design]] — Uses ESM embeddings for binder candidate scoring
