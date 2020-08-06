import random

# Read in all the words in one go
with open("input.txt") as f:
    words = f.read().split()

next_words = {}
start_words = []
end_words = set()

def is_start_word(word):
    return word[0].isupper() or (word[0] == '"' and word[1].isupper())

# Analyze which words can follow other words
for i in range(len(words)-1):
    word = words[i]
    following_word = words[i+1]

    if is_start_word(word):
        start_words.append(word)

    end_punctuation = ['.', '!', '?']
    if word[-1] in end_punctuation or (word[-1] == '"' and word[-2] in end_punctuation):
        end_words.add(word)

    # if is_start_word(following_word):
    #     continue

    if word not in next_words:
        next_words[word] = [following_word]
    # elif following_word not in next_words[word]:
    else:
        next_words[word].append(following_word)


# Construct 5 random sentences
def make_sentence():
    current_word = random.choice(start_words)
    while current_word not in end_words and current_word in next_words:
        print(current_word, end=" ")
        current_word = random.choice(next_words[current_word])
    print(current_word)

for i in range(5):
    make_sentence()
    print("")
