#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 09:00:41 2018

@author: jf
"""

import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier
from nltk.classify import MaxentClassifier
from random import shuffle
#from nltk.metrics import scores
import nltk.metrics
#import collections
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import math

class Classifier:
    
    def __init__(self):
        self.path = "/home/jf/Documentos/phd/thesis/intership/dev/tourist text mining/datasets/colombia_en/3 reviews/hotel/"
        self.positive_filename = "hotelOnlyPositiveReviews.txt"
        self.negative_filename = "hotelOnlyNegativeReviews.txt"
        self.percent_split = 0.75
    
    def get_sentences(self, filename):
        with open(filename, 'r') as in_file:
            text = in_file.read()
            return nltk.sent_tokenize(text)
        
    def split_sentences(self, sentences):
        train = sentences[: int(len(sentences) * self.percent_split)]
        test = sentences[int(len(sentences) * self.percent_split) :]
        return train, test
    
    def get_words(self, sentences):
        words = []
        for sentence in [word_tokenize(i) for i in sentences]:
            for word in sentence:
                words.append(word)
        return words
    
    def create_word_features(self, words):
        useful_words = [word for word in words if word not in stopwords.words("english")]
        my_dict = dict([(word, True) for word in useful_words])
        return my_dict
    
    def get_train_test(self):
        self.positive_sentences = self.get_sentences(self.path + self.positive_filename)
        self.negative_sentences = self.get_sentences(self.path + self.negative_filename)
        
        shuffle(self.positive_sentences)
        shuffle(self.negative_sentences)
        
        self.positive_train, self.positive_test = self.split_sentences(self.positive_sentences)
        self.negative_train, self.negative_test = self.split_sentences(self.negative_sentences)
        
        positive_train_words = self.get_words(self.positive_train)
        positive_test_words = self.get_words(self.positive_test)
        negative_train_words = self.get_words(self.negative_train)
        negative_test_words = self.get_words(self.negative_test)
        
        positive_train_features = []
        positive_train_features.append((self.create_word_features(positive_train_words), "positive"))
        positive_test_features = []
        positive_test_features.append((self.create_word_features(positive_test_words), "positive"))
        negative_train_features = []
        negative_train_features.append((self.create_word_features(negative_train_words), "negative"))
        negative_test_features = []
        negative_test_features.append((self.create_word_features(negative_test_words), "negative"))
        
        self.training_set = positive_train_features + negative_train_features
        self.testing_set = positive_test_features + negative_test_features

    def wordcloud_draw(self, data, color = 'black'):
        words = ' '.join(data)
        cleaned_word = " ".join([word for word in words.split()
                                if 'http' not in word
                                    and not word.startswith('@')
                                    and not word.startswith('#')
                                    and word != 'RT'
                                ])
        wordcloud = WordCloud(stopwords = STOPWORDS,
                          background_color = color,
                          width = 3840,
                          height = 2160
                         ).generate(cleaned_word)
        plt.figure(1, figsize = (20, 20))
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()
        
    def nb_classifier(self):
        self.classifier = NaiveBayesClassifier.train(self.training_set)
        
    def megam_classifier(self, filename):
        nltk.config_megam(filename)
        self.classifier = MaxentClassifier.train(self.training_set, "megam")
        
    def predict(self, review):
        words = word_tokenize(review)
        words = self.create_word_features(words)
        return self.classifier.classify(words)
    
    def stats(self):
        TP = 0
        FP = 0
        FN = 0
        TN = 0
        
        for sentence in self.positive_test:
            if (self.predict(sentence) == 'positive'):
                TP += 1
            else:
                FN += 1
        
        for sentence in self.negative_test:
            if (self.predict(sentence) == 'positive'):
                FP += 1
            else:
                TN += 1  
        
        print("                               +-------------------------+")
        print("                               |      Actual class       |")           
        print("                               +------------+------------+")
        print("                               |  positive  |  negative  |")
        print("+-----------------+------------+------------+------------+")
        print("|                 |  positive  | %10d | %10d |" % (TP, FP))
        print("| predicted class +------------+------------+------------+")
        print("|                 |  negative  | %10d | %10d |" % (FN, TN))
        print("+-----------------+------------+------------+------------+")
        print("\n\n");

        print("                               +-------------------------+")
        print("                               |      Actual class       |")           
        print("                               +------------+------------+")
        print("                               |  positive  |  negative  |")
        print("+-----------------+------------+------------+------------+")
        print("|                 |  positive  | %10.5f | %10.5f |" % (TP / (TP + FN), FP / (FP + TN)))
        print("| predicted class +------------+------------+------------+")
        print("|                 |  negative  | %10.5f | %10.5f |" % (FN / (TP + FN), TN / (FP + TN)))
        print("+-----------------+------------+------------+------------+")
        print("\n\n");
        
        accuracy = (TP + TN) / (TP + TN + FP + FN)
        TPR = TP / (TP + FN)
        TNR = TN / (TN + FP)
        PPV = TP / (TP + FP)
        NPV = TN / (TN + FN)
        FNR = FN / (FN + TN)
        FPR = FP / (FP + TN)
        FDR = FP / (FP + TP)
        FOR = FN / (FN + TN)
        F1_score = 2 * TP / (2 * TP + FP + FN)
        MCC = (TP * TN - FP * FN) / math.sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))
        BM = TPR + TNR - 1
        MK = PPV + NPV - 1
        
        print("accuracy (ACC)                                           : ", accuracy)
        print("sensitivity, recall, hit rate or True Positive Rate (TPR): ", TPR)
        print("specificy, selectivity or True Negative Rate (TNR)       : ", TNR)
        print("precision or Positive Predictive Value (PPV)             : ", PPV)
        print("Negative Predictive Value (NPV)                          : ", NPV)
        print("Miss rate or False Negative Rate (FNR)                   : ", FNR)
        print("Fall-out or False Positive Rate (FPR)                    : ", FPR)
        print("Fall Discovery Rate (FDR)                                : ", FDR)
        print("False Omission Rate (FOR)                                : ", FOR)
        print("F1 Score                                                 : ", F1_score)
        print("Matthews correlation coefficient (MCC)                   : ", MCC)
        print("Informedness or Bookmaker Informedness (BM)              : ", BM)
        print("Markedness (MK)                                          : ", MK)

        #self.classifier.show_most_informative_features(100)

        self.wordcloud_draw(self.positive_sentences, 'white')
        self.wordcloud_draw(self.negative_sentences)
        
#        accuracy = nltk.classify.util.accuracy(self.classifier, self.testing_set)
#        print('accuracy: ', accuracy)

        
#        refsets = collections.defaultdict(set)
#        testsets = collections.defaultdict(set)

#        for i, (feats, label) in enumerate(self.testing_set):
#            refsets[label].add(i)
#            observed = self.classifier.classify(feats)
#            testsets[observed].add(i)
    
#        print('positive precision:', scores.precision(refsets['positive'], testsets['positive']))
#        print('positive recall:', scores.recall(refsets['positive'], testsets['positive']))
#        print('positive F-measure:', scores.f_measure(refsets['positive'], testsets['positive']))
#        print('negative precision:', scores.precision(refsets['negative'], testsets['negative']))
#        print('negative recall:', scores.recall(refsets['negative'], testsets['negative']))
#        print('negative F-measure:', scores.f_measure(refsets['negative'], testsets['negative']))



