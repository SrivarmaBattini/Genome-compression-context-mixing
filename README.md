# 🧬 Genome Compression using Context Mixing & Arithmetic Encoding

## 📌 Overview
This project implements a **lossless genome compression** algorithm using:

- **N-Gram Models (2-gram & 4-gram)**
- **Context Mixing**
- **Arithmetic Encoding & Decoding**

It is designed to compress viral genome data efficiently while ensuring **zero data loss after decompression**.

---

## 🎯 Motivation

- Genomic data contains huge amounts of information, demanding efficient storage and transmission.
- General-purpose compressors (like ZIP) don't leverage biological patterns.
- We utilize **statistical modeling with n-gram and context mixing**, followed by **arithmetic encoding**, to achieve better compression.
- The algorithm is **lossless** — original data is exactly reconstructed after decoding.

---

## 📂 Datasets Used

We tested our algorithm on **four viral genome datasets**, including:

1. **SARS-CoV-2** (≈ 30,000 bases)
2. **HIV** genome
3. **Influenza A** virus
4. **Sample test genome** (≈ 9,000 bases)

All datasets are in standard **FASTA** format.

---

## ⚙️ Features

- Implements **n-gram modeling** (2-gram and 4-gram)
- Uses **context mixing** to combine predictions from multiple models
- Performs **arithmetic encoding** of the full genome string into a decimal
- **Decodes** the entire genome to verify **data fidelity**
- Calculates:
  - Theoretical compression (using entropy estimation)
  - Actual compression (based on saved binary file size)

---

## ✅ Results

- **Compression Ratio** (Theoretical): ~0.24 – 0.26
- **Actual Compression Ratio** (File Size): ~0.24 – 0.25
- **Decompression Accuracy**: 100% (0 mismatches)
- Successfully tested on all four datasets

---

## 📁 Output Files

- `original_sequence.txt` – Original genome sequence
- `decoded_sequence.txt` – Reconstructed sequence from decoding
- `compressed_genome.bin` – Compressed binary file
- `compression_report.txt` – Summary of results

---

## 🛠 Technologies Used

- **Python 3**
- `decimal`, `math`, `os`, `collections`
- No third-party compression libraries

---

## ▶️ How to Run

1. Place your genome file as `sequences.fasta` in the root folder.
2. Run the script: `python genome_compression.py`
3. Output files and reports will be generated automatically.

---

## 👥 Team Members

- Srivarma Battini – [Add Role if needed]
- [Team Member 2]
- [Team Member 3]

---

## 📚 References

- Mahoney, M. (2005). *Adaptive context mixing for lossless data compression*. Florida Institute of Technology.
- Shibata, H., & Takeda, M. (2011). *Lossless genomic data compression based on context mixing*. Bioinformatics, 27(9), 1216–1222.
- Langdon, G. G. (1984). *An introduction to arithmetic coding*. IBM Journal of Research and Development, 28(2), 135–149.

---

## 🔍 Note

This project demonstrates the potential of **statistical modeling** in genome compression. The encoded data is saved as a binary file, and the **exact original genome** is recovered from it using arithmetic decoding.

