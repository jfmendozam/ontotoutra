#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 18:07:07 2020

@author: luz
"""
# pip install -U selenium
# pip install webdriver-manager
from selenium import webdriver
import pandas as pd
import fnmatch

#%% Get hotel data

# Download the chromedriver file of ChromeDriver site or with python code
# 1. Web site: https://sites.google.com/a/chromium.org/chromedriver/downloads
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())

dir = '/home/luz/Python/web scraping/chromedriver/chromedriver'
d = webdriver.Chrome(dir)
d.get(
      'https://www.booking.com/searchresults.es.html?label=gen173nr-1DCAEoggI46AdIM1gEaDKIAQGYAQq4ARnIAQzYAQPoAQGIAgGoAgO4ApvV4_QFwAIB&sid=78b82c38c254c0b4e576ed5f0ef5b97c&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.es.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaDKIAQGYAQq4ARnIAQzYAQPoAQGIAgGoAgO4ApvV4_QFwAIB%3Bsid%3D78b82c38c254c0b4e576ed5f0ef5b97c%3Bsb_price_type%3Dtotal%26%3B&ss=Colombia&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters='   
)

# Colombia: 9.359 alojamientos encontrados
hotelsNum = [
    item.text for item in d.find_elements_by_css_selector("h1[class='sorth1']")
]

tags = {
       'hotelID'               : {'type': 'attribute', 'tag': 'data-hotelid'},
       'hotelName'             : {'type': 'css', 'tag': '.sr-hotel__title-wrap [data-et-click="    "]'},
       'reviewScore'           : {'type': 'css', 'tag': '.sr_item_review_block [class="bui-review-score__badge"]'},
       'reviewNumber'          : {'type': 'css', 'tag': '.sr_item_review_block [class="bui-review-score__text"]'},
       'reviewCategoricalScore': {'type': 'css', 'tag': '.sr_item_review_block [class="bui-review-score__title"]'},
       'hotelCity'             : {'type': 'css', 'tag': '.sr_card_address_line [rel="noopener"]'},
       'hotelDescription'      : {'type': 'css', 'tag': '.sr_item_main_block [class="hotel_desc"]'},
       'hotelLocation'         : {'type': 'cssattribute', 'tag': '[class="bui-link"]', 'tag2':'data-coords'},
       'hotelUrl'              : {'type': 'cssattribute', 'tag': '[class="hotel_name_link url"]', 'tag2':'href'}       
}

hotels = []
for hotel in d.find_elements_by_xpath("//div[contains(@data-et-click, 'customGoal:')]"):
    hotelDict = {}
    for k, v in tags.items():
        try:
            if v['type'] == 'attribute':
                hotelDict[k] = hotel.get_attribute(v['tag'])  
            elif v['type'] == 'css':
                hotelDict[k] = hotel.find_element_by_css_selector(v['tag']).text
            elif v['type'] == 'cssattribute':
                hotelDict[k] = hotel.find_element_by_css_selector(v['tag']).get_attribute(v['tag2'])  
        except:
            hotelDict[k] = None
    hotels.append(hotelDict)
hotelsDF = pd.DataFrame(hotels)


#%% Get hotels page url by CSS

# <li class="bui-pagination__pages">  class="bui-pagination__link sr_pagination_link"
url_page_hotel = d.find_elements_by_xpath("//li[@class='bui-pagination__pages'] //a[contains(@class,'bui-pagination__link sr_pagination_link')]") 
page = [elem.get_attribute('href') for elem in url_page_hotel]

pageFirts = page[0]    # Page firts
pageSecond = page[1]   # Page firts + &offset=25
pageSecond = page[2]   # Page firts + &offset=50



                                
#%% Test for finding specific data of one hotel

dir = '/home/luz/Python/web scraping/chromedriver/chromedriver'
d = webdriver.Chrome(dir)
d.get(
      'https://www.booking.com/hotel/co/palmetto-apartamento-602-frente-a-la-playa.es.html?label=gen173nr-1BCAEoggI46AdIM1gEaDKIAQGYAQq4ARnIAQzYAQHoAQGIAgGoAgO4ApvV4_QFwAIB&sid=88da4754de46f2132ee96adaceaf859c&dest_id=47&dest_type=country&group_adults=2&group_children=0&hapos=1&hpos=1&no_rooms=1&sr_order=popularity&srepoch=1587502660&srpvid=6d0893625e9400ab&ucfs=1&from=searchresults;highlight_room=#hotelTmpl'
)

# --- change: #blockdisplay4 by #tab-reviews
url_com = d.find_elements_by_xpath("//a[@class='hp_nav_reviews_link toggle_review track_review_link_zh']") 
url_comments = [elem.get_attribute('href') for elem in url_com]

# Add to url #tab-reviews

headers = {'userId':0, 'country':1, 'rating':2, 'reviewDate':3, 'catRating':4,
           'acommodation':-3, 'acommodationDate':-2}


reviews = []
for user in d.find_elements_by_css_selector("li[class='review_list_new_item_block']"):
    review = {}
    comment = (user.text).split('\n') 
    for k, v in headers.items():
        review[k] = comment[v]
    
    try:
        index1 = comment.index('Gustó')
    except:
        index1 = -1
    try:
        index2 = comment.index('No gustó')
    except:
        index2 = -1

    index3 = comment.index(fnmatch.filter(comment, 'Se alojó en*')[0])

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
        
    reviews.append(review)
  
    
# <li class="bui-pagination__pages">  class="bui-pagination__link sr_pagination_link"
url_page_comment = d.find_elements_by_xpath("//a[@class='bui-pagination__link']") 
page_rew = [elem.get_attribute('href') for elem in url_page_comment]

#%% Hotel services  ************************  

data_services = {'bathroom':0, 'outdoors':1, 'pets':2, 'activities':3, 
                 'foodDrink':4, 'internet':5, 'parking':6, 'receptionServices':7,
                 'cleaningServices':8, 'businesFacilities':9, 'wellnessFacilities':10,
                 'shops':11, 'miscellaneous':12}

services = [item.text for item in d.find_elements_by_css_selector(
    '.facilitiesChecklist [class="facilitiesChecklistSection"]')]
print(services)


#%% User Comments 

# Personal, Instalaciones y servicios, Limpieza, Confort, Relación calidad-precio, Ubicación, WiFi gratis
bar_title = [item.text for item in d.find_elements_by_css_selector(
    '.c-score-bar [class="c-score-bar__title"]')]
print(bar_title)

bar_score = [item.text for item in d.find_elements_by_css_selector(
    '.c-score-bar [class="c-score-bar__score"]')]
print(bar_score)

# ******** Review scores by user
user_review = [item.text for item in d.find_elements_by_css_selector(
    '.review_list_new_item_block [class="bui-avatar-block__title"]')]

# Country
location_review = [item.text for item in d.find_elements_by_css_selector(
    '.review_list_new_item_block [class="bui-avatar-block__subtitle"]')]
print(location_review)

# Review date (comentó en: fecha) and Accommodation date (Se alojó en:)
date_review = [item.text for item in d.find_elements_by_css_selector(
    '.review_list_new_item_block [class="c-review-block__date"]')]
print(date_review)

data_reviews = [item.text for item in d.find_elements_by_css_selector(
    "li[class='review_list_new_item_block']")]

#%% Hotel information

# hotelName = [item.text for item in d.find_elements_by_css_selector('.sr-hotel__title-wrap [data-et-click="    "]')]
# print(hotelName)

# reviewScore = [item.text for item in d.find_elements_by_css_selector('.sr_item_review_block [class="bui-review-score__badge"]')]
# print(reviewScore)

# reviewNumber = [item.text for item in d.find_elements_by_css_selector('.sr_item_review_block [class="bui-review-score__text"]')]
# print(reviewNumber)

# reviewCatScore = [item.text for item in d.find_elements_by_css_selector('.sr_item_review_block [class="bui-review-score__title"]')]
# print(reviewCatScore)

# hotelCity = [item.text for item in d.find_elements_by_css_selector('.sr_card_address_line [rel="noopener"]')]
# print(hotelCity) 

# hotelDescription = [item.text for item in d.find_elements_by_css_selector('.sr_item_main_block [class="hotel_desc"]')]
# print(hotelDescription)

# Hotel id by XPATH
# num = d.find_elements_by_xpath("//div[contains(@data-et-click, 'customGoal:')]")
# id_hotel = []
# for i in num:
#     if i.get_attribute("data-hotelid") != "null":
#         id_hotel.append(i.get_attribute("data-hotelid"))    

# ********** Hotel city location by XPATH
#c = d.find_elements_by_xpath("//a[contains(@class, 'bui-link')]")
# c = d.find_elements_by_xpath("//a[@class='bui-link' and contains(@href,'/hotel/')]") 
# coord = []
# for i in c:
#     if i.get_attribute("data-coords") != "null":
#         coord.append(i.get_attribute("data-coords"))

# # ******** Hotel city location by CSS
# loc = d.find_elements_by_css_selector('[class="bui-link"]')
# loc_city = [elem.get_attribute('data-coords') for elem in loc]

# url_hotel = d.find_elements_by_css_selector('[class="hotel_name_link url"]')
# url = [elem.get_attribute('href') for elem in url_hotel]

