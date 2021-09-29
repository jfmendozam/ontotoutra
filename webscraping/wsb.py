#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 18:07:07 2020

@author: luz and JF
"""
# pip install -U selenium
# pip install webdriver-manager
# Download the chromedriver file of ChromeDriver site or with python code
# 1. Web site: https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium import webdriver
import pandas as pd
from URL import URL
import fnmatch
import numpy as np
import ast

states = {
        'Amazonas': {'capital': 'Leticia', 'url': 'Amazonas,+Colombia', 'abrv': 'Amazon', 'id': 5131, 'lat': -4.077855, 'lon': -70.056213, 'type': 'region', 'reg_type': 'province'},
        'Antioquia': {'capital': 'Medellín', 'url': 'Antioquia,+Colombia', 'abrv': 'Antio', 'id': 5098, 'lat': 6.264933, 'lon': -75.467158, 'type': 'region', 'reg_type': 'province'},
        'Arauca': {'capital': '', 'url': 'Arauca,+Arauca,+Colombia', 'abrv': 'ara', 'id': -577427, 'lat': 7.08246, 'lon': -70.75702, 'type': 'city'},
        'Atlántico': {'capital': 'Barranquilla', 'url': 'Atlántico,+Colombia', 'abrv': 'Atlan', 'id': 5182, 'lat': 10.978864, 'lon': -74.84611, 'type': 'region', 'reg_type': 'province'},
        'Bogotá': {'capital': '', 'url': 'Bogotá,+Colombia', 'abrv': 'Bogo', 'id': -578472, 'lat': 4.61648, 'lon': -74.069373, 'type': 'city'},
        'Bolívar': {'capital': 'Cartagena', 'url': 'Bolivar,+Colombia', 'abrv': 'Boliv', 'id': 5135, 'lat': 10.374164, 'lon': -75.526307, 'type': 'region', 'reg_type': 'province'},
        'Boyacá': {'capital': 'Tunja', 'url': 'Boyacá,+Colombia', 'abrv': 'Boyac', 'id': 5178, 'lat': 5.678011, 'lon': -73.28576, 'type': 'region', 'reg_type': 'province'},
        'Caldas': {'capital': 'Manizales', 'url': 'Caldas,+Colombia', 'abrv': 'Caldas', 'id': 5103, 'lat': 5.127664, 'lon': -75.478355, 'type': 'region', 'reg_type': 'province'},
        'Caquetá': {'capital': 'Florencia', 'url': 'Caquetá,+Colombia', 'abrv': 'Caque', 'id': 5104, 'lat': 1.617935, 'lon': -75.61062, 'type': 'region', 'reg_type': 'province'},
        'Casanare': {'capital': 'Yopal', 'url': 'Casanare,+Colombia', 'abrv': 'Casana', 'id': 5105, 'lat': 5.268352, 'lon': -72.328708, 'type': 'region', 'reg_type': 'province'},
        'Cauca': {'capital': 'Popayán', 'url': 'Cauca,+Colombia', 'abrv': 'Cauca', 'id': 5183, 'lat': 2.505533, 'lon': -76.573148, 'type': 'region', 'reg_type': 'province'},
        'Cesar': {'capital': 'Valledupar', 'url': 'Cesar,+Colombia', 'abrv': 'Cesar', 'id': 5107, 'lat': 10.256708, 'lon': -73.307046, 'type': 'region', 'reg_type': 'province'},
        'Chocó': {'capital': 'Quibdo', 'url': 'Choco,+Colombia', 'abrv': 'Choco', 'id': 5181, 'lat': 7.151754, 'lon': -76.732422, 'type': 'region', 'reg_type': 'province'},
        'Córdoba': {'capital': 'Montería', 'url': 'Cordoba,+Colombia', 'abrv': 'Cordoba', 'id': 5129, 'lat': 9.030927, 'lon': -75.862848, 'type': 'region', 'reg_type': 'province'},
        'Cundinamarca': {'capital': '', 'url': 'Cundinamarca,+Colombia', 'abrv': 'Cundinam', 'id': 5110, 'lat': 4.68732, 'lon': -74.366746, 'type': 'region', 'reg_type': 'province'},
        'Guainía': {'capital': 'Puerto Inírida', 'url': 'Guainía,+Colombia', 'abrv': 'Guania', 'id': 5179, 'lat': 3.866928, 'lon': -67.922208, 'type': 'region', 'reg_type': 'province'},
        'Guaviare': {'capital': 'San José', 'url': 'Guaviare,+Colombia', 'abrv': 'Guaviare', 'id': 5112, 'lat': 2.565178, 'lon': -72.666761, 'type': 'region', 'reg_type': 'province'},
        'Huila': {'capital': 'Neiva', 'url': 'Huila,+Colombia', 'abrv': 'Huila', 'id': 5505, 'lat': 2.643487, 'lon': -74.439289, 'type': 'region', 'reg_type': 'province'},
        'La Guajira': {'capital': 'Riohacha', 'url': 'La+Guajira%2C+Colombia', 'abrv': 'La+Guajira', 'id': 5180, 'lat': 11.383638, 'lon': -73.205721, 'type': 'region', 'reg_type': 'province'},
        'Magdalena': {'capital': 'Santa Marta', 'url': 'Magdalena,+Colombia', 'abrv': 'Magdalena', 'id': 5114, 'lat': 11.203006, 'lon': -74.174366, 'type': 'region', 'reg_type': 'province'},
        'Meta': {'capital': 'Villavicencio', 'url': 'Meta,+Colombia', 'abrv': 'Meta', 'id': 5115, 'lat': 4.074242, 'lon': -73.591891, 'type': 'region', 'reg_type': 'province'},
        'Nariño': {'capital': 'Pasto', 'url': 'Nariño,+Colombia', 'abrv': 'Nariñ', 'id': 5116, 'lat': 1.182717, 'lon': -77.440279, 'type': 'region', 'reg_type': 'province'},
        'Norte de Santander': {'capital': 'Cúcuta', 'url': 'Norte+de+Santander,+Colombia', 'abrv': 'Norte+de+Santander', 'id': 5117, 'lat': 7.908419, 'lon': -72.682909, 'type': 'region', 'reg_type': 'province'},
        'Putumayo': {'capital': 'Mocoa', 'url': 'Putumayo,+Colombia', 'abrv': 'Putu', 'id': 5118, 'lat': 1.004133, 'lon': -76.502918, 'type': 'region', 'reg_type': 'province'},
        'Quindío': {'capital': 'Armenia', 'url': 'Quindio,+Colombia', 'abrv': 'Quind', 'id': 5119, 'lat': 4.562988, 'lon': -75.69423, 'type': 'region', 'reg_type': 'province'},
        'Risaralda': {'capital': 'Pereira', 'url': 'Risaralda,+Colombia', 'abrv': 'Risara', 'id': 5120, 'lat': 4.843666, 'lon': -75.703515, 'type': 'region', 'reg_type': 'province'},
        'San Andrés y Providencia': {'capital': 'San Andrés', 'url': 'San+Andres+Isla+-+Colombia,+San+Andrés,+San+Andres+and+Providencia+Islands,+Colombia', 'abrv': 'San+An', 'id': -597118, 'lat': 12.583026, 'lon': -81.696053, 'type': 'city'},
        'Santander': {'capital': 'Bucaramanga', 'url': 'Santander,+Colombia', 'abrv': 'Santander', 'id': 5121, 'lat': 6.735787, 'lon': -73.223134, 'type': 'region', 'reg_type': 'province'},
        'Sucre': {'capital': 'Sincelejo', 'url': 'Sucre,+Colombia', 'abrv': 'Sucre', 'id': 5122, 'lat': 9.489594, 'lon': -75.60579, 'type': 'region', 'reg_type': 'province'},
        'Tolima': {'capital': 'Ibagué', 'url': 'Tolima,+Colombia', 'abrv': 'Tolima', 'id': 5123, 'lat': 4.366013, 'lon': -74.861691, 'type': 'region', 'reg_type': 'province'},
        'Valle del Cauca': {'capital': 'Cali', 'url': 'Valle+del+Cauca,+Colombia', 'abrv': 'Valle+del+', 'id': 5124, 'lat': 3.651338, 'lon': -76.507921, 'type': 'region', 'reg_type': 'province'},
        'Vaupés': {'capital': 'Mitú', 'url': 'Vaupes,+Colombia', 'abrv': 'Vaupes', 'id': 5097, 'lat': 1.251696, 'lon': -70.233295, 'type': 'region', 'reg_type': 'province'},
        'Vichada': {'capital': 'Puerto Carreño', 'url': 'Vichada,+Colombia', 'abrv': 'Vicha', 'id': 5125, 'lat': 5.024488, 'lon': -69.028611, 'type': 'region', 'reg_type': 'province'},
}

tags = {
       'hotelTag': {'hotelData': False, 'tag': "//div[contains(@data-et-click, 'customGoal:')]"},
       'hotelID': {'hotelData': True, 'type': 'attribute', 'tag': 'data-hotelid'},
       'hotelName': {'hotelData': True, 'type': 'css', 'tag': '.sr-hotel__title-wrap [data-et-click="    "]'},
       'reviewScore': {'hotelData': True, 'type': 'css', 'tag': '.sr_item_review_block [class="bui-review-score__badge"]'},
       'reviewNumber': {'hotelData': True, 'type': 'css', 'tag': '.sr_item_review_block [class="bui-review-score__text"]'},
       'reviewCategoricalScore': {'hotelData' : True, 'type': 'css', 'tag': '.sr_item_review_block [class="bui-review-score__title"]'},
       'hotelCity': {'hotelData': True, 'type': 'css', 'tag': '.sr_card_address_line [rel="noopener"]'},
       'hotelDescription': {'hotelData': True, 'type': 'css', 'tag': '.sr_item_main_block [class="hotel_desc"]'},
       'hotelLocation':  {'hotelData': True, 'type': 'cssattribute', 'tag': '[class="bui-link"]', 'tag2': 'data-coords'},
       'hotelUrl':  {'hotelData': True, 'type': 'cssattribute', 'tag': '[class="hotel_name_link url"]', 'tag2': 'href'},
       'hotelNextPage': {'hotelData': True, 'type': 'xpath', 'tag': "//li[@class='bui-pagination__pages'] //a[contains(@class,'bui-pagination__link sr_pagination_link')]", 'tag2': 'href'},
       'offset': {'hotelData': False, 'tag' : '&offset='},
       'hotelsNum': {'hotelData': False, 'type': 'css', 'tag' : "h1[class='sorth1']"},
       'hotelServices': {'hotelData': False, 'type': 'css', 'tag' : '.facilitiesChecklist [class="facilitiesChecklistSection"]'},       
       'reviewPage': {'hotelData': False, 'tag': "li[class='review_list_new_item_block']"},
       'tabReview': {'hotelData': False, 'tag': 'tab-reviews'},
       'barScoreTitle': {'hotelData': False, 'tag': '.c-score-bar [class="c-score-bar__title"]'},
       'barScore': {'hotelData': False, 'tag': '.c-score-bar [class="c-score-bar__score"]'},
       'nextReviewURL': {'hotelData': False, 'tag': "//a[@class='bui-pagination__link']"},
       'positiveTitle': {'hotelData': False, 'tag': 'Gustó'},
       'negativeTitle': {'hotelData': False, 'tag': 'No gustó'},
       'usefulTitle': {'hotelData': False, 'tag': 'Útil'},
       'uselessTitle': {'hotelData': False, 'tag': 'Poco útil'},
       'stayedTitle': {'hotelData': False, 'tag': 'Se alojó en'},
       'hotelAddress': {'hotelData': False, 'tag': '.wrap-hotelpage-top [class="address address_clean"]'},
}

    
def getHotelData(d, state, nextURL):
    """
    Get hotel data

    Parameters
    ----------
    d : webdriver.Chrome
        The Google Chrome Driver.
    state : dictionary
        State data.

    Returns
    -------
    hotelsDF: Pandas DataFrame.
        Hotels data

    """
    
    # Download the chromedriver file of ChromeDriver site or with python code
    # 1. Web site: https://sites.google.com/a/chromium.org/chromedriver/downloads
    # from webdriver_manager.chrome import ChromeDriverManager
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # hotelsDF = getHotelData(d, url.startURLbyCountry())
    # hotelsDF = getHotelData(d, url.startURLbyCity(states['Arauca']))
    
    if nextURL == '':
        url = URL()
        if state['type'] == 'region':
            d.get(url.startURLbyRegion(state))
        elif state['type'] == 'city':
            d.get(url.startURLbyCity(state))
    else:
        d.get(nextURL)

    hotels = []
    for hotel in d.find_elements_by_xpath(tags['hotelTag']['tag']):
        hotelDict = {}
        for k, v in tags.items():
            if v['hotelData']:
                try:
                    if v['type'] == 'attribute':
                        hotelDict[k] = hotel.get_attribute(v['tag'])
                    elif v['type'] == 'css':
                        hotelDict[k] = hotel.find_element_by_css_selector(
                            v['tag']
                        ).text
                    elif v['type'] == 'cssattribute':
                        hotelDict[k] = hotel.find_element_by_css_selector(
                            v['tag']
                        ).get_attribute(v['tag2'])  
                except:
                    hotelDict[k] = None

        hotelDict['state'] = state['id']
        hotels.append(hotelDict)

    hotelsDF = pd.DataFrame(hotels)
    print(hotelsDF)

    hotelsDF['hotelID'] = hotelsDF['hotelID'].apply(lambda x : int(x))
    hotelsDF['reviewScore'] = hotelsDF['reviewScore'].apply(
        lambda  x: 0 if x is None else float(x.replace(',', '.'))
    )
    hotelsDF['reviewNumber'] = hotelsDF['reviewNumber'].apply(
        lambda x: 0 if x is None else int(x.split()[0].replace('.', ''))
    )
    hotelsDF['hotelCity'] = hotelsDF['hotelCity'].apply(
        lambda x: x.replace('Mostrar en el mapa', '')
    )
    hotelsDF['hotelLon'] = hotelsDF['hotelLocation'].apply(
        lambda x: x.split(',')[0]
    )
    hotelsDF['hotelLat'] = hotelsDF['hotelLocation'].apply(
        lambda x: x.split(',')[1]
    )
    hotelsDF = hotelsDF.drop(['hotelLocation'], axis = 1)
    
    return hotelsDF


def getNextPageURL(d):
    """
    Get the URL from the next page.

    Parameters
    ----------
    d : webdriver.Chrome
        The Google Chrome Driver.

    Returns
    -------
    nextPageURL: string
        The next page URL.
    linesPerPage : int
        Instances number per page.
    totalPages : int
        Total next pages.
    hotelsNum : int
        Hotels number by country.

    """
    url_page_hotel = d.find_elements_by_xpath(tags['hotelNextPage']['tag'])
    if (len(url_page_hotel)):
        page = [elem.get_attribute(tags['hotelNextPage']['tag2']) for elem in url_page_hotel]
            
        linesPerPage = int(fnmatch.filter(
            page[len(page) - 1].split('&'), 'rows*'
        )[0].split('=')[1])
        lastOffset = int(page[len(page) - 1].split("=")[-1])
        totalPages = int(lastOffset / linesPerPage)
        hotelsNum = int([item.text for item in d.find_elements_by_css_selector(
            tags['hotelsNum']['tag'])][0].split(':')[1].split()[0].replace('.', '')
        )
        return page[0], linesPerPage, totalPages, hotelsNum
    else:
        hotelsNum = int([item.text for item in d.find_elements_by_css_selector(
            tags['hotelsNum']['tag'])][0].split(':')[1].split()[0].replace('.', '')
        )
        return None, 0, 0, hotelsNum


def getHotelServices(d, hotelsDF):
    """
    Get the hotel services
    Parameters
    ----------
    d : webdriver.Chrome
        The Google Chrome Driver.
    hotelsDF : Pandas DataFrame
        Hotels data
    Returns
    -------
    None.
    """

    hotelServices = []
    for index, hotel in hotelsDF.iterrows():
        print(
            "Service (" + str(index + 1) + "/"  + str(len(hotelsDF)) + ") " 
            + hotel.hotelName
        )
        d.get(hotel.hotelUrl)
        services = [item.text for item in d.find_elements_by_css_selector(
            tags['hotelServices']['tag']
        )]

        serviceDict = {}
        for service in services:
            serviceList = service.split('\n')
            k = serviceList[0]
            del serviceList[0]
            serviceDict[k] = serviceList
        hotelServices.append(serviceDict)

    hotelsDF['hotelServices'] = hotelServices
    return hotelsDF, hotelServices

def getHotelScoreBars(d):
    """
    Get hotel categorical score 
    (Personal, Instalaciones y servicios, Limpieza, Confort, 
     Relación calidad-precio, Ubicación, WiFi gratis)

    Parameters
    ----------
    d : webdriver.Chrome
        The Google Chrome Driver.

    Returns
    -------
    dictionary
        The hotel categorical score.

    """

    bar_title = [x.rstrip() for x in [
        item.text for item in d.find_elements_by_css_selector(
            tags['barScoreTitle']['tag']
        )
    ]]
    bar_score = [item.text for item in d.find_elements_by_css_selector(
        tags['barScore']['tag']
    )]

    return dict(zip(bar_title, [float(i.replace(',', '.')) for i in bar_score]))


def reviewStructuralAnalysis(text):
    reviews = text.split('\n')

    if reviews[0].find(' ') >= 0:     # Split User and country
        tmp = reviews[0].split(' ')
        reviews.insert(1, tmp[1])
        reviews[0] = tmp[0]

    if reviews[1].replace(',', '', 1).isnumeric():  # Has it country?
        reviews.insert(1, 'No country')

                                        # Split reviews and positive title
    if len(fnmatch.filter(reviews, tags['positiveTitle']['tag'] + '*')) > 0:
        index = reviews.index(
            fnmatch.filter(reviews, tags['positiveTitle']['tag'] + '*')[0]
        )
        if len(fnmatch.filter(reviews, tags['positiveTitle']['tag'] + '*')[0]) \
            > len(tags['positiveTitle']['tag']):
            tmp = reviews[index].split('·')
            if (len(tmp) > 1):
                reviews.insert(index + 1, ' ·' + tmp[1])
                reviews[index] = tags['positiveTitle']['tag']

                                        # Split reviews and negative title
    if len(fnmatch.filter(reviews, tags['negativeTitle']['tag'] + '*')) > 0:
        index = reviews.index(
            fnmatch.filter(reviews, tags['negativeTitle']['tag'] + '*')[0]
        )
        if len(fnmatch.filter(reviews, tags['negativeTitle']['tag'] + '*')[0]) \
            > len(tags['negativeTitle']['tag']):
            tmp = reviews[index].split('·')
            reviews.insert(index + 1, ' ·' + tmp[1])
            reviews[index] = tags['negativeTitle']['tag']

    if len(fnmatch.filter(reviews, tags['stayedTitle']['tag'] + '*')) <= 0:
                                        # Replace with stayed row
        if len(fnmatch.filter(reviews, tags['usefulTitle']['tag'] + '*')) > 0:
            index = reviews.index(
                fnmatch.filter(reviews, tags['usefulTitle']['tag'] + '*')[0]
            )
            reviews[index] = tags['stayedTitle']['tag'] + ': unspecified room'
        else:
            reviews.insert(
                len(reviews), tags['stayedTitle']['tag'] + ': unspecified room'
            )

                                        # Replace with accomodation date row
        accomodationDate = ' '.join([
            reviews[3].split(' ')[-3].capitalize(), 
            reviews[3].split(' ')[-2], 
            reviews[3].split(' ')[-1]
        ])
        if len(fnmatch.filter(reviews, tags['uselessTitle']['tag'] + '*')) > 0:
            index = reviews.index(
                fnmatch.filter(reviews, tags['uselessTitle']['tag'] + '*')[0]
            )
            reviews[index] = accomodationDate
        else:
            index = reviews.index(
                fnmatch.filter(reviews, tags['stayedTitle']['tag'] + '*')[0]
            ) + 1
            reviews.insert(index, accomodationDate)
    
                                            # Add dummy row
        if reviews[-1] == accomodationDate:
            reviews.insert(
                len(reviews),
                tags['usefulTitle']['tag'] + ' ' + tags['uselessTitle']['tag']
            )

    return '\n'.join(reviews)


def getHotelReview(block, hotel):
    headers = {
        'userId': 0, 'country': 1, 'rating': 2, 'reviewDate': 3, 'catRating': 4
    }

    reviews = []
    for user in block:
        review = {}

        text = reviewStructuralAnalysis(user.text)
        comment = text.split('\n')

        for k, v in headers.items():
            review[k] = comment[v]

        try:
            index1 = comment.index(tags['positiveTitle']['tag'])
        except:
            index1 = -1
        try:
            index2 = comment.index(tags['negativeTitle']['tag'])
        except:
            index2 = -1

        if index1 != -1 or index2 != -1:
            index3 = comment.index(fnmatch.filter(
                comment, tags['stayedTitle']['tag'] + '*'
            )[0])

            if index1 != -1:
                start = index1 + 1
                if index2 != -1:
                    end = index2 - 1
                else:
                    end = index3 - 1

                s = comment[start]
                for i in range(start + 1, end + 1):
                    s += '\n' + comment[i] 

                review['positiveReview'] = s

            if index2 != -1:
                start = index2 + 1
                end = index3 - 1

                s = comment[start]
                for i in range(start + 1, end + 1):
                    s += '\n' + comment[i]

                review['negativeReview'] = s

        if len(fnmatch.filter(comment, tags['stayedTitle']['tag'] + '*')) <= 0:
            review['accommodation'] = tags['stayedTitle']['tag'] + ': unspecified room'
            review['accommodationDate'] = ' '.join([
                review['reviewDate'].split(' ')[-3].capitalize(), 
                review['reviewDate'].split(' ')[-2], 
                review['reviewDate'].split(' ')[-1]
            ])
        else:
            review['accommodation'] = fnmatch.filter(
                comment, tags['stayedTitle']['tag'] + '*'
            )[0]
            index4 = comment.index(review['accommodation']) + 1
            review['accommodationDate'] = comment[index4]

        review['hotelID'] = hotel['hotelID']
        reviews.append(review)

    reviewsDF = pd.DataFrame(reviews)
    reviewsDF = reviewsDF.replace(np.nan, '', regex=True)
    reviewsDF['rating'] = reviewsDF['rating']\
        .apply(lambda  x: float(x.replace(',', '.')))
    reviewsDF['accommodation'] = reviewsDF['accommodation']\
        .apply(lambda x: x.replace(tags['stayedTitle']['tag'] + ': ', ''))
    reviewsDF['reviewDate'] = reviewsDF['reviewDate']\
        .apply(lambda x: x.replace('Comentó en: ', '')\
        .replace('La elección de los viajeros ', ''))
    if index1 != -1:
        reviewsDF['positiveReview'] = reviewsDF['positiveReview']\
            .apply(lambda x: x.replace(' · ', ''))
    if index2 != -1:
        reviewsDF['negativeReview'] = reviewsDF['negativeReview']\
            .apply(lambda x: x.replace(' · ', ''))

    return list(reviewsDF.T.to_dict().values())


def getHotelReviews(d, hotel):
    """
    

    Parameters
    ----------
    d : TYPE
        DESCRIPTION.
    hotel : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    if hotel.reviewNumber == 0:
        return([])

    block = d.find_elements_by_css_selector(tags['reviewPage']['tag'])
    rowsPerPage = 10

    if hotel.reviewNumber > rowsPerPage:
        while True:
            try:
                nextURLBlock = d.find_elements_by_xpath(
                    tags['nextReviewURL']['tag']
                )
                lastURL = [elem.get_attribute('href') for elem in nextURLBlock][-1]
                url = '&' . join(
                    [i for i in lastURL.split('&') if i.find('offset') == -1]
                )
                break
            except (IndexError, ValueError, KeyError):
                pass

    offset = 0
    hotelReviewsList = []
    while True:
        bunchList = getHotelReview(block, hotel)
        hotelReviewsList += bunchList
        offset += len(bunchList)

        if offset >= hotel['reviewNumber'] - 1:          
            break
        else:
            while True:
                d.get(url + '&offset=' + str(offset))
                block = d.find_elements_by_css_selector(tags['reviewPage']['tag'])
                if len(block) == 0:
                    break
                try:
                    a = block[0].text
                    break
                except (IndexError, ValueError, KeyError):
                    pass
            if len(block) == 0:
                break
            
    return hotelReviewsList


def getHotelComments(d, hotelsDF):
    """
    Get the hotel services
    Parameters
    ----------
    d : webdriver.Chrome
        The Google Chrome Driver.
    hotelsDF : Pandas DataFrame
        Hotels data
    Returns
    -------
    Pandas DataFrame
        The hotel dataframe.
    """

    hotel_scores = []
    hotel_reviews = []
    for index, hotel in hotelsDF.iterrows():
        if index >= 0:
            print(
                "Reviews (" + str(index + 1) + "/" + str(len(hotelsDF)) + ") " 
                + hotel.hotelName + " (" + str(hotel.reviewNumber) 
                + " reviews)..."
            )
            if hotel.reviewNumber != 0:
                urlHotelReviews = hotel.hotelUrl[:-9] + tags['tabReview']['tag']
                d.get(urlHotelReviews)

                hotel_scores.append(getHotelScoreBars(d))
                hotel_reviews.append(getHotelReviews(d, hotel))
            else:
                hotel_scores.append({})
                hotel_reviews.append({})

    hotelsDF['scores']  = hotel_scores
    hotelsDF['reviews'] = hotel_reviews

    return hotelsDF, hotel_reviews, hotel_scores

def getHotelAddress(d, hotelsDF):
    """
    Get the hotel address
    Parameters
    ----------
    d : webdriver.Chrome
        The Google Chrome Driver.
    hotelsDF : Pandas DataFrame
        Hotels data
    Returns
    -------
    None.
    """

    addressList = []
    for index, hotel in hotelsDF.iterrows():
        print(
            "Address (" + str(index + 1) + "/"  + str(len(hotelsDF)) + ") " 
            + hotel.hotelName
        )
        d.get(hotel.hotelUrl)
        address = [item.text for item in d.find_elements_by_css_selector(
            tags['hotelAddress']['tag']
        )]
        if len(address) <= 0:
            address = ["No Address–"]
        addressList.append(address)

    hotelsDF['hotelAddress'] = addressList
    hotelsDF['hotelAddress'] = hotelsDF.hotelAddress.apply(
        lambda x: x[0].split('–')[0]
    )

    return hotelsDF

#%%

#rootDir = '/home/jf/Documentos/PhD/Thesis/Dev/WebScraping/'
rootDir = '/home/jf/Documentos/education/phd/thesis/dev/ontologies/01 Web Scraping to MySQL/web scrapping/workspace/WebScrapping/2020 webscraping/'
chromeDriverDir = rootDir + 'chromedriver/chromedriver'
d = webdriver.Chrome(chromeDriverDir)
datasetDir = rootDir + 'dataset/'

#state = states['Vichada']
for k, state in states.items():
    hotelsDF = getHotelData(d, state, '')

    urlNextPage, hotelsPerPage, totalPages, hotelsNum = getNextPageURL(d)
    startInstance = len(hotelsDF) if hotelsPerPage == 0 else hotelsPerPage
    while (startInstance + 1 <= hotelsNum):
        newURL = urlNextPage + tags['offset']['tag'] + str(startInstance)
        hotelsDF = hotelsDF.append(
            getHotelData(d, state, newURL), 
            ignore_index = True
        )
        startInstance += hotelsPerPage

    hotelsDF = getHotelAddress(d, hotelsDF)

    hotelsDF, hotel_services = getHotelServices(d, hotelsDF)
    #hotelsDF = pd.read_csv(datasetDir + state['abrv'] + '_hotels.csv')
    hotelsDF, hotel_reviews, hotel_scores = getHotelComments(d, hotelsDF)
    # hotelLon,hotelLat,hotelServices,hotelAddress,scores,reviews 

    hotelsDF.drop_duplicates(subset = "hotelID", inplace = True)
    hotelsDF.reset_index(drop = True)

    hotelsDF.to_csv(
        datasetDir + state['abrv'] + '_hotels.csv',
        index = False,
        header = True
    )

    hotelsDF.to_csv(
        datasetDir + state['abrv'] + '_super.csv',
        index = False, 
        header = True
    )

    servicesDF = pd.DataFrame(hotel_services)
    servicesDF['hotelID'] = hotelsDF['hotelID']
    servicesDF.to_csv(
        datasetDir + state['abrv'] + '_services.csv',
        index = False, 
        header = True
    )

    scoresDF = pd.DataFrame(hotel_scores)
    scoresDF['hotelID'] = hotelsDF['hotelID']
    scoresDF.to_csv(
        datasetDir + state['abrv'] + '_scores.csv',
        index = False,
        header = True
    )

    # Get the keys of the dictionary list
    list(dict.fromkeys([k for i in hotel_reviews[0] for k, v in i.items()]))
    # Get the hotel reviews Dataframe
    hreviews = []
    for hotel in hotel_reviews:
        for comment in hotel:
            hreviews.append(comment)
    reviewsDF = pd.DataFrame(hreviews)
    reviewsDF.to_csv(
        datasetDir + state['abrv'] + '_reviews.csv',
        index = False,
        header = True
    )

    # reviews_test = pd.read_csv(
    #    datasetDir + state['abrv'] + '_reviews.csv',
    #    dtype = {"rating" : "float64", "hotelID" : "int64"},
    #    sep = ",",
    #    header = 0
    # )
