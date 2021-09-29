#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 17:24:51 2018

@author: jf
"""

import pycountry

class Country:
    def __init__(self):
        self.df = []

    def toEnglish(self, field = 'country'):
        countryDict = {
                'Abjasia': 'Russian Federation',
                'Abkhazia': 'Russian Federation',
                'Alemania': 'Germany',
                'Antártida': 'Antarctica',
                'Bahréin': 'Bahrain',
                'Bélgica': 'Belgium',
                'Bolivia': 'Bolivia, Plurinational State of',
                'Bonaire St. Eustatius and Saba': 'Bonaire, Sint Eustatius and Saba',
                'Brasil': 'Brazil',
                'Canadá': 'Canada',
                'Dinamarca': 'Denmark',
                'España': 'Spain',
                'Estados Unidos': 'United States',
                'Finlandia': 'Finland',
                'Francia': 'France',
                'Islas Vírgenes Británicas': 'United Kingdom',
                'Iran': 'Iran, Islamic Republic of',
                'Italia': 'Italy',
                'Japón': 'Japan',
                'Laos': "Lao People's Democratic Republic",
                'Líbano': 'Lebanon',
                'México': 'Mexico',
                'Nueva Zelanda': 'New Zealand',
                'none': 'Colombia',
                'Países Bajos': 'Netherlands',
                'Panamá': 'Panama',
                'Perú': 'Peru',
                'Reino Unido': 'United Kingdom',
                'República Dominicana': 'Dominican Republic',
                'Russia': 'Russian Federation',
                'South Korea': 'Korea, Republic of',
                'Suecia': 'Sweden',
                'Suiza': 'Switzerland',
                'Taiwan': 'Taiwan, Province of China',
                'United States of America': 'United States',
                'Venezuela': 'Venezuela, Bolivarian Republic of',
                'Vietnam': 'Viet Nam',
        }
        for key, value in countryDict.items():
            self.df[field].replace(key, value, inplace = True)

    def addCountryAbbr(self, field = 'country'):
        countries = {}
        for country in pycountry.countries:
            countries[country.name] = country.alpha3

        self.df['abbr'] = self.df[field].apply(lambda x : countries[x])
