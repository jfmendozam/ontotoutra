#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 00:20:39 2018

@author: jf
"""

import glob
import os
from pandas import pandas as pd
import matplotlib.pyplot as plt
import gensim
from gensim import corpora, models, similarities
#import gensim.models.doc2vec as d2v
#from sklearn.linear_model import SGDClassifier

from pygeocoder import Geocoder

from Country import Country
from Sentiment import Sentiment
#from pygeocoder import Geocoder
#import cartopy.crs as ccrs

df = pd.DataFrame()
path = r'/home/jf/Documentos/ontologies/web scrapping/workspace/WebScrapping/webscrapping/boyaca_en'
path = r'/home/jf/Documentos/ontologies/web scrapping/workspace/WebScrapping/webscrapping/colombia_es'
path = r'/home/jf/Documentos/ontologies/web scrapping/workspace/WebScrapping/webscrapping/colombia_en'
allFiles = glob.glob(os.path.join(path, "*.csv"))
df = pd.concat((pd.read_csv(f) for f in allFiles), ignore_index = True)

tmp = Country()
tmp.df = df
tmp.toEnglish('country')
tmp.addCountryAbbr('country')
df = tmp.df

tmp = Sentiment()
tmp.df = df
tmp.addSentiment('comment')
df = tmp.df

model = gensim.models.Word2Vec(tmp.corpus, min_count = 1, size = 32)

#tokenCorpus = [nltk.word_tokenize(sent.encode('utf-8')) for sent in df['comment']]


#print (df['country'].value_counts().nlargest(20))
#print (df['score'].groupby(df['country']).value_counts())
#print (df.groupby(['country', 'score']).country.value_counts().nlargest(15))





#plt.barh(df['country'], df['score'], align='center')

#plt.figure(figsize = (10, 3))
#df['country'].value_counts().plot(kind = 'barh')
    

#location = str('Bogota' + ',' + 'Colombia')
#result = Geocoder.geocode(location)
#coords = str(result[0].coordinates)
#lat = float(coords.split(',')[0].split('(')[1])
#lon = float(coords.split(',')[1].split(')')[0])
