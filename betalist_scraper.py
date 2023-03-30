#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:02:40 2023

@author: tedwards
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata, unidecode
import re

def betalist_brand_info_scrape(brand_directory):
    #df = pd.DataFrame(columns= ["Brand Name", "Brand Url", "Brand Description", "Brand Blurb", "Categories", "Founder", "Location", "Debut on Site"])
    df = pd.DataFrame(columns = ["Brand Name", "Brand Url", "Brand Description", "Brand Blurb", "Founder", "Categories", "Location"])
    for brand_link in brand_directory:
        r = get(f'https://betalist.com{brand_link}')
        brand_url = "https://betalist.com" + brand_link
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            brand_name = soup.find('h1', {'class': 'startup__summary__name'}).text.strip()
            brand_blurb = soup.find('h2', {'class': 'startup__summary__pitch'}).text.strip()
            
            #brand_description = soup.find('div', {'class': 'startup__description text-lg max-w-xl mx-auto mt-10 px-4 [&_p:not(:first-child)]:mt-4 [&_strong]:font-bold'}).text.strip()
            brand_description = ""
            for brand_des in soup.find_all('div', {'class': 'startup__description text-lg max-w-xl mx-auto mt-10 px-4 [&_p:not(:first-child)]:mt-4 [&_strong]:font-bold'}):
                count = 0
                for anchor in brand_des.find_all('p'):
                    if count == 0: brand_description = anchor.text.strip()
                    count +=1
            if not brand_description: brand_description = "Not Found"
            
            founder = soup.find('a', {'class': 'maker__name'})
            if not founder: founder = "Not Listed"
            else: founder = founder.text.strip()

            location = soup.find('div', {'class': 'gap-0'})
            if not location: location = "Not Listed"
            else: location = location.text.strip()
            
            category_list = ""
            categories = soup.find('div', {'class': 'flex gap-2 flex-wrap'})
            for anchor in categories.find_all('a'): 
                category_list = category_list + anchor.text.strip() + "|"
            brand_info = [brand_name, brand_url, brand_description, brand_blurb, founder, category_list, location]
            print(brand_name + " " + category_list + " " + brand_description)
            df.loc[len(df)] = brand_info
    return df

def betalist_brands_scrape(directory):
    brands_directory = set()
    brands = set()
    for topic in directory:
        r = get(f'https://betalist.com{topic}')
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            tags = soup.find_all('a', {'class': 'block whitespace-nowrap text-ellipsis overflow-hidden font-medium'})
            for tag in tags:
                #print(tag['href'])
                tagline = tag['href']
                brands.add(tagline[11:])
                brands_directory.add(tag['href'])
    return brands_directory, brands

def betalist_category_scrape():
    category_directory = set()
    categories = set()
    r = get('https://betalist.com/topics')
    if r.status_code == 200:
        print("Accessed site. ")
        soup = BeautifulSoup(r.content, 'html.parser')
        tags = soup.find_all('a', {'class': 'tag tag--card'})
        #count = 0
        for tag in tags:
            #if count == 2: break
            #print(tag['href'])
            tagline = tag['href']
            categories.add(tagline[8:])
            category_directory.add(tag['href'])
            #count +=1
    return category_directory, categories
        
directory, categories = betalist_category_scrape()
brand_directory, brands = betalist_brands_scrape(directory)
df = betalist_brand_info_scrape(brand_directory)