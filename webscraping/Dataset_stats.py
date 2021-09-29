#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Jul 26 13:42:50 2018

@author: jf
"""

import pandas as pd
import numpy as np

#%%

class Dataset_stats:


    def __init__(self):
        """
        Default constructor
        """

        self.months_es = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
                          'julio', 'agosto', 'septiembre', 'octubre', 
                          'noviembre', 'diciembre']
        self.months_en = ['january', 'february', 'march', 'april', 'may', 
                          'june', 'july', 'august', 'september', 'october', 
                          'november', 'december']
        
        self.filename = '/home/jf/Documentos/phd/thesis/intership/dev/tourist text mining/datasets/colombia_es/3 reviews/hotel/hotelsReviews.csv'

        self.category_equivalence_es = [
                ['Viaje de negocios',      'Viaje de negocios'],
                ['Viaje de ocio',          'Viaje de ocio'],

                ['Pareja',                 'Pareja'],
                ['Persona que viaja sola', 'Persona que viaja sola'],
                ['Grupo',                  'Grupo'],
                ['Familia ',               'Familia'],
                ['llegada',                'Alojamiento asignado a la llegada'],
                ['Enviado por móvil',      'Enviado por móvil'],
                ['Con una mascota',        'Con una mascota'],
                ['movilidad reducida',     'Habitación para personas con movilidad reducida'],

                ['Suite',                  'Suite'],
                ['Apartamento',            'Apartamento'], 
                ['Loft',                   'Apartamento'],
                ['Alojamiento Vacacional', 'Apartamento'],
                ['Cabaña',                 'Cabaña'], 
                ['Yurta',                  'Cabaña'],
                ['Chalet',                 'Chalet'], 
                ['Chalé',                  'Chalet'], 
                ['Estudio',                'Estudio'],
                ['Casa',                   'Casa'], 
                ['Villa',                  'Villa'],
                ['Abadía',                 'Villa'],
                ['Tienda',                 'Tienda'],
                ['Camping',                'Tienda'],
                ['Carpa',                  'Tienda'],
                ['Caravana',               'Tienda'],
                ['Glamping',               'Tienda'],
                ['Bungalow',               'Cabaña'],

                ['Litera',                 'Habitación con litera'],
                ['Camarote',               'Habitación con camarote'],
                ['Hamaca',                 'Habitación con hamaca'],
                ['Familiar',               'Habitación familiar'],
                ['Deluxe',                 'Habitación deluxe'],
                ['Premiu',                 'Habitación deluxe'],
                ['Premier',                'Habitación deluxe'],
                ['Plus',                   'Habitación deluxe'],
                ['Lodge',                  'Habitación deluxe'],
                ['Lujo',                   'Habitación deluxe'],
                ['Superior',               'Habitación deluxe'],
                ['Torre Homenaje',         'Habitación deluxe'],
                ['Wonderful',              'Habitación deluxe'],
                ['Confort',                'Habitación deluxe'],
                ['Exclusive',              'Habitación deluxe'],
                ['Económica',              'Habitación económica'],
                ['Vista',                  'Habitación con vista panorámica'],
                ['compartid',              'Habitación compartida'],
                ['mixto',                  'Habitación compartida'],
                ['cama grande',            'Habitación con camas grandes'],
                ['cama extragrande',       'Habitación con camas grandes'],
                ['camas grandes',          'Habitación con camas grandes'],
                ['privad',                 'Habitación privada'],
                ['Matrimonial',            'Habitación para pareja'],
                ['Romántica',              'Habitación para pareja'],
                ['habitaciones',           'Múltiples habitaciones'],
                ['dormitorios',            'Múltiples habitaciones'],
                ['cama doble',             'Habitación con una cama doble'],
                ['camas dobles',           'Habitación con una cama doble'],
                ['2 camas',                'Habitación doble'],
                ['doble',                  'Habitación doble'],
                ['Dúplex',                 'Habitación doble'],
                ['3 camas',                'Habitación triple'],
                ['3 huéspedes',            'Habitación triple'],
                ['Triple',                 'Habitación triple'],
                ['4 huéspedes',            'Habitación con más de 3 camas'],
                ['5 huéspedes',            'Habitación con más de 3 camas'],
                ['6 camas',                'Habitación con más de 3 camas'],
                ['6 adultos',              'Habitación con más de 3 camas'],
                ['9 camas',                'Habitación con más de 3 camas'],
                ['12 camas',               'Habitación con más de 3 camas'],
                ['Cuádruple',              'Habitación con más de 3 camas'],
                ['Quíntuple',              'Habitación con más de 3 camas'],
                ['Séxtuple',               'Habitación con más de 3 camas'],
                ['Múltiple',               'Habitación con más de 3 camas'],
                ['Económic',               'Habitación económica'],
                ['Ecohab',                 'Habitación estándar'],
                ['Espectacular',           'Habitación estándar'],
                ['estándar',               'Habitación estándar'],
                ['fabuloso',               'Habitación estándar'],
                ['Habitación',             'Habitación estándar'],
                ['One Space',              'Habitación estándar'],
                ['Room',                   'Habitación estándar'],
                ['Ático',                  'Habitación estándar'],
                ]

        self.category_equivalence_en = [
                ['Business trip',          'Business trip'],
                ['Leisure trip',           'Leisure trip'],

                ['Couple',                 'Couple'],
                ['Solo traveller',         'Solo traveller'],
                ['Group',                  'Group'],
                ['People with friends',    'Group'],
                ['Family with',            'Family'],
                ['Check In',               'Room Selected at Check In'],
                ['Check-In',               'Room Selected at Check In'],
                ['Submitted via mobile',   'Submitted via mobile'],
                ['With a pet',             'With a pet'],
                ['Disability Access',      'Disability Access'],
                ['Mobility Access',        'Disability Access'],

                ['Studio',                 'Studio'],
                ['Apart',                  'Apartment'], 
                ['Loft',                   'Apartment'],
                ['Cabin',                  'Cabin'], 
                ['Yurt',                   'Cabin'],
                ['Bungalow',               'Cabin'],
                ['Cottage',                'Cabin'],
                ['Chalet',                 'Chalet'],
                ['Cabaña',                 'Chalet'],
                ['Penthouse',              'Suite'], 
                ['House',                  'House'],
                ['Maisonette',             'House'],
                ['Holiday Home',           'House'],
                ['Villa',                  'Villa'],
                ['Tent',                   'Tent'],
                ['Camp',                   'Tent'],
                ['Glamping',               'Tent'],
                ['Carpa',                  'Tent'],
                ['Family',                 'Family Suite'],
                ['Familiar',               'Family Suite'],
                ['Suite',                  'Suite'],

                ['Bunk',                   'Room with bunk bed'],
                ['Hammock',                'Room with hammock'],
                ['Deluxe',                 'Deluxe Room'],
                ['Premiu',                 'Deluxe Room'],
                ['Premier',                'Deluxe Room'],
                ['Superior',               'Deluxe Room'],
                ['Wonderful',              'Deluxe Room'],
                ['Luxury',                 'Deluxe Room'],
                ['Economy',                'Budget Room'],
                ['Economic',               'Budget Room'],
                ['Budget',                 'Budget Room'],
                ['View',                   'Room with panoramic view'],
                ['share',                  'Shared Room'],
                ['mixe',                   'Shared Room'],
                ['rooms',                  'Múltiple rooms'],
                ['Single Room',            'Single Room'],
                ['Sencill',                'Single Room'],
                ['One Bed',                'Single Room'],
                ['One Space',              'Single Room'],
                ['Double',                 'Double Room'],
                ['Doble',                  'Double Room'],
                ['Duplex',                 'Double Room'],
                ['Twin Room',              'Double Room'],
                ['Two Single Beds',        'Double Room'],
                ['Matrimonial',            'Double Room'],
                ['Triple',                 'Triple Room'],
                ['3-Bed',                  'Triple Room'],
                ['4-Bed',                  'Room with more than 3 beds'],
                ['4 Bed',                  'Room with more than 3 beds'],
                ['Quadruple',              'Room with more than 3 beds'],
                ['5-Bed',                  'Room with more than 3 beds'],
                ['Quintuple',              'Room with more than 3 beds'],
                ['Quíntuple',              'Room with more than 3 beds'],
                ['6-Bed',                  'Room with more than 3 beds'],
                ['7-Bed',                  'Room with more than 3 beds'],
                ['8-Bed',                  'Room with more than 3 beds'],
                ['9-Bed',                  'Room with more than 3 beds'],
                ['10-Bed',                 'Room with more than 3 beds'],
                ['11 Bed',                 'Room with more than 3 beds'],
                ['11-Bed',                 'Room with more than 3 beds'],
                ['12-Bed',                 'Room with more than 3 beds'],
                ['Adults',                 'Room with more than 3 beds'],
                ['2-Bed',                  'Double Room'],
                ['King Room',              'King Room'],
                ['Queen Room',             'Queen Room'],
                ['Private Room',           'Private Room'],
                ['Standard',               'Standard Room'],
                ['Classic Room',           'Standard Room'],
                ['Executive Room',         'Standard Room'],
                ['Spectacular',            'Standard Room'],
                ['Fabulous',               'Standard Room'],
                ['Dormitory Dome',         'Standard Room'],
                ['Basic Room',             'Standard Room'],
                ['Single Bed',             'Standard Room'],
                ['Ecohab',                 'Standard Room'],
                ['Business Room',          'Standard Room'],
                ['Room',                   'Standard Room'],
                ]

#%%
    def load_hotels_dataset_es(self, filename):
        """
           Load the hotels dataset (in Spanish) 
        """

        self.df = pd.read_csv(filename, index_col = False, header = 0)

        self.df['day'] = self.df['date'].apply(lambda x : int(x.split()[0]))
        self.df['month'] = self.df['date'].apply(lambda x : int(self.months_es.index(x.split()[2]) + 1))
        self.df['year'] = self.df['date'].apply(lambda x : int(x.split()[4]))
        self.df['stdate'] = pd.to_datetime(self.df['year'] * 10000 + self.df['month'] * 100 + self.df['day'], format = '%Y%m%d')

        self.df['score'] = self.df['score'].apply(lambda x : float(x.replace(',', '.')))

        self.df['tags'] = self.df['tags'].apply(lambda x : x.replace('[', '').replace(']', '').replace(" '", '').replace("'", '').split(","))

#%%
    def load_hotels_dataset_en(self, filename):
        """
           Load the hotels dataset (in Spanish) 
        """

        self.df = pd.read_csv(filename, index_col = False, header = 0)

        self.df['day'] = self.df['date'].apply(lambda x : int(x.split()[0]))
        self.df['month'] = self.df['date'].apply(lambda x : int(self.months_en.index(x.lower().split()[1]) + 1))
        self.df['year'] = self.df['date'].apply(lambda x : int(x.split()[2]))
        self.df['stdate'] = pd.to_datetime(self.df['year'] * 10000 + self.df['month'] * 100 + self.df['day'], format = '%Y%m%d')

        self.df['score'] = self.df['score'].apply(lambda x : float(x))

        self.df['tags'] = self.df['tags'].apply(lambda x : x.replace('[', '').replace(']', '').replace(" '", '').replace("'", '').split(","))

#%%
    def load_locations_dataset_es(self, filename):
        """
           Load the locations dataset
        """

        self.df = pd.read_csv(filename, index_col = False, header = 0)

        self.df['day'] = self.df['date'].apply(lambda x : int(x.split()[0]))
        self.df['month'] = self.df['date'].apply(lambda x : int(self.months_es.index(x.lower().split()[2]) + 1))
        self.df['year'] = self.df['date'].apply(lambda x : int(x.split()[4]))
        self.df['stdate'] = pd.to_datetime(self.df['year'] * 10000 + self.df['month'] * 100 + self.df['day'], format = '%Y%m%d')

#%%
    def load_locations_dataset_en(self, filename):
        """
           Load the locations dataset
        """

        self.df = pd.read_csv(filename, index_col = False, header = 0)

        self.df['day'] = self.df['date'].apply(lambda x : int(x.split()[0]))
        self.df['month'] = self.df['date'].apply(lambda x : int(self.months_en.index(x.lower().split()[1]) + 1))
        self.df['year'] = self.df['date'].apply(lambda x : int(x.split()[2]))
        self.df['stdate'] = pd.to_datetime(self.df['year'] * 10000 + self.df['month'] * 100 + self.df['day'], format = '%Y%m%d')

#%%
    def re_tag_es(self, category_equivalence):
        """
           Change to standard tags (in Spanish)
        """

        self.tags = dict()
        for instance in self.df['tags']:
            for tag in instance:
                find = False
                for key, value in self.tags.items():
                    if tag == key:
                        find = True
                        self.tags[key] += 1
                        break
                if not find:
                    self.tags[tag] = 1
        
        for tag_key, tag_value in self.tags.items():
            if isinstance(tag_value, int):
                if "Estancia de " in tag_key:
                    days = int(tag_key.split()[2])
                    if days > 7:
                        self.tags[tag_key] = "Estancia mayor de 1 semana"
                    else:
                        self.tags[tag_key] = tag_key

                for category in category_equivalence:
                    if category[0].lower() in tag_key.lower():
                        self.tags[tag_key] = category[1]
                        break

#%%
    def re_tag_en(self, category_equivalence):
        """
           Change to standard tags (in English)
        """

        self.tags = dict()
        for instance in self.df['tags']:
            for tag in instance:
                find = False
                for key, value in self.tags.items():
                    if tag == key:
                        find = True
                        self.tags[key] += 1
                        break
                if not find:
                    self.tags[tag] = 1
        
        for tag_key, tag_value in self.tags.items():
            if isinstance(tag_value, int):
                if "Stayed " in tag_key:
                    days = int(tag_key.split()[1])
                    if days > 7:
                        self.tags[tag_key] = "Stayed longer than 1 week"
                    else:
                        self.tags[tag_key] = tag_key

                for category in category_equivalence:
                    if category[0].lower() in tag_key.lower():
                        self.tags[tag_key] = category[1]
                        break
                    
#%%
    def add_new_tag(self):
        """
        Add tag fields to the dataset
        """

        tag_list = []
        for instance in self.df['tags']:
            row_list = []
            for tag in instance:
                new_tag = self.tags[tag]
                row_list.append(new_tag)
            tag_list.append(row_list)

        length = len(sorted(tag_list, key = len, reverse = True)[0])
        p = pd.DataFrame(data = np.array([t + [''] * (length - len(t)) for t in tag_list]),
                         columns = ["tag" + str(c) for c in range(1, length + 1)])
        for col in p.columns:
            self.df[col] = p[col]

#%%
    def stats(self, ds_type):
        """
        Get the dataset stats
        """

        if (ds_type == "hotel"):
            location_field = 'locationID'
        elif (ds_type == "location"):
            location_field = 'location'
        
        print("Dataset stats")
        print("Instances: ", len(self.df))
        print("Locations: ", self.df[location_field].nunique())
        print("Reviewers: ", self.df['author'].nunique())
        print("Countries: ", self.df['country'].nunique())
        print("Oldest review: ", min(self.df['stdate']))
        print("Recent review: ", max(self.df['stdate']))
        print("Days: ", self.df['date'].nunique())
        print("Score average: ", self.df['score'].mean())

        if (ds_type == "hotel"):
            print("Positive reviews:")
            print(" count: ", self.df['positiveReview'].count())
            print(" average length: ", self.df['positiveReview'].apply(lambda x:len(str(x))).mean())
            print(" words: ", self.df['positiveReview'].apply(lambda x:len(str(x).split())).mean())

            print("Negative reviews:")
            print(" count: ", self.df['negativeReview'].count())
            print(" average length: ", self.df['negativeReview'].apply(lambda x:len(str(x))).mean())
            print(" words: ", self.df['negativeReview'].apply(lambda x:len(str(x).split())).mean())

            print("Tags:")
            count = 0
            for col in self.df.columns:
                if "tag" in col:
                    count += 1
            for i in range(1, count):
                print("tag level", i, ": ", self.df['tag' + str(i)].apply(lambda x:1 if len(x) > 1 else 0).sum())

        elif (ds_type == "location"):
            print("Rating:")
            print(self.df['rating'].value_counts())
            print("Reviews:")
            print(" count: ", self.df['review'].count())
            print(" average length: ", self.df['review'].apply(lambda x:len(str(x))).mean())
            print(" words: ", self.df['review'].apply(lambda x:len(str(x).split())).mean())
        

#%%
    def run_stats(self, language, filename, ds_type):
        """
           Run the dataset statisticals
        """

        if (language == "es"):
            if (ds_type == "hotel"):
                self.load_hotels_dataset_es(filename)
                self.re_tag_es(self.category_equivalence_es)
                self.add_new_tag()
            elif (ds_type == "location"):
                self.load_locations_dataset_es(filename)
        elif (language == "en"):
            if (ds_type == "hotel"):
                self.load_hotels_dataset_en(filename)
                self.re_tag_es(self.category_equivalence_en)
                self.add_new_tag()
            elif (ds_type == "location"):
                self.load_locations_dataset_en(filename)
        
        self.stats(ds_type)
