#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:23:37 2018

@author: jf
"""

from BookingWebScraping import BookingWebScraping

bws = BookingWebScraping()
bws.location = "co"
bws.country = "co"
bws.language = "es"
bws.language = "en-gb"
#bws.directory = "/run/media/jf/Datos/Tourist Text Mining/datasets/bws/"
bws.directory = "/home/luz/Python/web scraping/bws/"
bws.inputFilename = "colombia.html"
bws.getCountryReviews()

#for location in bws.getLocations("boyaca", "en-gb"):
#    print ("Processing " + location + "...")

#import pandas as pd
#hotel_df = pd.DataFrame.from_records(bws.hotelList, columns = ['hotelID', 'hotelName', 'hotelURL', 'location', 'cities'])
#hotel_df.to_csv('hotelList.csv', sep = ',')
#
#        self.hotelList = [
#['-578472', 'Hotel Habitel', '/hotel/co/habitel.en-gb.html', ['Teusaquillo', '-74.0732374038163', '4.61714866328819'], [['-578472', 'bogota']]],
#['1001827', 'Hotel Teusaquillo', '/hotel/co/teusaquillo-bogota.en-gb.html', ['Teusaquillo', '-74.0732374038163', '4.61714866328819'], [['-578472', 'bogota']]],
#['1003658', 'Hotel Feria Nova', '/hotel/co/feria-novia.en-gb.html', ['Teusaquillo', '-74.0960090085877', '4.63253851718474'], [['-578472', 'bogota']]],
#['1003660', 'Hotel Santiago Plaza', '/hotel/co/santiago-plaza.en-gb.html', ['Teusaquillo', '-74.0917264', '4.6329294'], [['-578472', 'bogota']]],
#['1004390', 'Hostal Parque Real', '/hotel/co/hostal-parque-real.en-gb.html', ['Santa Marta – Show on map', '-74.2137638855446', '11.2414812098759'], [['-598739', 'santa-marta']]],
#['1004392', 'Hotel Medellín Rodadero', '/hotel/co/medellin-rodadero.en-gb.html', ['Santa Marta – Show on map', '-74.226690530777', '11.1992614289905'], [['-598739', 'santa-marta']]],
#['1005177', 'Hotel Estadio 63A', '/hotel/co/estadio-63a.en-gb.html', ['Barrios Unidos', '-74.0714570134878', '4.65323543313627'], [['-578472', 'bogota']]],
#['1006000', 'Posada Turística Miss Geidy', '/hotel/co/posada-nativa-miss-geidy.en-gb.html', ['San Andrés – Show on map', '-81.7030997', '12.589044'], [['-597118', 'san-andres-co']]],
#['1006743', 'Posada Caribbean Refuge', '/hotel/co/posada-caribbean-refuge-san-andres.en-gb.html', ['San Andrés – Show on map', '-81.7262864112854', '12.5460912954843'], [['-597118', 'san-andres-co']]],
#['1007273', 'Posada Martha´s Place', '/hotel/co/posada-martha-s-place.en-gb.html', ['San Andrés – Show on map', '-81.7273324728012', '12.5467589259529'], [['-597118', 'san-andres-co']]],
#['1007316', 'Hospedería Casa Familiar', '/hotel/co/hospederia-casa-familiar-santa-marta.en-gb.html', ['Santa Marta – Show on map', '-74.2127617932541', '11.247052063254'], [['-598739', 'santa-marta']]],
#]

#self.hotelList = [[333347, "Hotel Andes Plaza", "/hotel/co/andes-plaza.es.html", ["Bogotá", -74.0481895208359, 4.68570495410158], [[-578472, "bogota"]]]]

# df = pd.read_csv('/run/media/jf/Datos/Tourist Text Mining/datasets/bws_es/hotelsReviews.csv', sep = ',', header = 0)
