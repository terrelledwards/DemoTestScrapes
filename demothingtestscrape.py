#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 14:18:23 2023

@author: tedwards
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata, unidecode

"""
On the lowest level, we want to scrape the brand info page for each brand 
Before that, we want to grab each brand 
In order to grab each brand, we need to 

Things to do: 
    Extraction of relevant data from info
    Accessing
    Make a function that takes in a string and returns the string all lowercase with - in all whitespace
"""

def scrape_brand_info_test():
    #r = get('https://thingtesting.com/brands/flair-chocolatier/info')
    r = get('https://thingtesting.com/brands/up-up-chocolate/info')
    #Have tested on multiple different sources. As long as the brand name is correctly divided up, the general form should work
    if r.status_code == 200:
        print ("Accessed Chocolatier Page")
        soup = BeautifulSoup(r.content, 'html.parser')
        
        brand_description = soup.find('div', {'class': 'sc-53654036-0 sc-733f3dab-1 bJugGc jdqFcO'})
        print(brand_description)
        print(brand_description.text.strip())
        #The text stripped version is exactly what we want to save. 
        
        """
        So all the brand info is output into a large text chunk. Parsing this text chunk
        intentionally is probably the best bet. Have a set list of data we know we would like to 
        extract from this site and check to see if the text chunk contains it. They will always have the 
        format "keyword": ______ where the underline implies the information we are seeking. 
        """
        info = soup.find('script', {'id': '__NEXT_DATA__'})
        #print(info)
        print(info.text.strip())
        

def scrape_brand_info(brand):
    #Will need to parse brand name either before or after. It should be all lowercase with -s between words
    r = get(f'https://thingtesting.com/brand/{brand}/info')
    if r.status_code == 200:
        print("Accessed brand page")
        soup = BeautifulSoup(r.content, 'html.parser')
        
        #This is finding the category names
        brand_description = soup.find('div', {'class': 'sc-53654036-0 sc-733f3dab-1 bJugGc jdqFcO'})
        #Do a .text.strip()?
        print(brand_description)
    else:
        print("failed to access brand page")
        print(brand)



def scrape_thingtesting_by_category(categories):
    #Could run a while 404 vs while 200 in order to guarantee success
    #Here we want to grab brand names and pass on the brand names to scrape_brand_info 
    for category in categories: 
        r = get(f"https://thingtesting.com/categories/{category}")
        if r.status_code == 200:
            print ("accessed site")
            soup = BeautifulSoup(r.content, 'html.parser')
            #brands = soup.find_all()
        else:
            print ("did not access site")

"""
Categories pages obfuscates the list of categories. May not be as useful timewise to figure out.
"""

def scrape_category_names():
    url = 'https://thingtesting.com/categories'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)
        
        #The main problem is the information I want is hidden. This should be grabbing the relevant info.
        correct_category = soup.find_all('a', {'class': 'sc-14fdfd51-0 eDFusO'})
        print(correct_category)
        return correct_category

"""
Here I am envisioning no trailing whitespace characters. I just want to take in strings that 
represent brands / categories and to return the url-style format. This should be the string with 
no trailing whitespace wherein all whitespace within the string is converted to dashes and the entire
string is lowercase. 
"""
def text_converter(string):
    new_string = string.lower()
    new_string.replace(" ", "-")
    return string

scrape_brand_info_test()       
#categories = scrape_category_names()
#scrape_thingtesting_by_category(categories)




