import csv
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer

def main():

    tsv_file = './a3-dataset/covid_training.tsv'
    
    data=pd.read_csv(tsv_file, sep='\t')

    token = RegexpTokenizer(r'[a-zA-Z0-9]+')
    cv = CountVectorizer(lowercase=True,stop_words=None,ngram_range = (1,1),tokenizer = token.tokenize)
    text_counts= cv.fit_transform(data['text'])
    
    vocabulary = pd.DataFrame(text_counts.toarray(),columns=cv.get_feature_names())
    q1_label = data['q1_label']
    matrix = vocabulary.join(q1_label)
    #print(matrix.head(10))

    
    #used to calculate probability of classifier, i.e. c1 = yes, c2 = no
    calc_P(data, classifier_word='no')
    
    #total # of times the word appears in a negative case
    calc_P_of_word_class(matrix, word='zombie',classifier_word='no')
    
def calc_P(data, classifier_word):
    
    total_documents = len(data)
    classifier_word = classifier_word
    total_occurances = data['q1_label'].str.contains(classifier_word).sum()
    P_value = total_occurances / total_documents
    return P_value

def calc_P_of_word_class(matrix, word, classifier_word):
    
    #total # of times the word appears in a negative case
    output = matrix.loc[matrix['q1_label'] == classifier_word, word].sum()
    return output
    
    
main()