import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(parent_dir, "word_count"))
# pylint: disable=import-error
from word_count import word_count  # nopep8


with open("robin.txt") as f:
    sentence = f.read()
    word_list = word_count(sentence)

sorted_list = {}
max_count = 0
longest_word_length = 0

for word, count in word_list.items():
    if len(word) > longest_word_length:
        longest_word_length = len(word)

    if count not in sorted_list:
        sorted_list[count] = []

        if count > max_count:
            max_count = count

    sorted_list[count].append(word)

for count in range(max_count, 0, -1):
    if count not in sorted_list:
        continue
    for word in sorted(sorted_list[count]):
        print(word, end=' ')
        print(' ' * (longest_word_length-len(word)), end='')
        print('#' * count)
