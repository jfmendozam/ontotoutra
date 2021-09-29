#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 23:37:55 2018

@author: jf
"""

from textblob import TextBlob
import nltk

class Sentiment:
    def __init__(self):
        self.df = []
        self.polarity = []
        self.subjectivity = []
        self.corpus = []

    def addSentiment(self, field = 'comment'):
        for text in self.df[field]:
            text_blob = TextBlob(text)
            self.polarity.append(text_blob.polarity)
            self.subjectivity.append(text_blob.subjectivity)
            for word in [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text)]:
                self.corpus.append(word)

#            for word in [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text)]:
#                self.corpus.append(word)

        self.df['polarity'] = self.polarity
        self.df['subjectivity'] = self.subjectivity
        #self.df['corpus'] = [self.corpus]
