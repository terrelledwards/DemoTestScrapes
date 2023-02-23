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
        May want to export the results of classification_categories to a set to exclude double information then
        pass that set into a function that will iterate over it and store the relevant data in a pandas dataframe
"""
 #Could run while 404 vs while 200 in order to guarantee success

def scrape_brand_info_test():
    #r = get('https://thingtesting.com/brands/flair-chocolatier/info')
    r = get('https://thingtesting.com/brands/motif/info')
    #Have tested on multiple different sources. As long as the brand name is correctly divided up, the general form should work
    if r.status_code == 200:
        print ("Accessed Test Page")
        soup = BeautifulSoup(r.content, 'html.parser')
        
        brand_description = soup.find('div', {'class': 'sc-53654036-0 sc-733f3dab-1 bJugGc jdqFcO'})
        #print(brand_description)
        print("Brand description: " + brand_description.text.strip())
        #The text stripped version is exactly what we want to save. 
        
        """
        So all the brand info is output into a large text chunk. Parsing this text chunk
        intentionally is probably the best bet. Have a set list of data we know we would like to 
        extract from this site and check to see if the text chunk contains it. They will always have the 
        format "keyword": ______ where the underline implies the information we are seeking. 
        """
        info = soup.find('script', {'id': '__NEXT_DATA__'})
        print(info)
        print(" ")
        print(" ")
        print(" ")
        
        categories_for_classifying = soup.find_all('div', {'class': 'sc-577b0f44-0 cqqtMQ'})
        for i in range (0, len(categories_for_classifying)):
            print(categories_for_classifying[i].text.strip())
        #Text stripping doesnt help nearly as much here. 
        #print(info.text.strip())
        

def scrape_brand_info(brand):
    #Will need to parse brand name either before or after. It should be all lowercase with -s between words
    #can use a call to text-converter to get a url-style brand name
    brand_info = set()
    r = get(f'https://thingtesting.com/brands/{brand}/info')
    if r.status_code == 200:
        print("Accessed brand page")
        soup = BeautifulSoup(r.content, 'html.parser')
        print("This is the brand we are working with currently: " + brand)
        #This is finding the category names
        """
        brand_description = soup.find('div', {'class': 'sc-53654036-0 sc-733f3dab-1 bJugGc jdqFcO'})
        if(brand_description == None):
            print("There is no brand description")
        else:
            print(brand_description.text.strip())
        """
        classification_categories = soup.find_all('div', {'class': 'sc-577b0f44-0 cqqtMQ'})
        #This outputs the same information twice
        for i in range(0, len(classification_categories)):
            print("Accessing brand info for " + brand)
            """
            print(classification_categories[i].text.strip())
            print(" ")
            print(" ")
            print(" ")
            """
            brand_info.add(classification_categories[i].text.strip())
    else:
        print("failed to access brand page")
        print(brand)
    return brand_info

"""
This is just a test function like scrape_brand_info_test. There was a problem of scrape_thingtesting_by_category
not actually scraping the individual category pages, but the homepage. This should be fixed by the function that 
converts the category names into their url format. 
"""
def scrape_thingtesting_by_category_test():
    category = "pets"
    category_two = "skin-care"
    
    r = get("https://thingtesting.com/categories/pets")
    if r.status_code == 200:
        print("Successfully accessed " + category + " page")
        soup = BeautifulSoup(r.content, 'html.parser')
        brands = soup.find_all('a', {'class': 'sc-cd075a2b-5 fNlBic'})
        for i in range(0, len(brands)):
            print(brands[i].text.strip())
    
    r_2 = get("https://thingtesting.com/categories/skin-care")
    if r_2.status_code == 200:
        print("successfully accessed "+ category_two + " page")
        soup_two = BeautifulSoup(r_2.content, 'html.parser')
        brands_two = soup_two.find_all('a', {'class': 'sc-cd075a2b-5 fNlBic'})
        for j in range (0, len(brands_two)):
            print(brands_two[j].text.strip())

#maybe like above it may be useful to play around with getting scrape by categories to work in a test case
def scrape_thingtesting_by_category(categories):
    brand_holder = set()
    #Here we want to grab brand names and pass on the brand names to scrape_brand_info 
    for category in categories: 
        #If the category does not exist it will redirect to the homepage
        #print("Curr category: " + category)
        curr_category = text_converter_categories(category)
        r = get(f"https://thingtesting.com/categories/{curr_category}")
        if r.status_code == 200:
            print ("Accessing current category page: " + category)
            soup = BeautifulSoup(r.content, 'html.parser')
            #print(soup.prettify())
        
            brands = soup.find_all('a', {'class': 'sc-cd075a2b-5 fNlBic'})
            for i in range(0, len(brands)):
                #print(brands[i].text.strip())
                brand_holder.add(brands[i].text.strip())
        else:
            print ("Did not access site")
    return brand_holder

"""
Categories pages obfuscates the list of categories. May not be as useful timewise to figure out.
Instead of using the /categories page I am instead going to scrape the lead categories from the homepage.
This will lead to less specific results than what is possible, but should still cover all the companies
as the homepage categories are just a more general list. 
"""
#This is successfully outputing
def scrape_category_names():
    category_holder = []
    url = 'https://thingtesting.com'
    #url = 'https://thingtesting.com/categories'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        #print("Accessed homepage. Attemtping to grab categories.")
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
    #print("Converting brand name to url style")
    #print(string)
    new_string = string.lower()
    new_string = new_string.replace(' ', '-')
    #print(new_string)
    return new_string

def text_converter_categories(string):
    new_string = string.lower()
    new_string = new_string.replace('&', 'and')
    new_string = new_string.replace(' ', '-')
    return new_string

df = pd.DataFrame(columns = ["Categories", "Ships to", "Founded", "Launched", "Headquarters", "Founders", "Founder Attributes"])
print(" ")
print(" ")
print(" ")      
categories = scrape_category_names()
print(" ")
print(" ")
print(" ")
#print(categories)
#print(" ")
#print(" ")
#print(" ")
#The method below really ought to return brand names as the method above returned categories
brands = scrape_thingtesting_by_category(categories)
print(brands)

#The generalized version of the method below ought to return a pandas dataframe with possible entry values for all the relevant text we could get from a brands info page
#scrape_brand_info_test() 
for brand in brands:
    curr_brand = text_converter_brand(brand)
    brand_info = scrape_brand_info(curr_brand)
    for val in brand_info:
        print(val)
    #Here is where we can parse the brand_info tab
    
#Finally, we can concatenate the data here by amalgamating the returned dataframes. 

#scrape_thingtesting_by_category_test()
#scrape_brand_info_test()
