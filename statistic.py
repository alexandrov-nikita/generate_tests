import re
import os
import json
from collections import Counter

alphabet = re.compile('[a-zA-Z0-9-]+|[,./?\:;=@%^&*()]+')
PEOPLE = ["Mr", "Mrs", "Ms", "Dr", "DR", "MR", "MS", "MRS"]
SHORT_WORDS = ["i", "e", "a", "m", "g", "p"]
SIGNAL_WORD = "~~~"
SENTENCE_ENDS = ['.', '?', '!']


def increase_frequency(triple, pair_counter, triple_counter):
    if (triple[0], triple[1]) not in pair_counter:
        pair_counter[(triple[0], triple[1])] = 0
    if triple not in triple_counter:
        triple_counter[triple] = 0
    pair_counter[(triple[0], triple[1])] += 1
    triple_counter[triple] += 1


def get_words(file_name):
    words = []
    text = open(file_name)
    for line in text:
        for word in alphabet.findall(line):
            words.append(word)
    return words


def make_shift(triple, pair_counter, triple_counter):
    increase_frequency(tuple(triple), pair_counter, triple_counter)
    if (triple[2] in SENTENCE_ENDS and triple[1] not in PEOPLE + SHORT_WORDS):
        increase_frequency((triple[1], triple[2], SIGNAL_WORD), pair_counter, triple_counter)
        increase_frequency((triple[2], SIGNAL_WORD, SIGNAL_WORD), pair_counter, triple_counter)
        triple[0], triple[1] = SIGNAL_WORD, SIGNAL_WORD
    else:
        triple[0], triple[1] = triple[1], triple[2]


def get_statistic_from_file(words, pair_counter, triple_counter):
    frt_word, snd_word = SIGNAL_WORD, SIGNAL_WORD
    for trd_word in words:
        triple = [frt_word, snd_word, trd_word]
        make_shift(triple, pair_counter, triple_counter)
        frt_word, snd_word, trd_word = triple[0], triple[1], triple[2]


def count_statistics_for_file(file_name, pair_counter, triple_counter):
    words = get_words(file_name)
    get_statistic_from_file(words, pair_counter, triple_counter)


def write_in_json(output_file, pair_counter, triple_counter):
    trd_words = {}
    for triple, total_number in triple_counter.iteritems():
        if (triple[0], triple[1]) not in trd_words:
            trd_words[(triple[0], triple[1])] = []
        frequency = float(total_number) / pair_counter[(triple[0], triple[1])]
        trd_words[(triple[0], triple[1])].append((triple[2], frequency))
    with open(output_file, 'w') as stat:
        json.dump([(words[0], words[1], trd_word) for words, trd_word in trd_words.iteritems()], stat)


def calculate_statistics(path, output_file):
    pair_counter, triple_counter = {}, {}
    for file_name in os.listdir(path):
        count_statistics_for_file(path + str(file_name), pair_counter, triple_counter)
    write_in_json(output_file, pair_counter, triple_counter)


calculate_statistics("corpus/", "stat.json")