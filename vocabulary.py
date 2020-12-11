import csv
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
import numpy as np

class Vocabulary:
    def __init__(self, tsv_file):

        token = RegexpTokenizer(r'[a-zA-Z0-9]+')
        
        self.data=pd.read_csv(tsv_file, sep='\t')
        self.cv = CountVectorizer(lowercase=True,stop_words=None,ngram_range = (1,1),tokenizer = token.tokenize)
        self.text_counts= self.cv.fit_transform(self.data['text'])
        
        self.vocabulary = pd.DataFrame(self.text_counts.toarray(),columns=self.cv.get_feature_names())
        print(self.vocabulary)
        self.q1_label = self.data['q1_label']
        self.matrix = self.vocabulary.join(self.q1_label)

    def get_vocabulary_size(self):
        return self.vocabulary.shape[1]

    def get_total_words_class(self,classifier_word):
        is_classifier = self.matrix['q1_label'] == classifier_word
        matrix_classifier = self.matrix[is_classifier]
        print (matrix_classifier.shape[0])
        print (matrix_classifier.sum(numeric_only=True).sum())