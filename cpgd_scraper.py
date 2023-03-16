#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 09:25:38 2023

@author: tedwards
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata, unidecode
import re

def scrape_cpgd():
    print("This is the full scrape. ")
    df = pd.DataFrame(columns = ["Brand Name", "Brand Url", "Brand Description", "Categories", "Headquarters", "LinkedIn"])
    categories = scrape_category_names()
    brands = scrape_brand_names_by_category(categories)
    #We can just call scrape_new_brands here to do just that

    for brand in brands:
        brand_info = scrape_brand_info(brand)
        df.loc[len(df)] = brand_info
    return df

def scrape_brand_info(brand):
    brand_key = text_converter_brand(brand)
    brand_url = "https://www.cpgd.xyz/brand/" + brand_key
    r = get(f'https://www.cpgd.xyz/brands/{brand_key}')
    if r.status_code == 200:
        print("Accessed Brand Page for: " + brand)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        info_headers = soup.find_all('div', {'class': 'brand__detail-block'})
        location = info_headers[0].text.strip()[5:]
        
        if not location: location = "Not Found"
        sub_cat = info_headers[2].text.strip()[13:]
        category = soup.find('div', {'class': 'text-medium brand__filed'}).text.strip()
        if sub_cat: category = category + ": " + sub_cat
        
        description = soup.find('div', {'class': 'text-large brand__sus-typo'}).text.strip()
        
        count = 0
        linkedin = ""
        for brand_socials in soup.find_all('div', {'class': 'w-layout-grid brand__socials-wrap'}):
            for link in brand_socials.find_all('a'):
                if count == 2: linkedin = link['href']
                count += 1
        if linkedin == "#": linkedin = "Not Found"
        return [brand, brand_url, description, category, location, linkedin]

def scrape_brand_names_by_category(categories):
    brand_holder = set()
    for category in categories:
        curr_category = text_converter_categories(category)
        r = get(f'https://www.cpgd.xyz/brands?brand-categories={curr_category}')
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            brands = soup.find_all('div', {'class': 'hero-head brands__product-name'})
            for brand in brands: brand_holder.add(brand.text.strip())
    return brand_holder

def scrape_category_names():
    category_holder = set()
    r = get('https://www.cpgd.xyz/brands')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        categories = soup.find_all('div', {'class': 'text-size-6'})
        for category in categories: category_holder.add(category.text.strip())
    return category_holder

"""
After scraping the site, only the new additions (which are updated weekly) need to be scraped
"""
def scrape_new_brand_names():
    brand_holder = set()
    r = get('https://www.cpgd.xyz/')
    if r.status_code == 200:
        print("Accessed site. ")
        soup = BeautifulSoup(r.content, 'html.parser')
        brands = soup.find_all('h3', {'class': 'heading-large'})
        for brand in brands: brand_holder.add(brand.text.strip())

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

df = scrape_cpgd()




















