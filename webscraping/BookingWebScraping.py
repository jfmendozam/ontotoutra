#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 9 17:08:00 2020

@author: Luz & JF
"""

from bs4 import BeautifulSoup
import requests
import os
import csv

from URL import URL

class BookingWebScraping:
    """ Web Scrapping for www.booking.com website """


    def __init__(self):
        """ Default constructor """

        self.locationList              = []
        # hotelList: 0 - hotelID, 1 - hotelName, 2 - hotelURL
        #            3.1 - location, 3.2 - Latitude, 3.3 - Longitude
        #            4.1 - locationID, 4.2 - locationName
        self.hotelList                 = []
        self.language                  = "es"       # Search language
        self.location                  = ""         # Search location
        self.directory                 = ""         # Output directory
        self.locationHeader = ['location', 'score', 'rating', 'date',\
                               'review', 'author', 'country']
        self.hotelHeader = ['locationID', 'date', 'author', 'country', 'score',\
                            'positiveReview', 'negativeReview', 'tags']
        self.source                    = ""         # Data source: Website or file
        self.inputFilename             = ""         # Local filename
        self.country                   = "co"       # Country abbreviation
        self.countryName               = "Colombia" # Country name
        self.web                       = False      # Is the web the data source?

        # Search city keywords 2018
        # self.cityKeyword = {
        #         'start'    : 'drow ddeck',
        #         'top'      : 'dcol w100',
        #         'city'     : 'dcol w50_m_up w33_l_up',
        #         'topClick' : 'dcol w66_xl_up dcard__head dcard__header__image dcard_js_click',
        #         'click'    : ' card_border frontborder4 ',
        #         'id'       : 'dsf_section--more ',
        #         'review'   : {
        #                 'start'   : 'dsf-review',
        #                 'rate'    : 'dsf-review__rate-text',
        #                 'score'   : 'dsf-review__rate-score',
        #                 'date'    : 'dsf-review__date',
        #                 'text'    : 'dsf-review__text',
        #                 'author'  : 'dsf-review__author-name',
        #                 'country' : 'dsf-review__author-country',
        #                 }
        #         }
        
        # Search city keywords 2020
        self.cityKeyword = {
                'start'    : 'bui-carousel__item',
                'top'      : 'dcol w100',
                'city'     : 'dcol w50_m_up w33_l_up',
                'topClick' : 'dcol w66_xl_up dcard__head dcard__header__image dcard_js_click',
                'click'    : ' card_border frontborder4 ',
                'id'       : 'dsf_section--more ',
                'review'   : {
                        'start'   : 'dsf-review',
                        'rate'    : 'dsf-review__rate-text',
                        'score'   : 'dsf-review__rate-score',
                        'date'    : 'dsf-review__date',
                        'text'    : 'dsf-review__text',
                        'author'  : 'dsf-review__author-name',
                        'country' : 'dsf-review__author-country',
                        }
                }

        # Search hotel list keyword
        self.hotelKeyword = {
                'start'    : ' nodates_hotels wider_image ',
                'first'    : 'sr_item sr_item_new sr_item_default sr_property_block sr_item_bs sr_item_no_dates ',
                'other'    : 'sr_item sr_item_new sr_item_default sr_property_block sr_item_no_dates ',
                'id'       : 'data-hotelid',
                'name'     : 'sr-hotel__name ',
                'score'    : 'sr-review-score ',
                'location' : ' jq_tooltip district_link visited_link ',
                'coord'    : 'bicon-map-pin show_map map_address_pin',
                'coords'   : 'data-coords',
                'pages'    : 'results-paging',
                'review'   : {
                        'start'    : 'review_list',
                        'item'     : 'review_item clearfix ',
                        'date_es'  : 'Escrito en ',
                        'author'   : 'review_item_reviewer',
                        'country'  : 'reviewer_country',
                        'text'     : 'review_item_review',
                        'score'    : 'review-score-badge',
                        'positive' : 'review_pos ',
                        'negative' : 'review_neg ',
                        'tags'     : 'review_info_tag ',
                        'pages'    : 'page_link review_next_page',
                        }
                }
        
        # Booking properties tags
        self.propertyTags = {
            'startH' : {'htmlTag' : 'div', 'tag' : 'sr_item  sr_item_new sr_item_default sr_property_block  sr_flex_layout sr_item_no_dates       sr_item--highlighted       '},
            'start'  : {'htmlTag' : 'div', 'tag' : 'sr_item  sr_item_new sr_item_default sr_property_block  sr_flex_layout sr_item_no_dates         '},
        }


    def getLocations(self, region, language):
        """ Get locations from a region
            Parameters:
                - region: Region for searching
                - language: Search language
        """

        url = URL()
        source = requests.get(url.buildRegionURL(region, language)).text
        regionSoup = BeautifulSoup(source, 'lxml')

        region = regionSoup.find('div', class_ = 'dsf_to_refresh')
        locations = []

        try:
            topCity = region.find('div', class_ = "dsf-top-city").a['href']
            locations.append(topCity.split('/')[4].split(".")[0])
        except Exception as e:
            pass

        try:
            for city in region.find_all('div', class_ = 'dsf_city'):
                try:
                    locations.append(city.find('div', class_ = ' card_border frontphoto_filter_1 ').a['href'].split('/')[4].split(".")[0])
                except Exception as e:
                    pass
        except Exception as e:
            print (region)

        return locations


    def getPropertiesReviews(self):
        """ Get the hotels reviews """

        url = URL()
        kw = self.hotelKeyword['review']
        reviewsList = []
        index = 1
        for hotel in self.hotelList:
            print(hotel[1] + " (" + str(index) + " of "\
                  + str(len(self.hotelList)) + ") ")
            index += 1

            hotelURL = hotel[2]
            urlText = url.buildHotelURL(hotelURL, self.language)
            nextPage = True
            numPage = 1

            while (nextPage):
                source = requests.get(urlText).text
                soup = BeautifulSoup(source, 'lxml')
                reviews = soup.find('ul', class_ = kw['start'])

                try:
                    for review in reviews.find_all('li', class_ = kw['item']):

                        try:
                            if (self.language == "es"):
                                date = ' '.join(review.p.text.\
                                                replace(kw['date_es'], '').\
                                                split())
                            else:
                                date = ' '.join(review.p.text.split(':')[1]\
                                                .split())
                        except Exception as e:
                            date = ""

                        try:
                            author = ' '.join(review\
                                              .find('div', class_ = kw['author'])\
                                              .h4.span.text.split())
                        except Exception as e:
                            author = ""

                        try:
                            country = ' '.join(review\
                                               .find('span', class_ = kw['country'])\
                                               .select('span > span')[0]\
                                               .text.split())
                        except Exception as e:
                            country = ""

                        try:
                            score = ' '.join(review\
                                       .find('span', class_ = kw['score'])\
                                       .text.split())
                        except Exception as e:
                            score = ""

                        try:
                            positiveReview = ' '.join(review\
                                                .find('p', class_ = kw['positive'])\
                                                .span.text.split())
                        except Exception as e:
                            positiveReview = ""

                        try:
                            negativeReview = ' '.join(review\
                                                .find('p', class_ = kw['negative'])\
                                                .span.text.split())
                        except Exception as e:
                            negativeReview = ""

                        try:
                            tags = []
                            for tag in review.find_all('li', class_ = kw['tags']):
                                tags.append(' '.join(tag.text.split('•')[1].split()))
                        except Exception as e:
                            tags = []

                        item = [hotel[0], date, author, country, score,\
                                positiveReview, negativeReview, tags]
                        reviewsList.append(item)
                except Exception as e:
                    pass

                try:
                    if (soup.find('p', class_ = kw['pages']).a.text):
                        nextPage = True
                        numPage += 1
                        urlText = url.buildNextHotelPageURL(hotelURL,\
                                      self.language, numPage)
                    else:
                        nextPage = False
                except Exception as e:
                    nextPage = False

        return reviewsList


    def addLocation(self, hotelID, hotelName, hotelURL, hotelLocation, lat, lon, locationID, location):
        """ Add the location to the list
            Parameters:
                - hotelID       : Hotel identification
                - hotelName     : Hotel name
                - hotelURL      : Hotel URL
                - hotelLocation : Hotel location name
                - lat           : Latitude of the coordinate of the hotel location
                - lon           : Longitude of the coordinate of the hotel location
                - locationID    : Location Identification
                - location      : Location name
        """

        found = False
        index = 0
        for hotel in self.hotelList:
            if (hotel[0] == hotelID):
                found = True
                break
            index += 1

        if (found):
            cities = self.hotelList[index][4]
            if (not [locationID, location] in cities):
                cities.append([locationID, location])
                cities.sort()
                self.hotelList[index][4] = cities
        else:
            self.hotelList.append([\
                    hotelID,\
                    hotelName,\
                    hotelURL,\
                    [hotelLocation, lat, lon],\
                    [[locationID, location]]\
                    ])
            self.hotelList.sort()


    def getPropertiesList(self, locationID, location):
        """ Get the properties reviews
            Parameters:
                - locationID: Location code
                - location: Location name
        """

        url = URL()
        urlText = url.buildLocalPropertiesURL(locationID, self.language)
        source = requests.get(urlText).text
        soup = BeautifulSoup(source, 'lxml')

        kw = self.hotelKeyword

        try:
            numPages = int(soup.find('div', class_ = kw['pages'])\
                           ['aria-label'].split(',')[1].split(' ')[1])
        except Exception as e:
            numPages = 0

        for page in range(1, numPages + 1):
            print((page % 10), end = "")

            if (page > 1):
                urlText = url.buildNextPropertyURL(locationID,\
                                                   self.language, page)
                source = requests.get(urlText).text
                soup = BeautifulSoup(source, 'lxml')
            try:
                hotels = soup.find('div', class_ = kw['start'])
                if (page == 1):
                    hotelItems = hotels.find('div', class_ = kw['first'])

                    hotelID = hotelItems[kw['id']]
                    hotelLocation = " ".join(hotelItems.\
                                             find('a', class_ = kw['location'])\
                                             .text.split()).split(',')[0]
                    lat = hotelItems.find('a', class_ = kw['coord'])\
                                    [kw['coords']].split(',')[0]
                    lon = hotelItems.find('a', class_ = kw['coord'])\
                                    [kw['coords']].split(',')[1]
                    hotelName = " ".join(hotelItems.find('span',\
                                                         class_ = kw['name'])\
                                         .text.split())
                    hotelURL = hotelItems.find('div', class_ = kw['score'])\
                                         .a['href'].split(";")[0]

                    self.addLocation(hotelID, hotelName, hotelURL,\
                                     hotelLocation, lat, lon,\
                                     locationID, location)
            except Exception as e:
                pass

            try:
                hotelItems = hotels.find_all('div', class_ = kw['other'])
                for hotel in hotelItems:
                    try:
                        hotelID = hotel[kw['id']]
                        hotelLocation = " ".join(hotel.find('a', class_ = kw['location'])\
                                           .text.split()).split(',')[0]
                        lat = hotel.find('a', class_ = kw['coord'])\
                                   [kw['coords']].split(',')[0]
                        lon = hotel.find('a', class_ = kw['coord'])\
                                   [kw['coords']].split(',')[1]
                        hotelName = " ".join(hotel.find('span',\
                                                        class_ = kw['name'])\
                                             .text.split())
                        hotelURL = hotel.find('div', class_ = kw['score'])\
                                        .a['href'].split(";")[0]

                        self.addLocation(hotelID, hotelName, hotelURL,\
                                         hotelLocation, lat, lon,\
                                         locationID, location)
                    except Exception as e:
                        continue
            except Exception as e:
                pass


    def getLocationID(self, location):
        """ Get Booking location code
            Parameters:
                - location: Location name
        """

        url = URL()
        urlText = url.buildLocalHomeURL(self.country, location, self.language)
        source = requests.get(urlText).text
        soup = BeautifulSoup(source, 'lxml')
        cityID = soup.find('div', class_ = self.cityKeyword['id'])\
                     .a['href'].split('&')[0].split('=')[1]
        return cityID


    def hotel2CSV(self, reviews):
        """ Save the comments to a CSV file
            Parameters:
                - reviews: Reviews list
        """

        fileDir = os.path.dirname(self.directory)
        filename = os.path.join(fileDir, 'hotels.csv')

        csvFile = open(filename, 'w')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(self.hotelHeader)
        csvWriter.writerows(reviews)
        csvFile.close()


    def location2CSV(self, location, reviews):
        """ Save the comments to a CSV file
            Parameters:
                - location: Location name
                - reviews: Reviews list
        """

        folder = self.directory + location + "/"
        if not os.path.exists(folder):
            os.makedirs(folder)
        fileDir = os.path.dirname(folder)
        filename = os.path.join(fileDir, location + '.csv')

        csvFile = open(filename, 'w')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(self.locationHeader)
        csvWriter.writerows(reviews)
        csvFile.close()


    def getLocationReviews(self, location):
        """ Get the reviews list by city
            Parameters:
                - location: Location name
        """

        reviewsList = []
        kw = self.cityKeyword['review']

        url = URL()
        urlText = url.buildLocalURL(self.country, location, self.language)
        source = requests.get(urlText).text
        soup = BeautifulSoup(source, 'lxml')
        reviews = soup.find_all('div', class_ = kw['start'])

        for review in reviews:
            score = int(review.find('div', class_ = kw['score']).text)
            rating = ' '.join(review\
                              .find('div', class_ = kw['rate']).text.split())
            date = ' '.join(review\
                            .find('div', class_ = kw['date']).text.split())
            try:
                comment = review.find('div', class_ = kw['text'])
                paragraphs = comment.find_all('p')
                commentsList = []
                for paragraph in paragraphs:
                    commentsList.append(paragraph.text.replace("\r", ""))
                    comments = '. '.join(commentsList).replace(".. ", ". ")\
                                   .replace(".  .", ". ")
            except Exception as e:
                comments = ""
            try:
                author = ' '.join(review\
                                  .find('div', class_ = kw['author'])\
                                  .text.split())
            except Exception as e:
                author = "anonymous"

            try:
                country = ' '.join(review\
                                   .find('div', class_ = kw['country'])\
                                   .text.split())
            except Exception as e:
                country = "none"

            item = [location, score, rating, date, comments, author, country]
            reviewsList.append(item)

        return reviewsList


    def getSource(self):
        """ Get the data source: web or local file """

        self.web = False
        if (len(self.inputFilename) > 0):
            fileDir  = os.path.dirname(self.directory)
            filename = os.path.join(fileDir, self.inputFilename)

            if (not os.path.isfile(filename)):
                self.web = True
        else:
            self.web = True

        if (self.web):
            url = URL()
            urlText = url.buildCountryURL(self.location, self.language)
            source = requests.get(urlText).text
        else:
            source = open(filename)
            
        return source
        
        
    def getLocationsByCountry(self):
        """ Get the cities list by country """

        locations = []
        kw = self.cityKeyword

        source = self.getSource()
        countrySoup = BeautifulSoup(source, 'lxml')
        country = countrySoup.find('div', class_ = kw['start'])

        try:
            cities = country.find_all('div', class_ = kw['top'])
            for city in cities:
                try:
                    cityName = city.find('div',\
                                         class_ = kw['topClick'])\
                                         ['data-href']\
                                         .split('/')[4]\
                                         .split(".")[0]
                    locations.append(cityName)
                except Exception as e:
                    continue
        except Exception as e:
            pass

        try:
            cities = country.find_all('div', class_ = kw['city'])
            for city in cities:
                try:
                    pos = 4
                    if (not self.web):
                        pos = pos + 2

                    cityName = city.find('div', class_ = kw['click'])\
                                   .a['href'].split('/')[pos].split(".")[0]
                    locations.append(cityName)
                except Exception as e:
                    continue
        except Exception as e:
            pass

        if (not self.web):
            source.close()

        return locations

    def getPropertySource(self):
        """ Get the data source: web or local file """

        self.web = False
        if (len(self.inputFilename) > 0):
            fileDir  = os.path.dirname(self.directory)
            filename = os.path.join(fileDir, self.inputFilename)

            if (not os.path.isfile(filename)):
                self.web = True
        else:
            self.web = True

        if (self.web):
            url = URL()
            urlText = url.buildPropertiesURL(self.language, self.countryName)
            source = requests.get(urlText).text
        else:
            source = open(filename)
            
        return source

    def getPropertiesByCountry(self):
        """
        Get properties (hotels) list from web or local file.

        Returns
        Property list
        """
        
        properties = []
        kw = self.propertyTags
        
        source = self.getPropertySource()
        self.countrySoup = BeautifulSoup(source, 'lxml')
        print(kw['startH']['tag'] + "#")
        country = self.countrySoup.find(kw['startH']['htmlTag'], class_ = kw['startH']['tag'])
        print(country)
        #self.propertyTags = {
        #     'startH' : {'htmlTag' : 'div', 'tag' : 'sr_item  sr_item_new sr_item_default sr_property_block  sr_flex_layout sr_item_no_dates       sr_item--highlighted       '},
        #     'start'  : {'htmlTag' : 'div', 'tag' : 'sr_item  sr_item_new sr_item_default sr_property_block  sr_flex_layout sr_item_no_dates         '},
        # }

        

    def getCountryReviews(self):
        """ Get the user reviews of the a country given """

        # self.locationList = self.getLocationsByCountry()
        # self.hotelList = []

        # for location in self.locationList:
        #     print("\n" + location + ": ", end = "")
        #     locationReviews = self.getLocationReviews(location)
        #     self.location2CSV(location, locationReviews)
        #     locationID = self.getLocationID(location)
        #     self.getPropertiesList(locationID, location)

        # hotelsReviews = self.getPropertiesReviews()
        # self.hotel2CSV(hotelsReviews)
        
        self.hotelList = self.getPropertiesByCountry()
