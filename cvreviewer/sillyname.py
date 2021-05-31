import random

with open('cvreviewer/sillyname.txt') as f:
    words = [line.rstrip('\n') for line in f]

upper_words = [word for word in words if word[0].isupper()]
name_words = [word for word in upper_words if not word.isupper()]


def rand_silly_name():
    name = ' '.join([name_words[random.randint(0, len(name_words))] for i in range(2)])
    return name
