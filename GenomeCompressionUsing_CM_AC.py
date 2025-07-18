from collections import defaultdict
from decimal import Decimal, getcontext
import math
import os


# Load FASTA: removes headers and joins nucleotide lines
def read_fasta(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return ''.join(line.strip() for line in lines if not line.startswith('>')).upper()


# N-gram model (e.g., bigram or 4-gram) to collect next-symbol frequencies
class NGramModel:
    def __init__(self, n):
        self.n = n
        self.context_counts = defaultdict(lambda: defaultdict(int))  

    def train(self, sequence):
        for i in range(len(sequence) - self.n):
            context = sequence[i:i+self.n]
            next_char = sequence[i+self.n]
            self.context_counts[context][next_char] += 1  # Count next char following context

    def predict(self, context):
        if context not in self.context_counts:
            return {ch: 0.25 for ch in 'ACGT'}  # If unseen, use uniform distribution
        counts = self.context_counts[context]
        total = sum(counts.values())
        return {ch: counts.get(ch, 0) / total for ch in 'ACGT'}


# Combines predictions from multiple models (uniformly averaged)
class ContextMixer:
    def __init__(self, models):
        self.models = models

    def mix(self, contexts):
        final_probs = {ch: 0 for ch in 'ACGT'}
        for i, model in enumerate(self.models):
            probs = model.predict(contexts[i])  # Predict using each model
            for ch in 'ACGT':
                final_probs[ch] += probs[ch]
        return {ch: final_probs[ch] / len(self.models) for ch in 'ACGT'}  # Average all models


# Arithmetic Encoding Algorithm
def arithmetic_encode(sequence, probs_fn):
    low, high = Decimal(0), Decimal(1)  # Initial interval [0, 1)
    for i, ch in enumerate(sequence):
        probs = probs_fn(i)  # Get probability distribution for current context
        total = Decimal(0)
        for base in 'ACGT':
            range_width = high - low
            if base == ch:
                high = low + range_width * (total + Decimal(probs[base]))
                low = low + range_width * total
                break
            total += Decimal(probs[base])
    return (low + high) / 2  # Final encoded value lies inside the final interval


# Arithmetic Decoding Algorithm
def arithmetic_decode(encoded_value, probs_fn, sequence_length):
    result = ""
    value = Decimal(encoded_value)
    low = Decimal(0)
    high = Decimal(1)
    for i in range(sequence_length):
        probs = probs_fn(i)
        total = Decimal(0)
        for base in 'ACGT':
            prev_total = total
            total += Decimal(probs[base])
            range_width = high - low
            curr_low = low + range_width * prev_total
            curr_high = low + range_width * total
            if curr_low <= value < curr_high:
                result += base  
                low, high = curr_low, curr_high  
                break
    return result



# Load and prepare the input DNA sequence
sequence = read_fasta("Dengue_virus_1.fasta")
original = sequence  

# Train two n-gram models: bigram and 4-gram
model_2gram = NGramModel(2)
model_4gram = NGramModel(4)
model_2gram.train(sequence)
model_4gram.train(sequence)

# ContextMixer to combine both models
mixer = ContextMixer([model_2gram, model_4gram])

# Returns the mixed probability at position `i`
def get_mixed_probs(i):
    context2 = sequence[i:i+2]
    context4 = sequence[i:i+4]
    return mixer.mix([context2, context4])


getcontext().prec = 50000
encoded_val = arithmetic_encode(original, get_mixed_probs)
decoded_seq = arithmetic_decode(encoded_val, get_mixed_probs, len(original))
mismatches = sum(1 for a, b in zip(original, decoded_seq) if a != b)

# Entropy-based estimate of total bits required for encoding
compressed_bits = 0
for i, ch in enumerate(original):
    probs = get_mixed_probs(i)
    prob = probs.get(ch, 1e-10)  
    compressed_bits += -math.log2(prob)  


original_bits = len(original) * 8  # 8 bits per character (ASCII)
compression_ratio = compressed_bits / original_bits # Theoretical caculation


with open("original_sequence.txt", "w", encoding="utf-8") as f:
    f.write(original)

with open("decoded_sequence.txt", "w", encoding="utf-8") as f:
    f.write(decoded_seq)


num_bits = math.ceil(compressed_bits)
integer_representation = int(encoded_val * (2 ** num_bits))
byte_data = integer_representation.to_bytes((num_bits + 7) // 8, 'big')
with open("compressed_genome.bin", "wb") as f:
    f.write(byte_data)

# Calculate file sizes in bytes
compressed_size = os.path.getsize("compressed_genome.bin")
original_size = os.path.getsize("Dengue_virus_1.fasta")
actual_ratio = compressed_size / original_size  


print("Total characters compressed:", len(original))
print("Mismatches after decompression:", mismatches)
print("Original size (bits):", original_bits)
print("Estimated compressed size (bits):", int(compressed_bits))
print("Theoretical compression ratio:", round(compression_ratio, 4))
print("Physical compressed size (bytes):", compressed_size)
print("Physical original size (bytes):", original_size)
print("Actual compression ratio (file size):", round(actual_ratio, 4))
