""" import a training and testing tsv files of Tweets and try to label the testing set based on
    the training set with the Naive-Bayes Bag of Words Classifier
"""
import math
import string

TOKENIZING_MODE = 0  # determines tokenizing; 0 = lower case; 1 = lower case + ignore punctuation
USAGE_LIMIT = 2  # removes words with less than USAGE_LIMIT when implementing filtered vocab
SMOOTHING = 0.01  # smoothing value


def main():
    """ imports data set and runs the NB BOW Classifier on it
    """

    training_file = open("./a3-dataset/covid_training.tsv", "r", encoding="utf-8")
    testing_file = open("./a3-dataset/covid_test_public.tsv", "r", encoding="utf-8")

    next(training_file)  # skip first line, as it is a header in the training file

    training_lines = training_file.readlines()
    testing_lines = testing_file.readlines()

    data = DataSet()

    for line in training_lines:
        col = line.split('\t')
        data.append_training_set(Tweet(col[0], col[1], col[2]))  # must append training set first

    for line in testing_lines:
        col = line.split('\t')
        data.append_testing_set(TestingTweet(col[0], col[1], col[2]))

    print(data)  # print statistics of the dataset; non-filtered

    data.calc_total_cond_probability()
    data.calc_testing_prob()

    data.print_unique_words("words_OV")

    write_trace_and_eval_files('NB-BOW-OV', data)  # write trace and eval files of OV

    data.implement_filtered_vocabulary()  # removes words with less usage than USAGE_LIMIT

    print(data)  # print statistics of the filtered vocabulary dataset
    data.calc_total_cond_probability()
    data.calc_testing_prob()

    data.print_unique_words("words_FV")

    write_trace_and_eval_files('NB-BOW-FV', data)  # write trace and eval files of FV


def write_trace_and_eval_files(file_name, data):
    """ Writes Trace and Eval Files
        1. goes through DataSet's "data" testing_documents_list
        2. find the higher probability between yes/no classes
        3. if p_yes is larger; our predicted label is "yes", we compare this with the actual
        label to determine the correctness ("correct" or "wrong") and mark it as a true positive
        or false positive accordingly
        4. repeat same for "no" label
        5. uses statistics to write eval files
    """
    # statistics
    t_p = 0  # true positive
    f_p = 0  # false positive
    t_n = 0  # true negative
    f_n = 0  # false negative

    file_trace = open(f"trace_{file_name}.txt", "w+")
    for document in data.testing_documents_list:
        if document.p_yes > document.p_no:
            correctness, t_p, f_p, t_n, f_n = determine_correctness(
                document.label, "yes", t_p, f_p, t_n, f_n)
            text = document.tweet_id + "  " + "yes" + "  " + \
                str(document.p_yes) + "  " + document.label + "  " + correctness + "\n"
            file_trace.write(text)
        else:
            correctness, t_p, f_p, t_n, f_n = determine_correctness(
                document.label, "no", t_p, f_p, t_n, f_n)
            text = document.tweet_id + "  " + "no" + "  " + \
                str(document.p_no) + "  " + document.label + "  " + correctness + "\n"
            file_trace.write(text)
    file_trace.close()

    file_eval = open(f"eval_{file_name}.txt", "w+")
    file_eval.write(calc_statistics(t_p, f_p, t_n, f_n))
    file_eval.close()


def determine_correctness(label, predicted_label, t_p, f_p, t_n, f_n):
    """ Returns whether prediction was right or not; updates all the variables t_p, f_p, t_n, f_n
    """
    if label == predicted_label and label == 'yes':
        t_p += 1
        return 'correct', t_p, f_p, t_n, f_n

    if label == predicted_label and label == 'no':
        t_n += 1
        return 'correct', t_p, f_p, t_n, f_n

    if label != predicted_label and label == 'yes':
        f_n += 1
        return 'wrong', t_p, f_p, t_n, f_n

    if label != predicted_label and label == 'no':
        f_p += 1
        return 'wrong', t_p, f_p, t_n, f_n


def calc_statistics(t_p, f_p, t_n, f_n):
    """ Calculates statistics based on inputs t_p, f_p, t_n, f_n
    """
    accuracy = round((t_p+t_n) / (t_p + t_n + f_p + f_n), 4)
    yes_p = round((t_p) / (t_p+f_p), 4)
    no_p = round((t_n)/(t_n+f_n), 4)
    yes_r = round((t_p) / (t_p+f_n), 4)
    no_r = round((t_n)/(t_n+f_p), 4)
    yes_f1 = round(2*(yes_r*yes_p)/(yes_p+yes_r), 4)
    no_f1 = round(2*(no_r*no_p)/(no_p+no_r), 4)
    print('Evaluation Peformance:')
    print("{0}\n{1}  {2}\n{3}  {4}\n{5}  {6}".format(
        accuracy, yes_p, no_p, yes_r, no_r, yes_f1, no_f1))
    print()

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
    """ The class holding a Tweet/Document for the Testing set; so we need additional parameters
    """

    def __init__(self, tweet_id, text, label):
        super().__init__(tweet_id, text, label)
        self.word_array = []
        self.unseen_words = []  # denotes words in tweet that are not in the training set
        self.p_yes = 0
        self.p_no = 0

    def calculate_probability(self, probability_yes, probability_no):
        """ Calculates the yes and no probability the testing Tweet/Document
        """
        # priors
        combined_word_probability_yes = math.log(probability_yes, 10)
        combined_word_probability_no = math.log(probability_no, 10)

        for word in self.word_array:
            # this check is needed for filtered vocabulary;
            # which sets the prob of filtered words to "filtered"
            if isinstance(word.p_yes, float) and isinstance(word.p_no, float):
                combined_word_probability_yes += math.log(word.p_yes, 10)
                combined_word_probability_no += math.log(word.p_no, 10)

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
        self.p_yes = 0  # probability given yes; calculated later with prob_word_given_class_yes
        self.p_no = 0  # probability given no; calculated later with prob_word_given_class_no

    def add_count(self, tweet_origin):
        """ If the TweetWord is not unique, we want to use add_count to note more usage
        """
        self.mentioned_tweets.add(tweet_origin)
        self.usage += 1
        if tweet_origin.label == 'yes':
            self.label_yes = self.label_yes + 1
        else:
            self.label_no = self.label_no + 1

    def prob_word_given_class_yes(self, classifier_total, dataset_size, smoothing=SMOOTHING):
        """ Calculate Probability that the word is from Class Yes
        """
        self.p_yes = (self.label_yes+smoothing)/(classifier_total+dataset_size*smoothing)

    def prob_word_given_class_no(self, classifier_total, dataset_size, smoothing=SMOOTHING):
        """ Calculate Probability that the word is from Class No
        """
        self.p_no = (self.label_no+smoothing)/(classifier_total+dataset_size*smoothing)

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
            transformed_word_new = True
            for known_word in self.unique_words:
                if known_word.string == transformed_word:
                    input_tweet.word_array.append(known_word)
                    transformed_word_new = False
            if transformed_word_new:
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
        """ returns unique words set
        """
        return self.unique_words

    def print_unique_words(self, document_name):
        """ Print List of Unique Words to a text file
        """
        file = open(f"{document_name}.txt", "w+", encoding="utf-8")
        for word in self.unique_words:
            file.write(
                f'{word.string}, p_yes: {word.p_yes}, p_no: {word.p_no}, '
                f'c_yes: {word.label_yes}, c_no: {word.label_no}\n')

        file.close()

    def __repr__(self):
        return (f'Dataset Statistics:: Filtered Vocabulary: {str(self.filtered_vocabulary)}\n'
                f'Training Set Statistics:\n'
                f'Unique words: {len(self.unique_words)}({len(self.unique_words_actual)}), '
                f'Total words: {self.total_words}\n'
                f'Yes words: {self.yes_label_words}, No words: {self.no_label_words}\n'
                f'Total Tweets: {len(self.training_documents_list)}, '
                f'Yes Tweets: {self.yes_label_documents}, No Tweets: {self.no_label_documents}\n'
                f'Testing Set Statistics: Total Tweets: {len(self.testing_documents_list)}')

    def calc_total_cond_probability(self):
        """ Calculate Probability of every (unique) word in the (training) data set
        """
        for known_word in self.unique_words:
            known_word.prob_word_given_class_yes(self.yes_label_words, len(self.unique_words))
            known_word.prob_word_given_class_no(self.no_label_words, len(self.unique_words))

    def calc_testing_prob(self):
        """ Calculate Probability of every document in the testing data set
        """
        probability_yes = self.yes_label_documents/len(self.training_documents_list)
        probability_no = self.no_label_documents/len(self.training_documents_list)
        for document in self.testing_documents_list:
            document.calculate_probability(probability_yes, probability_no)

    def implement_filtered_vocabulary(self):
        """ Alters entire DataSet Object:
            deletes all words that occur less than 2 times; cannot be undone
        """
        new_set = set()  # cannot change the size of a set we're iterating through
        if not self.filtered_vocabulary:
            self.filtered_vocabulary = True
            for known_word in self.unique_words:
                if known_word.usage < USAGE_LIMIT:
                    self.total_words = self.total_words - known_word.usage
                    self.no_label_words = self.no_label_words - known_word.label_no
                    self.yes_label_words = self.yes_label_words - known_word.label_yes
                    self.unique_words_actual.remove(known_word.string)
                    # the word's probabilities must be reset to avoid interfering with FV stats
                    known_word.p_yes = "filtered"
                    known_word.p_no = "filtered"
                else:
                    new_set.add(known_word)
        self.unique_words = new_set

    def confirm_count(self):
        """ Confirms the yes_label_words and no_label_words parameters
            A sanity check method
        """
        count_yes = 0
        count_no = 0
        for known_word in self.unique_words:
            count_yes += known_word.label_yes
            count_no += known_word.label_no
        assert count_yes == self.yes_label_words
        assert count_no == self.no_label_words


def transform(word):
    """ Transforms a word to the wanted format. If TOKENIZING_MODE is 1; we ignore punctuation too
        Otherwise, it's simply a lower-case transformation
    """
    if TOKENIZING_MODE > 0:
        table = str.maketrans('', '', string.punctuation)
        stripped = word.translate(table)
        return stripped.lower()
    return word.lower()


if __name__ == '__main__':
    main()
