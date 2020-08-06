import random
import re


end_punctuation = ['.', '!', '?']
quote_chars = ['"', "'"]

def is_start_word(word):
    if word[0].isupper():
        return True
    elif len(word) > 1 and word[0] == '"' and word[1].isupper():
        return True
    else:
        return False

def is_end_word(word):
    
    if word[-1] in end_punctuation:
        return True
    elif len(word) > 1 and word[-1] == '"' and word[-2] in end_punctuation:
        return True
    else:
        return False

def starts_quote(word):
    if word[0] in quote_chars:
        return word[0]
    else:
        return None

def ends_quote(word):
    if word[-1] in quote_chars:
        return word[-1]
    else:
        return None


# Read in all the words in one go
with open("input.txt") as f:
    without_parens = re.sub(r"[\(\)\n]", " ", f.read())
    words = re.split(r"\s+|--", without_parens)

next_words = {}
start_words = []
end_words = set()

# Analyze which words can follow other words
for i in range(len(words)-1):
    word = words[i]
    following_word = words[i+1]
    if len(word) < 1:
        continue

    if is_start_word(word):
        start_words.append(word)

    if len(following_word) > 0:
        if word not in next_words:
            next_words[word] = []
        next_words[word].append(following_word)


# Construct 5 random sentences
def make_sentence():
    current_word = random.choice(start_words)
    started_quote = starts_quote(current_word)
    if ends_quote(current_word):
        current_word = current_word [-1]

    while not is_end_word(current_word) and current_word in next_words:
        print(current_word, end=" ")
        current_word = random.choice(next_words[current_word])

        if starts_quote(current_word):
            if started_quote:
                current_word = current_word[1:]
            else:
                started_quote = starts_quote(current_word)

        if ends_quote(current_word):
            current_word = current_word[:-1]
            if started_quote:
                current_word = current_word + started_quote
            started_quote = None

    print(current_word, end='')
    if started_quote:
        print(started_quote)


for i in range(5):
    make_sentence()
    print("\n")
