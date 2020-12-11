import csv
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer



def prob_class(data, classifier_word):
            
    total_tweets = len(data)
    total_occurrences = data['q1_label'].str.contains(classifier_word).sum()
    P_value = total_occurrences / total_tweets
    print (P_value)
    return P_value

def prob_word_given_class(matrix, word, classifier_word, smoothing = 0.01):

    output = matrix.loc[matrix['q1_label'] == classifier_word, word].sum()
    print (output)
    return output
        
        