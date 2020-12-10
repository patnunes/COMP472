import numpy as np
from pandas import read_csv


def import_data_set():
    training_file = open("./a3-dataset/covid_training.tsv", "r", encoding="utf-8")
    testing_file = open("./a3-dataset/covid_test_public.tsv", "r", encoding="utf-8")

    next(training_file)  # skip first line
    next(testing_file)  # skip first line

    training_lines = training_file.readlines()
    testing_lines = testing_file.readlines()

    training_inputs = DataSet()
    testing_inputs = DataSet()

    for line in training_lines:
        col = line.split('\t')
        training_inputs.append_set(Tweet(col[0], col[1], col[2]))

    for line in testing_lines:
        col = line.split('\t')
        testing_inputs.append_set(Tweet(col[0], col[1], col[2]))

    print(training_inputs)
    print(training_inputs.get_most_used_words())
    # print(testing_inputs)


class Tweet:
    def __init__(self, tweet_id, text, label):
        self.tweet_id = tweet_id
        self.text = text
        self.label = label

    def __repr__(self):
        return f'Tweet ID: {self.tweet_id}, Text: {self.text}, Label: {self.label}'


class TweetWord:
    def __init__(self, tweet_origin, string):
        self.string = string
        self.usage = 0
        self.label_yes = 0
        self.label_no = 0
        self.mentioned_tweets = []
        self.set_label(tweet_origin)

    def set_label(self, tweet_origin):
        self.mentioned_tweets.append(tweet_origin)
        self.usage += 1
        if tweet_origin.label == 'yes':
            self.label_yes = self.label_yes + 1
        else:
            self.label_no = self.label_no + 1

    def __repr__(self):
        return f'Word: {self.string}, y/n: {self.label_yes}/{self.label_no}, Count: {self.usage}, Mentioned in: {len(self.mentioned_tweets)}\n'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.string == other.string
        else:
            return False

    def __hash__(self):
        return hash(self.string)

    def asdict(self):
        return {'string': self.string, 'usage': self.usage, 'yes': self.label_yes, 'no': self.label_no}


class DataSet:
    def __init__(self):
        self.full_input = []
        self.total_words = 0
        self.unique_words = set()
        self.unique_words_actual = set()
        self.no_label = []
        self.yes_label = []

    def append_set(self, input_tweet):
        self.full_input.append(input_tweet)
        input_words = input_tweet.text.split(' ')
        for word in input_words:
            transformed_word = transform(word)
            if transformed_word:
                self.total_words += 1
                tweet_word = TweetWord(input_tweet, transformed_word)
                if tweet_word in self.unique_words:
                    for known_word in self.unique_words:
                        if known_word.string == tweet_word.string:
                            known_word.set_label(input_tweet)
                            break
                else:
                    self.unique_words.add(tweet_word)

                self.unique_words_actual.add(tweet_word.string)

    def get_unique_words_count(self):
        return len(self.unique_words)

    def get_total_words(self):
        return len(self.total_words)

    def get_unique_words(self):
        return self.unique_words

    def get_most_used_words(self):
        word_list = []
        for known_word in self.unique_words:
            word_list.append(known_word)
        word_list = sorted(word_list, key=lambda word: word.usage, reverse=True)
        return word_list[:20]

    def __repr__(self):
        return f'Unique words: {len(self.unique_words)} ({len(self.unique_words_actual)}), Total words: {self.total_words}, Total entries: {len(self.full_input)}'


def transform(word):
    """ Transforms a word to the wanted format
    """
    return word.lower()


import_data_set()
