# Use frequency analysis to find the key to ciphertext.txt, and then
# decode it.

real_frequencies = {
    11.53: "E",
    9.75: "T",
    8.46: "A",
    8.08: "O",
    7.71: "H",
    6.73: "N",
    6.29: "R",
    5.84: "I",
    5.56: "S",
    4.74: "D",
    3.92: "L",
    3.08: "W",
    2.59: "U",
    2.48: "G",
    2.42: "F",
    2.19: "B",
    2.18: "M",
    2.02: "Y",
    1.58: "C",
    1.08: "P",
    0.84: "K",
    0.59: "V",
    0.17: "Q",
    0.07: "J",
    0.07: "X",
    0.03: "Z",
}

total_letters = 0
encoded_counts = {}
decryption_key = {}

with open("ciphertext.txt") as f:
    encoded_text = f.read()

for char in encoded_text:
    if not char.isalpha():
        continue

    if char not in encoded_counts:
        encoded_counts[char] = 0

    encoded_counts[char] += 1
    total_letters += 1

for char in encoded_counts:
    frequency = round(
        encoded_counts[char] * 100 / total_letters,
        2)
    decryption_key[char] = real_frequencies[frequency]

for char in encoded_text:
    if char in decryption_key:
        char = decryption_key[char]
    print(char, end='')
