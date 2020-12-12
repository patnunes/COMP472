""" imports data set and places it in DataSet class
"""
import math
import string


def main():
    """ imports data set
    """

    training_file = open("./a3-dataset/covid_training.tsv", "r", encoding="utf-8")
    testing_file = open("./a3-dataset/covid_test_public.tsv", "r", encoding="utf-8")

    next(training_file)  # skip first line
    next(testing_file)  # skip first line

    training_lines = training_file.readlines()
    testing_lines = testing_file.readlines()

    data = DataSet()

    for line in training_lines:
        col = line.split('\t')
        data.append_training_set(Tweet(col[0], col[1], col[2]))

    for line in testing_lines:
        col = line.split('\t')
        data.append_testing_set(TestingTweet(col[0], col[1], col[2]))

    print(data)

    data.calc_total_cond_probability()
    data.calc_testing_prob()
    # data.print_testing_set()

    t_p = 0
    f_p = 0
    t_n = 0
    f_n = 0
    file_1 = open("trace_NB-BOW-OV.txt", "w+")
    for document in data.testing_documents_list:
        if document.p_yes > document.p_no:
            correctness, t_p, f_p, t_n, f_n = determine_correctness(
                document.label, "yes", t_p, f_p, t_n, f_n)
            text = document.tweet_id + "  " + "yes" + "  " + \
                str(document.p_yes) + "  " + document.label + "  " + correctness + "\n"
            file_1.write(text)
        else:
            correctness, t_p, f_p, t_n, f_n = determine_correctness(
                document.label, "no", t_p, f_p, t_n, f_n)
            text = document.tweet_id + "  " + "no" + "  " + \
                str(document.p_no) + "  " + document.label + "  " + correctness + "\n"
            file_1.write(text)
    file_1.close()

    data.implement_filtered_vocabulary()
    data.calc_total_cond_probability()
    data.calc_testing_prob()
    # data.print_unique_words()

    file_3 = open("eval NB-BOW-OV.txt", "w+")
    file_3.write(calc_statistics(t_p, f_p, t_n, f_n))
    file_3.close()

    t_p = 0
    f_p = 0
    t_n = 0
    f_n = 0

    file_2 = open("trace_NB-BOW-FV.txt", "w+")
    for document in data.testing_documents_list:
        if document.p_yes > document.p_no:
            correctness, t_p, f_p, t_n, f_n = determine_correctness(
                document.label, "yes", t_p, f_p, t_n, f_n)
            text = document.tweet_id + "  " + "yes" + "  " + \
                str(document.p_yes) + "  " + document.label + "  " + correctness + "\n"
            file_2.write(text)
        else:
            correctness, t_p, f_p, t_n, f_n = determine_correctness(
                document.label, "no", t_p, f_p, t_n, f_n)
            text = document.tweet_id + "  " + "no" + "  " + \
                str(document.p_no) + "  " + document.label + "  " + correctness + "\n"
            file_2.write(text)
    file_2.close()

    file_4 = open("eval_NB-BOW-FV.txt", "w+")
    file_4.write(calc_statistics(t_p, f_p, t_n, f_n))
    file_4.close()

    print(data)


def determine_correctness(label, predicted_label, t_p, f_p, t_n, f_n):
    """ Returns whether prediction was right or not; updates all the variables t_p, f_p, t_n, f_n
    """
    if label == predicted_label and label == 'yes':
        t_p += 1
        return 'correct', t_p, f_p, t_n, f_n

    elif label == predicted_label and label == 'no':
        t_n += 1
        return 'correct', t_p, f_p, t_n, f_n

    elif label != predicted_label and label == 'yes':
        f_n += 1
        return 'wrong', t_p, f_p, t_n, f_n

    elif label != predicted_label and label == 'no':
        f_p += 1
        return 'wrong', t_p, f_p, t_n, f_n


def calc_statistics(t_p, f_p, t_n, f_n):
    """ Calculates statistics based on inputs t_p, f_p, t_n, f_n
    """
    accuracy = (t_p+t_n) / (t_p +
                            t_n+f_p+f_n)
    yes_p = (t_p) / (t_p+f_p)
    no_p = (t_n)/(t_n+f_n)
    yes_r = (t_p) / (t_p+f_n)
    no_r = (t_n)/(t_n+f_p)
    yes_f1 = 2*(yes_r*yes_p)/(yes_p+yes_r)
    no_f1 = 2*(no_r*no_p)/(no_p+no_r)

    print("{0}\n{1}  {2}\n{3}  {4}\n{5}  {6}".format(
        accuracy, yes_p, no_p, yes_r, no_r, yes_f1, no_f1))

    return "{0}\n{1}  {2}\n{3}  {4}\n{5}  {6}".format(accuracy, yes_p, no_p,
                                                      yes_r, no_r, yes_f1, no_f1)


class Tweet:
    """ The class holding a single tweet with its ID, text and label
    """

    def __init__(self, tweet_id, text, label):
        # used for all tweets
        self.tweet_id = tweet_id
        self.text = text
        self.label = label

    def __repr__(self):
        return f'Tweet ID: {self.tweet_id}, Text: {self.text}, Label: {self.label}'


class TestingTweet(Tweet):
    """ The class holding a Tweet/Document; so we need additional parameters
    """

    def __init__(self, tweet_id, text, label):
        super().__init__(tweet_id, text, label)
        self.word_array = []
        self.unseen_words = []  # denotes words in tweet that are not in the training set
        self.p_yes = 0
        self.p_no = 0

    def append_to_word_array(self, word):
        """ Apppends a word to word array
        """
        self.word_array.append(word)

    def calculate_probability(self, probability_yes, probability_no):
        """ Calculates the yes and no probability the testing Tweet/Document
        """
        combined_word_probability_yes = math.log(probability_yes, 10)
        combined_word_probability_no = math.log(probability_no, 10)
        for word in self.word_array:
            combined_word_probability_no += math.log(word.p_no, 10)
            combined_word_probability_yes += math.log(word.p_yes, 10)

        self.p_yes = combined_word_probability_yes
        self.p_no = combined_word_probability_no

    def __repr__(self):
        return (f'Tweet ID: {self.tweet_id}\t\tLabel: {self.label}\t\t'
                f'Word_array size: {len(self.word_array)}\t\tUnseen words: {len(self.unseen_words)}'
                f'\t\tP(yes): {self.p_yes}\t\tP(no): {self.p_no}\nTweet:{self.text}'
                f'\nUnseen words:{self.unseen_words}')


class TweetWord:
    """ The class containing unique word statistics
    """

    def __init__(self, tweet_origin, input_string):
        self.string = input_string  # actual word string
        self.usage = 0  # number of times used
        self.label_yes = 0  # number of times the word appears with a 'yes' label
        self.label_no = 0  # number of times the word appears with a 'no' label
        self.mentioned_tweets = set()  # set of tweet documents where word is mentioned
        self.add_count(tweet_origin)  # when first created, we want to add the details
        self.p_yes = 0  # probability given yes
        self.p_no = 0  # probability given no

    def add_count(self, tweet_origin):
        """ If the TweetWord is not unique, we want to use add_count to note more usage
        """
        self.mentioned_tweets.add(tweet_origin)
        self.usage += 1
        if tweet_origin.label == 'yes':
            self.label_yes = self.label_yes + 1
        else:
            self.label_no = self.label_no + 1

    def prob_word_given_class_yes(self, dataset_size, classifier_total, smoothing=0.01):
        """ Calculate Probability that the word is from Class Yes
        """
        self.p_yes = (self.label_yes+smoothing)/(classifier_total+dataset_size)

    def prob_word_given_class_no(self, dataset_size, classifier_total, smoothing=0.01):
        """ Calculate Probability that the word is from Class No
        """
        self.p_no = (self.label_no+smoothing)/(classifier_total+dataset_size)

    def __repr__(self):
        return (f'Word: {self.string}, y/n: {self.label_yes}/{self.label_no}, '
                f'Count: {self.usage}, Mentioned in: {len(self.mentioned_tweets)}')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.string == other.string
        else:
            return False

    def __hash__(self):
        return hash(self.string)

    def asdict(self):
        """ returns a dict of the object Tweet
        """
        return {'string': self.string, 'yes': self.label_yes, 'no': self.label_no}


class DataSet:
    """ The full data set object holding the tweets and the individual words
    """

    def __init__(self):
        self.training_documents_list = []  # individual tweets in training set
        self.testing_documents_list = []  # individual tweets in the testing set
        # training_set data variables
        self.total_words = 0  # total number of words
        self.unique_words = set()  # total number of unique words, a set
        self.unique_words_actual = set()  # total number of unique words, a set - a sanity check
        self.no_label_words = 0  # number of words labelled 'no'
        self.yes_label_words = 0  # number of words labelled 'yes'
        self.no_label_documents = 0  # number of documents/tweets labelled 'no'
        self.yes_label_documents = 0  # number of  documents/tweets labelled 'yes'
        self.filtered_vocabulary = False  # whether the data set filtered

    def append_training_set(self, input_tweet):
        """ Populate the data set by appending Tweet Objects to it from the training set
        """
        self.training_documents_list.append(input_tweet)
        # count yes/ no labels for documents
        if input_tweet.label == 'yes':
            self.yes_label_documents += 1
        else:
            self.no_label_documents += 1
        input_words = input_tweet.text.split(' ')
        for word in input_words:
            transformed_word = transform(word)
            if transformed_word:
                self.total_words += 1
                # count yes/ no labels for words
                if input_tweet.label == 'yes':
                    self.yes_label_words += 1
                else:
                    self.no_label_words += 1
                tweet_word = TweetWord(input_tweet, transformed_word)
                if tweet_word in self.unique_words:
                    for known_word in self.unique_words:
                        if known_word.string == tweet_word.string:
                            known_word.add_count(input_tweet)
                            break
                else:
                    self.unique_words.add(tweet_word)

                self.unique_words_actual.add(tweet_word.string)

    def append_testing_set(self, input_tweet):
        """ Populate the data set by appending Tweet Objects to it from the testing set
        """
        self.testing_documents_list.append(input_tweet)
        input_words = input_tweet.text.split(' ')
        for word in input_words:
            transformed_word = transform(word)
            transformed_word_unique = True
            for known_word in self.unique_words:
                if known_word.string == transformed_word:
                    input_tweet.append_to_word_array(known_word)
                    transformed_word_unique = False
            if transformed_word_unique:
                input_tweet.unseen_words.append(transformed_word)

    def get_unique_words_count(self):
        """ returns total numbers of unique words (ie vocabulary)
        """
        return len(self.unique_words)

    def get_total_words(self):
        """ returns total words
        """
        return len(self.total_words)

    def get_unique_words(self):
        """ returns unique words set (for some reason?)
        """
        return self.unique_words

    def print_unique_words(self):
        """ Print List of Unique Words to a text file
        """
        file = open("WORDS.txt", "w+")
        for word in self.unique_words:
            file.write(f'{word.string}, p_yes: {word.p_yes}, p_no: {word.p_no}\n')

        file.close()

    def get_most_used_words(self):
        """ gets the 20 most used words
        """
        word_list = []
        for known_word in self.unique_words:
            word_list.append(known_word)
        word_list = sorted(word_list, key=lambda word: word.usage, reverse=True)
        return word_list[:20]

    def __repr__(self):
        return (f'Training Set Statistics: '
                f'Unique words: {len(self.unique_words)}({len(self.unique_words_actual)}), '
                f'Total words: {self.total_words}, '
                f'Total Documents: {len(self.training_documents_list)}, '
                f'Yes words: {self.yes_label_words}, No words: {self.no_label_words}, '
                f'Yes docs: {self.yes_label_documents}, No docs: {self.no_label_documents} '
                f'FV: {str(self.filtered_vocabulary)}\n'
                f'Testing Set Statistics: Total Documents: {len(self.testing_documents_list)}')

    def calc_total_cond_probability(self):
        """ Calculate Probability of every (unique) word in the (training) data set
        """
        for known_word in self.unique_words:
            known_word.prob_word_given_class_yes(self.yes_label_words, len(self.unique_words))
            known_word.prob_word_given_class_no(self.no_label_words, len(self.unique_words))

    def calc_testing_prob(self):
        """ Calculate Probability of every document in the testing data set
        """
        for document in self.testing_documents_list:
            probability_yes = self.yes_label_documents/len(self.training_documents_list)
            probability_no = self.no_label_documents/len(self.training_documents_list)
            document.calculate_probability(probability_yes, probability_no)

    def implement_filtered_vocabulary(self):
        """ Alters entire DataSet Object:
         deletes all words that occur less than 2 times; cannot be undone
        """
        new_set = set()  # cannot change the size of a set we're iterating through
        if not self.filtered_vocabulary:
            self.filtered_vocabulary = True
            for known_word in self.unique_words:
                if known_word.usage < 2:
                    self.total_words = self.total_words - known_word.usage
                    self.no_label_words = self.no_label_words - known_word.label_no
                    self.yes_label_words = self.yes_label_words - known_word.label_yes
                    self.unique_words_actual.remove(known_word.string)
                else:
                    new_set.add(known_word)
        self.unique_words = new_set

    def print_testing_set(self):
        """ Prints testing set tweets/documents
        """
        print('============ Outputing entirety of testing set ============')
        for testing_document in self.testing_documents_list:
            print(testing_document)
        print('============               Done                ============')


def transform(word):
    """ Transforms a word to the wanted format
    """
    table = str.maketrans('', '', string.punctuation)
    stripped = word.translate(table)
    return stripped.lower()


if __name__ == '__main__':
    main()
