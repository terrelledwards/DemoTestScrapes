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
Things to do: 
    1) Make a function that takes in a string and returns the string all lowercase with - in all whitespace
    2) Extraction of relevant data from scrape (from brand scrape + scrape by category) —both are working to an extent
        Scrape by Category seems to have an issue with link redirection versus links when clicking around
        Scrape by Brand needs a method for extracting all the info we want from the text chunk that was scraped
    3) Extraction of relevant data from scrape results
        This is cleaning up everything for final entry into a pandas dataframe which can be converted to a csv
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
        #Text stripping doesnt help nearly as much here. 
        print(info.text.strip())
        

def scrape_brand_info(brand):
    #Will need to parse brand name either before or after. It should be all lowercase with -s between words
    #can use a call to text-converter to get a url-style brand name
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



#maybe like above it may be useful to play around with getting scrape by categories to work in a test case
def scrape_thingtesting_by_category(categories):
    #Could run a while 404 vs while 200 in order to guarantee success
    #Here we want to grab brand names and pass on the brand names to scrape_brand_info 
    for category in categories: 
        #If the category does not exist it will redirect to the homepage
        print("Curr category: " + category)
        r = get(f"https://thingtesting.com/categories/{category}?f=current-user-unreviewed-brands")
        if r.status_code == 200:
            print ("Accessed categories page")
            soup = BeautifulSoup(r.content, 'html.parser')
            #print(soup.prettify())
        
            brands = soup.find_all('a', {'class': 'sc-cd075a2b-5 fNlBic'})
            for i in range(0, len(brands)):
                print(brands[i].text.strip())
        else:
            print ("Did not access site")

"""
Categories pages obfuscates the list of categories. May not be as useful timewise to figure out.
Instead of using the /categories page I am instead going to scrape the lead categories from the homepage.
This will lead to less specific results than what is possible, but should still cover all the companies
as the homepage categories are just a more general list. 
"""

def scrape_category_names():
    category_holder = []
    url = 'https://thingtesting.com'
    #url = 'https://thingtesting.com/categories'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        print("Accessed homepage. Attemtping to grab categories.")

        #This is successfully outputing 
        categories = soup.find_all('button', {'class': 'sc-de770ae-0 efXhIH sc-70c1ce0d-0 iqVlCd'})
        #This outputs the correct category names. From this, we need to just store a list of all the names.
        for i in range(0, len(categories)):
            #print(categories[i].text.strip())
            category_holder.append(categories[i].text.strip())
        
        
        return category_holder

"""
Here I am envisioning no trailing whitespace characters. I just want to take in strings that 
represent brands / categories and to return the url-style format. This should be the string with 
no trailing whitespace wherein all whitespace within the string is converted to dashes and the entire
string is lowercase. 
"""
def text_converter_brand(string):
    new_string = string.lower()
    new_string.replace(" ", "-")
    return string


print(" ")
print(" ")
print(" ")      
categories = scrape_category_names()
print(" ")
print(" ")
print(" ")
print(categories)
#The method below really ought to return brand names as the method above returned categories
scrape_thingtesting_by_category(categories)

#The generalized version of the method below ought to return a pandas dataframe with possible entry values for all the relevant text we could get from a brands info page
#scrape_brand_info_test() 

#Finally, we can concatenate the data here by amalgamating the returned dataframes. 

