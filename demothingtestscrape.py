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
import re

"""
Feedback :
    Add brand descriptions 
Things to do: 
    1) Check on edge cases. There are a few companies with abnormal names (arc'teryx, dr. jort+, etc.) that may require changes
        to how brand names are processed after scraping before accessing the speciifc brand page for scraping
        Check if these apply in all cases:
            & --> and? 
            all other special characters dropped? (., ', !, @, _, +, *)
            accent marks dropped? éo
            remove underscores
            
            Manisafe London--> Has London dropped from url
            sole footwear--> Has footwear dropped from url
"""

def scrape_brand_info_test():
    r = get('https://thingtesting.com/brands/flair-chocolatier/info')
    #r = get('https://thingtesting.com/brands/casper/info')
    #Have tested on multiple different sources. As long as the brand name is correctly divided up, the general form should work
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')     
        brand_description = soup.find('div', {'class': 'sc-53654036-0 sc-733f3dab-1 bJugGc jdqFcO'})
        categories_for_classifying = soup.find_all('div', {'class': 'sc-577b0f44-0 cqqtMQ'})
        for i in range (0, len(categories_for_classifying)):
            print(categories_for_classifying[i].text.strip())

def scrape_brand_description(brand):
    return_string = ""
    r = get(f'https://thingtesting.com/brands/{brand}/info')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        brand_description = soup.find('div', {'class': 'sc-53654036-0 sc-733f3dab-1 bJugGc jdqFcO'})
        if not brand_description:
            return_string = "There is no brand description"
        else:
            return_string = brand_description.text.strip()
    return return_string

def scrape_brand_info(brand):
    brand_info = set()
    r = get(f'https://thingtesting.com/brands/{brand}/info')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        classification_categories = soup.find_all('div', {'class': 'sc-577b0f44-0 cqqtMQ'})
        #This outputs the same information twice that is why it ought to be stored in a set
        for i in range(0, len(classification_categories)):
            brand_info.add(classification_categories[i].text.strip())
    else:
        #Here we return an empty set so we can either check for the edge cases here or in the function that calls it or do it manually
        print("failed to access brand page")
        print(brand)
    return brand_info
    
def scrape_thingtesting_by_category(categories):
    brand_holder = set()
    #Here we want to grab brand names and pass on the brand names to scrape_brand_info 
    for category in categories: 
        #print("Curr category: " + category)
        curr_category = text_converter_categories(category)
        r = get(f"https://thingtesting.com/categories/{curr_category}?o=added")
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            brands = soup.find_all('a', {'class': 'sc-cd075a2b-5 fNlBic'})
            for i in range(0, len(brands)):
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
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        categories = soup.find_all('button', {'class': 'sc-de770ae-0 efXhIH sc-70c1ce0d-0 iqVlCd'})
        for i in range(0, len(categories)):
            category_holder.append(categories[i].text.strip())
        return category_holder

"""
Here I am envisioning no trailing whitespace characters. I just want to take in strings that 
represent brands / categories and to return the url-style format. This should be the string with 
no trailing whitespace wherein all whitespace within the string is converted to dashes and the entire
string is lowercase. 
"""
def text_converter_brand(string):
    print(string)
    new_string = string.lower()
    new_string = new_string.replace(' ', '-')
    new_string = new_string.replace('&', 'and') 
    new_string = new_string.replace('_', '-')
    print(new_string)
    return new_string

def text_converter_categories(string):
    new_string = string.lower()
    new_string = new_string.replace('&', 'and')
    new_string = new_string.replace(' ', '-')
    return new_string

def seperate_words(brand_list):
    res = [re.sub(r"(\w)([A-Z])", r"\1 \2", ele) for ele in brand_list]
    return res

def list_to_string(list):
    return_val = ""
    for val in list:
        return_val += ' ' + val
    return return_val

def scrape_thing_testing():
    df = pd.DataFrame(columns = ["Brand Name", "Brand Url", "Brand Description", "Categories", "Founded", "Ships to", "Launched", "Headquarters", "Founders", "Founder Attributes", "Certifications"]) 
    for brand in brands:
        #to_be_added = []
        curr_brand = text_converter_brand(brand)
        brand_info = scrape_brand_info(curr_brand)
        brand_description = scrape_brand_description(curr_brand)
        brands_as_list = list(brand_info)
        brand_info_seperated = seperate_words(brands_as_list)
        brand_url = "https://thingtesting.com/brands/" + curr_brand + "/info"
        #for val in brand_info:
        #    print(val)
        categories, founded, shipping_locations, launch_date, headquarters_loc, founders, founder_attrs, certs = ("", "", "", "", "", "", "", "")
        for val in brand_info_seperated:
            all_words = val.split(" ")
            if(all_words[0] == "Category"): categories = list_to_string(all_words[1:])
            elif(all_words[0] == "Categories"): categories = list_to_string(all_words[1:])
            elif(all_words[0][0:7] == "Founded"):
                if(len(all_words[0]) > 7):
                    founded = list_to_string(all_words[0][7:])
                else:
                    founded = list_to_string(all_words[1:])
            elif(all_words[0] == "Ships"): shipping_locations = list_to_string(all_words[1:])
            elif(all_words[0] == "Launched"): launch_date = list_to_string(all_words[1:])
            elif(all_words[0] == "Headquarters"): headquarters_loc = list_to_string(all_words[1:])      
            elif(all_words[0] == "Founder"):
                if(all_words[1] == "attributes"):
                    founder_attrs = list_to_string(all_words[2:])
                else: 
                    founders = list_to_string(all_words[1:])     
            elif(all_words[0] == "Founders"):
                if(all_words[1] == "attributes"):
                    founder_attrs = list_to_string(all_words[2:])
                else: 
                    founders = list_to_string(all_words[1:])     
            elif(all_words[0] == "Certifications"): certs = list_to_string(all_words[1:])
        #When the vals are empty this really screws up...have to figure out a workaround for entering blank values. Probably a "Not Found" type deal.
        if not categories: categories = "Not Found"
        if not founded: founded = "Not Found"
        if not shipping_locations: shipping_locations = "Not Found"
        if not launch_date: launch_date = "Not Found"
        if not headquarters_loc: headquarters_loc = "Not Found"
        if not founders: founders = "Not Found"
        if not founder_attrs: founder_attrs = "Not Found"
        if not certs: certs = "Not Found"
      
        final_row = [curr_brand, brand_url, brand_description, categories, founded, shipping_locations, launch_date, headquarters_loc, founders, founder_attrs, certs]
        df.loc[len(df)] = final_row
    return df

categories = scrape_category_names()
brands = scrape_thingtesting_by_category(categories)
df = scrape_thing_testing()

#scrape_brand_info_test()

