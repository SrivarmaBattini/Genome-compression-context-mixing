# Modelling Genome Compression in Viruses: Implementation of Context Mixing (CM)

## 📘 Overview

This project implements **lossless genome data compression** using **N-gram-based Context Mixing** and **Arithmetic Encoding** techniques. The main objective is to reduce the size of viral genome sequences (e.g., SARS-CoV-2) without any data loss during decompression.

---

## 🧠 Motivation

- Biological data like genome sequences are huge and growing rapidly.
- Efficient storage and transmission of this data is critical.
- Traditional compression tools (ZIP, GZIP) are not optimized for genomic structure.
- We leverage statistical models to achieve better, domain-specific compression.

---

## 🔍 Methodology

1. **Read and Preprocess** FASTA-formatted genome sequences.
2. **Train N-gram Models** (2-gram and 4-gram) to estimate symbol probabilities.
3. **Context Mixing**: Combine predictions from multiple models.
4. **Arithmetic Encoding**: Compress the sequence into a single floating-point number.
5. **Arithmetic Decoding**: Reconstruct the original sequence using the same models.
6. **Evaluation**: Check for mismatches and compute compression ratios.

---

## 📂 Dataset

We used FASTA files containing virus genome sequences, including:
- SARS-CoV-2 (≈30,000 characters)
- Two additional sample virus genome datasets

---

## 💻 Project Structure

```bash
.
├── sequences.fasta                # Input FASTA file
├── original_sequence.txt          # Extracted input sequence (A, C, G, T only)
├── decoded_sequence.txt           # Sequence after decompression
├── compressed_genome.bin          # Compressed binary output
├── report.pdf                     # Detailed project report (optional)
├── README.md                      # Project overview and instructions
└── genome_compression.py         # Main Python script
