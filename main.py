import csv
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
import naive_bayes 
import vocabulary

def main():

    tsv_file = './a3-dataset/covid_training.tsv'
    
    OV_vocab = vocabulary.Vocabulary(tsv_file)
    print (OV_vocab.get_vocabulary_size())
    #used to calculate probability of classifier, i.e. c1 = yes, c2 = no
    naive_bayes.prob_class(OV_vocab.data, classifier_word='no')
    
    #total # of times the word appears in a negative case
    naive_bayes.prob_word_given_class(OV_vocab.matrix, word='zombie',classifier_word='no')
    
    OV_vocab.get_total_words_class('no')

main()