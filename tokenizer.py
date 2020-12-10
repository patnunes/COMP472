
import numpy as np
from pandas import read_csv


def import_data_set():
    training_file = open("./a3-dataset/covid_training.tsv", "r")
    testing_file = open("./a3-dataset/covid_test_public.tsv", "r")

    training_lines = training_file.readlines()
    testing_lines = testing_file.readlines()

    training_inputs = DataSet()
    testing_inputs = DataSet()

    for line in training_lines:
        col = line.split('\t')
        training_inputs.append_set(InputFile(col[0], col[1], col[2]))

    for line in testing_lines:
        col = line.split('\t')
        testing_inputs.append_set(InputFile(col[0], col[1], col[2]))

    print(training_inputs)
    print(testing_inputs)


class InputFile:
    def __init__(self, tweet_id, text, query_1):
        self.tweet_id = tweet_id
        self.text = text
        self.query_1 = query_1

    def __repr__(self):
        return f'Tweet ID: {self.tweet_id}, Text: {self.text}, Query_1: {self.query_1}'


class DataSet:
    def __init__(self):
        self.full_input = []
        self.total_words = []
        self.unique_words = set()

    def append_set(self, input_string):
        self.full_input.append(input_string)
        input_words = input_string.text.split(' ')
        for word in input_words:
            self.unique_words.add(word)
            self.total_words.append(word)

    def get_unique_words(self):
        return len(self.unique_words)

    def get_total_words(self):
        return len(self.total_words)

    def __repr__(self):
        return f'Unique words: {len(self.unique_words)}, Total words: {len(self.total_words)}'


import_data_set()
