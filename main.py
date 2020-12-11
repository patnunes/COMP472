import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
import naive_bayes 
import vocabulary
from import_data_set import DataSet, Tweet, TweetWord

def main():

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
    print(testing_inputs)

    most_used_words = training_inputs.get_most_used_words()
    for elem in most_used_words:
        print(elem)

    training_inputs.implement_filtered_vocabulary()
    print(training_inputs)
    return training_inputs, testing_inputs

main()