#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 17:28:12 2018

@author: jf
"""

class URL:
    """ Build the URL for searching """


    def __init__(self):
        """ Default constructor """

        self.protocol      = "https://"
        self.domain        = "www.booking.com/"
        self.finder        = "destinationfinder/"
        self.urlLocation   = "cities/"
        self.country       = "co/"
        self.countryName   = "Colombia"
        self.search        = "searchresults."
        self.action        = "reviews"
        self.langSeparator = "."
        self.language      = "es"       # en-gb
        self.extension     = ".html"
        self.separator     = "?"
        self.aid           = "aid=304142"
        self.label         = "label=gen173nr-1DCAwoggJCAlhYSDNYBGhGiAEBmAEKwgEDeDExyAEM2AED6AEBkgIBeagCAw"
        self.sid           = "sid=f5f179eb5ef60b26541843337b9e81db"
        self.dsf           = "dsf_source=13"
        self.pageviewid    = 'a296a12429ce00bb'
        
        self.countries     = {
            'Colombia'     : {'id' : 47, 'lat' : 3.88373, 'lon' : -73.1938},
        }


    def buildRegionURL(self, search, language):
        """ Build the region URL
            Parameters:
                - search: URL search
                - language: Search language
        """

        self.urlLocation = "regions/"
        self.language = language
        self.search = search
        self.dsf = "dsf_source=3"
        url = self.protocol \
                    + self.domain \
                    + self.finder \
                    + self.urlLocation \
                    + self.country \
                    + self.search \
                    + self.langSeparator \
                    + self.language \
                    + self.extension \
                    + self.separator \
                    + self.aid \
                    + self.label \
                    + self.sid \
                    + self.dsf
        return url


    def buildCountryURL(self, search, language):
        """ Build the country URL
            Parameters:
                - search: URL search
                - language: Search language
        """

        url = "https://www.booking.com/destinationfinder/countries/"
        url += search + "." + language + ".html?"
        url += self.aid + ";" + self.label + ";" + self.sid + ";"
        url += "dsf_source=3"
        return url


    def buildLocalURL(self, country, search, language):
        """ Build the local URL
            Parameters:
                - country: Search country
                - search: URL search
                - language: Search language
        """

        url = "https://www.booking.com/destinationfinder/cities/"
        url += country + "/" + search + "/reviews." + language + ".html?"
        url += self.aid + ";" + self.label + ";" + self.sid + ";"
        url += "dsf_source=13"
        return url


    def buildLocalHomeURL(self, country, search, language):
        """ Build the local URL
            Parameters:
                - country: Search country
                - search: URL search
                - language: Search language
        """

        url = "https://www.booking.com/destinationfinder/cities/"
        url += country + "/" + search + "." + language + ".html?"
        url += self.aid + ";" + self.label + ";" + self.sid + ";"
        url += "dsf_source=1"
        return url


    def buildLocalPropertiesURL(self, locationID, language):
        """ Build the local properties URL
            Parameters:
                - locationID: Location identification
                - language: Search language
        """

        url = "https://www.booking.com/searchresults."
        url += language + ".html?"
        url += self.aid + ";" + self.label + ";" + self.sid + ";"
        url += "city=" + str(locationID) + ";src=destinationfinder&"
        return url

    def buildNextPropertyURL(self, locationID, language, page):
        """ Build the local properties URL
            Parameters:
                - locationID: Location identification
                - language: Search language
        """

        url = "https://www.booking.com/searchresults."
        url += language + ".html?"
        url += self.aid + ";" + self.label + ";" + self.sid + ";"
        url += "city=" + str(locationID)  + ";"
        url += "class_interval=1;dest_id=" + str(locationID) + ";"
        url += "dest_type=city;dtdisc=0;inac=0;index_postcard=0;"
        url += "label_click=undef;postcard=0;room1=A%2CA;sb_price_type=total;"
        url += "src=destinationfinder;ss_all=0;ssb=empty;sshis=0;rows=15;"
        url += "offset=" + str(page * 15)
        return url

    def buildPropertiesURL(self, language = 'en-gb', country = 'Colombia'):
        
        url  = self.protocolcountry
        url += self.domain
        
        self.search = 'searchresults.'
        url += self.search
        url += language
        url += '.html?'
        
        self.label = 'gen173nr-1DCAEoggI46AdICVgEaDKIAQGYAQm4ARnIAQzYAQPoAQH4AQKIAgGoAgO4AuDMuvQFwAIB'
        url += 'label=' + self.label + "&"
        
        url += 'lang=' + language + '&'
        
        self.sid = 'ba4ee5dd8cf90d6f8020106628f2392a'
        url += 'sid=' + self.sid + '&'

        url += 'sb=1&'
        url += 'sb_lp=1&'
        url += 'src=index&'
        url += 'src_elem=sb&'
        url += 'ss=' + country.capitalize() + '&'
        url += 'is_ski_area=0&'
        url += 'checkin_year=&'
        url += 'checkin_month=&'
        url += 'checkout_year=&'
        url += 'checkout_month=&'
        url += 'group_adults=2&'
        url += 'group_children=0&'
        url += 'no_rooms=1&'
        url += 'b_h4u_keep_filters=&'
        url += 'from_sf=1&'
        url += 'ss_raw=' + country.lower() + '&'
        url += 'ac_position=0&'
        url += 'ac_langcode=' + language[:2] + '&'
        url += 'ac_click_type=b&'
        url += 'dest_id=' + str(self.countries[country.capitalize()]['id']) + '&'
        url += 'dest_type=country&'
        url += 'place_id_lat=' + str(self.countries[country.capitalize()]['lat']) + '&'
        url += 'place_id_lon=' + str(self.countries[country.capitalize()]['lon']) + '&'
        
        url += 'search_pageview_id=' + self.pageviewid + '&'
        url += 'search_selected=true'
        
        return url


    def buildHotelURL(self, hotelURL, language):
        """ Build the hotel URL
            Parameters:
                - hotelURL   : Hotel URL
                - language   : Search language
        """

        hotelName = hotelURL.split('/')[3].split('.')[0]
        url = "https://www.booking.com/reviews/co/hotel/"
        url += hotelName + "." + language + ".html?"
        url += self.aid + ";" + self.label + ";" + self.sid
        return url



    def buildNextHotelPageURL(self, hotelURL, language, numPage):
        """ Build the hotel URL
            Parameters:
                - hotelURL   : Hotel URL
                - language   : Search language
        """

        hotelName = hotelURL.split('/')[3].split('.')[0]
        url = "https://www.booking.com/reviews/co/hotel/"
        url += hotelName + "." + language + ".html?"
        url += self.aid + ";" + self.label + ";" + self.sid
        url += "customer_type=total;hp_nav=0;old_page=0;"
        url += "order=featuredreviews;page=" + str(numPage) + ";"
        url += "r_lang=en;rows=75&"
        return url

    def startURLbyCountry(self):
        """
        Build the start URL by country

        Returns
        -------
        url : string
            start URL by Country

        """
        self.label = 'label=gen173nr-1DCAEoggI46AdIM1gEaDKIAQGYAQq4ARnIAQzYAQPoAQGIAgGoAgO4ApvV4_QFwAIB'
        self.sid = 'sid=78b82c38c254c0b4e576ed5f0ef5b97c'

        url =  self.protocol + self.domain
        url += self.search + self.language + self.extension + self.separator
        url += self.label + '&'
        url += self.sid + '&'

        url += 'sb=1&'
        url += 'sb_lp=1&'
        url += 'src=index&'
        url += 'src_elem=sb&'
        url += 'ss=' + self.countryName.capitalize() + '&'
        url += 'checkin_year=&'
        url += 'checkin_month=&'
        url += 'checkout_year=&'
        url += 'checkout_month=&'
        url += 'group_adults=2&'
        url += 'group_children=0&'
        url += 'no_rooms=1&'
        url += 'b_h4u_keep_filters=&'
        
        return url

    def startURLbyCity(self, city):
        """
        Build the start URL by city

        Parameters
        ----------
        city : dictionary
            The city dictionary.
        
        Returns
        -------
        url : string
            start URL by City

        """
        self.label = 'label=gen173nr-1DCAEoggI46AdIM1gEaDKIAQGYAQq4ARnIAQzYAQPoAQGIAgGoAgO4ApvV4_QFwAIB'
        self.sid = 'sid=78b82c38c254c0b4e576ed5f0ef5b97c'

        url =  self.protocol + self.domain
        url += self.search + self.language + self.extension + self.separator
        url += self.label + '&'
        url += self.sid + '&'

        url += 'sb=1&'
        url += 'sb_lp=1&'
        url += 'src=index&'
        url += 'src_elem=sb&'
        url += 'ss=' + city['url'] + '&'  
        url += 'is_ski_area=&'
        url += 'checkin_year=&'
        url += 'checkin_month=&'
        url += 'checkout_year=&'
        url += 'checkout_month=&'
        url += 'group_adults=2&'
        url += 'group_children=0&'
        url += 'no_rooms=1&'
        url += 'b_h4u_keep_filters=&'
        url += 'from_sf=1&'
        url += 'ss_raw=' + city['abrv'] + '&'
        url += 'ac_position=0&'
        url += 'ac_langcode=' + self.language + '&'
        url += 'ac_click_type=b&'
        url += 'dest_id=' + str(city['id']) + '&'
        url += 'dest_type=' + city['type'] + '&'
        url += 'place_id_lat=' + str(city['lat']) + '&'
        url += 'place_id_lon=' + str(city['lon']) + '&'
        
        self.pageviewid = '44da6e10f14e00a9'
        url += 'search_pageview_id=' + self.pageviewid + '&'
        url += 'search_selected=true&'
        url += 'search_pageview_id=' + self.pageviewid + '&'
        url += 'ac_suggestion_list_length=5&'
        url += 'ac_suggestion_theme_list_length=0'
        
        return url
    
    def startURLbyRegion(self, region):
        """
        Build the start URL by region (state)

        Parameters
        ----------
        region : dictionary
            The region dictionary.
        
        Returns
        -------
        url : string
            start URL by Region

        """
        self.label = 'label=gen173nr-1DCAEoggI46AdIM1gEaDKIAQGYAQq4ARnIAQzYAQPoAQGIAgGoAgO4ApvV4_QFwAIB'
        self.sid = 'sid=78b82c38c254c0b4e576ed5f0ef5b97c'

        url =  self.protocol + self.domain
        url += self.search + self.language + self.extension + self.separator
        url += self.label + '&'
        url += self.sid + '&'

        url += 'sb=1&'
        url += 'sb_lp=1&'
        url += 'src=index&'
        url += 'src_elem=sb&'
        url += 'ss=' + region['url'] + '&'  
        url += 'is_ski_area=&'
        url += 'checkin_year=&'
        url += 'checkin_month=&'
        url += 'checkout_year=&'
        url += 'checkout_month=&'
        url += 'group_adults=2&'
        url += 'group_children=0&'
        url += 'no_rooms=1&'
        url += 'b_h4u_keep_filters=&'
        url += 'from_sf=1&'
        url += 'ss_raw=' + region['abrv'] + '&'
        url += 'ac_position=0&'
        url += 'ac_langcode=' + self.language + '&'
        url += 'ac_click_type=b&'
        url += 'dest_id=' + str(region['id']) + '&'
        url += 'dest_type=' + region['type'] + '&'
        url += 'place_id_lat=' + str(region['lat']) + '&'
        url += 'place_id_lon=' + str(region['lon']) + '&'
        
        self.pageviewid = '3bba9c011df30086'
        url += 'search_pageview_id=' + self.pageviewid + '&'
        url += 'search_selected=true&'
        url += 'region_type=' + region['reg_type'] + '&'
        url += 'search_pageview_id=' + self.pageviewid + '&'
        url += 'ac_suggestion_list_length=5&'
        url += 'ac_suggestion_theme_list_length=0'
        
        return url
    