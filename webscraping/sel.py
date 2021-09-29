#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 19:37:06 2018

@author: jf
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


#System.setProperty("webdriver.chrome.driver", );
driver = webdriver.Chrome(executable_path=r"/run/media/jf/Datos/Tourism Text Minning/web scrapping/chromedriver")

url = "https://www.booking.com/destinationfinder/countries/co.en-gb.html?aid=304142;label=gen173nr-1DCAwoggJCAlhYSDNYBGhGiAEBmAEKwgEDeDExyAEM2AED6AEBkgIBeagCAw;sid=b53c4aecb4e604c2280da4687e4320cd;dsf_source=3"
driver.get(url)

ids = driver.find_element(By.XPATH('//*[@class="load_more_places"]'))
ids.click()
    
time.sleep(8)

driver.close()

        #with open("bws.html", "w") as file:
        #     file.write(str(soup))
