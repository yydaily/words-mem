import sys
import os
import yaml
import random
from time import sleep

words_file = __file__[:-9] + '/need_to_memory'

def print_usage():
    print('''word [command] [args]
command:
    none:   print usage, then print an random word without meanings, and sleep 3 second, if you remembered, mark it!
    int:    print a list with x random word which contains meanings
    add:    add one word you don't know, follow with at least 3 args, if there are more then one part of speech, add as much as you want
        1. word itself
        2. part of speech
        3. meanings
''')

def choose_random_word(cnt):
    if not os.path.exists(words_file):
        print_usage()
        print('no word in your need_to_memory list, try to add some')
        exit(0)
    word_dict = yaml.safe_load(open(words_file, 'r'))
    words = []
    for k in word_dict:
        words.append(k)
    random.shuffle(words)
    if len(words) >= cnt:
        words = words[:cnt]
    else:
        print('not enough words, display all')
    return words, word_dict

def add(args):
    if len(args) % 2 != 1 and len(args) < 3:
        print_usage()
        return

    if not os.path.exists(words_file):
        open(words_file, 'w').close()
    d = {}
    for i in range(1, len(args), 2):
        d[args[i]] = args[i+1]
    data = { args[0]: d}
    open(words_file, 'a').write(yaml.dump(data))


def show(cnt):
    words, d = choose_random_word(cnt)
    if cnt != 1:
        for word in words:
            print(word, ':')
            for k in d[word]:
                print('\t', k, '\t', d[word][k])
            print("==============================")
        return
    if random.random()>0.5:
        print(words[0])
        input()
        for k in d[words[0]]:
            print(k, '\t', d[words[0]][k])
    else:
        for k in d[words[0]]:
            print(k, '\t', d[words[0]][k])
        input()
        print(words[0])

if __name__ == '__main__':
    args = sys.argv[2:]
    if len(args) == 0: # only command
        show(1)
    else:
        if args[0] == 'add':
            add(args[1:])
        else:
            cnt = int(args[0])
            show(cnt)
