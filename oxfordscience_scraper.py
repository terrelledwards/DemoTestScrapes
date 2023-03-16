#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:13:57 2023

@author: tedwards
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata, unidecode
import re

def scrape_oxfordscience():
    df = pd.DataFrame(columns = ["Brand Name", "Brand Url", "Brand Description", "Categories",  "LinkedIn", "Founder", "Science Founder", "Founded", "Brand Website"])
    brands = scrape_brands()
    for brand in brands:
        brand_info = scrape_brand_info(brand)
        df.loc[len(df)] = brand_info
    return df

def scrape_brand_info(brand_path):
    brand_url = "https://www.oxfordscienceenterprises.com" + brand_path
    r = get(f'https://www.oxfordscienceenterprises.com{brand_path}')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        print("Accessed Brand Page. ")
        
        brand_name = soup.find('h1').text.strip()
        
        brand_info = soup.find_all('p')
        brand_website = brand_info[0].text.strip() #brand website
        brand_description = brand_info[1].text.strip() #brand description
        #print(brand_info[2].text.strip())
        
        linkedin = ""
        links = soup.find_all('a', {'title': 'LinkedIn'})
        for link in links:
            linkedin = link['href']
        if not linkedin: linkedin = "Not Found"
        

        count = 0
        category = ""
        founded = ""
        founder = ""
        science_founder = ""
        for brand in soup.find_all('dl', {'class': 'style_details__Qu2pX'}):
            for anchor in brand.find_all('dd'):
                if count == 0: category = anchor.text.strip()
                if count == 1: founded = anchor.text.strip()
                if count == 2: founder = anchor.text.strip()
                if count == 5: science_founder = anchor.text.strip()
                count += 1
        #print(category)
        #print(founded)
        #print(founder)
        #print(science_founder)                    
        return [brand_name, brand_url, brand_description, category, linkedin,founder, science_founder, founded, brand_website]

def text_converter_categories(string):
    new_string = string.lower()
    #new_string = new_string.replace('&', 'and')
    #new_string = new_string.replace(' ', '-')
    return new_string

def text_converter_brand(string):
    #print(string)
    new_string = string.lower()
    new_string = new_string.replace(' ', '-')
    new_string = new_string.replace('&', 'and') 
    new_string = new_string.replace('_', '-')
    new_string_final = re.sub("'!éä", "", new_string)
    #print(new_string_final)
    return new_string_final

def scrape_brands():
    brand_holder = set()
    r = get('https://www.oxfordscienceenterprises.com/portfolio')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        print("Accesed site. ")
        tags = soup.find_all('a', {'class': 'style_portfolioCard__dE6qU'})
        for tag in tags:
            #print(tag['href'])
            brand_holder.add(tag['href'])
    return brand_holder

df = scrape_oxfordscience()
