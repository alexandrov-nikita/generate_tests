import re
import os
import json
import numpy
from random import uniform
import random

AFTER_APOSTROPHE = ["ll", "t", "s", "ve", "m", "d", "re"]
PUNCTUATION = ['.', '?', '!', ':', ',', ';', '@', '%', '/', '(', ')']
SIGNAL_WORD = "~~~"
               
               
def get_sentence(stat):
    first_word = SIGNAL_WORD
    second_word = SIGNAL_WORD
    counter_words = 0
    third_word = ""
    str = ""
    while third_word != SIGNAL_WORD:
        possible_words = stat[first_word, second_word]
        partial_sum = 0.0
        stop_sum = uniform(0.0, 1.0)
        for next_word in possible_words:
            partial_sum += next_word[1]
            if partial_sum >= stop_sum:
                third_word = next_word[0]
                break
        if third_word == SIGNAL_WORD:
            break
        
        first_word, second_word = second_word, third_word
        if first_word == SIGNAL_WORD or third_word in AFTER_APOSTROPHE + PUNCTUATION:
            if third_word in AFTER_APOSTROPHE:
                str += '\''
            str += third_word
        else:
            str += " " + third_word
    return str
        

def create_map(list_of_pairs):
    pairs = {}
    for pair_words in list_of_pairs:
        pairs[(pair_words[0], pair_words[1])] = pair_words[2]
    return pairs


def generation(pairs):
    number_of_sentences = random.randint(3000, 5000)
    current_in_title = 0
    number_of_sentences_in_title = random.randint(1, 20)
    text = " "
    for sentence in range(number_of_sentences):
        text += get_sentence(pairs) + " "
        current_in_title += 1
        if current_in_title > number_of_sentences_in_title:
            text += '\n\n\n '
            current_in_title = 0
            number_of_sentences_in_title = random.randint(1, 20)
    return text

with open("stat.json", 'r') as stat:
        list_of_pairs = json.load(stat)
pairs = create_map(list_of_pairs)

f = open("gen.txt", 'w')
text = generation(pairs)
f.write(text)

