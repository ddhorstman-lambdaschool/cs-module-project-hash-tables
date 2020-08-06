import re


def word_count(s):
    blacklist = re.compile(r'[":;,\.\-\+\=/\\\|\[\]\{\}\(\)\*\^&]')
    words = blacklist.sub("", s).lower()
    words = re.sub('\s+', ' ', words).split(' ')
    word_count = {}
    for word in words:
        if word == '':
            continue
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count


if __name__ == "__main__":
    print(word_count(""))
    print(word_count("Hello"))
    print(word_count('Hello, my cat. And my cat doesn\'t say "hello" back.'))
    print(word_count('":;,.-+=/\\|[]{}()*^&'))
    print(word_count(
        'This is a test of the emergency broadcast network. This is only a test.'))
