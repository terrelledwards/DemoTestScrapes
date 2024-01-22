#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 13:48:06 2023

@author: tedwards
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata, unidecode
import re


def failory_scrape():
    df = pd.DataFrame(columns = ["Fund Name", "Country", "City", "Founded", "Founders", "Industries", "Stages", "Min Check Size", "Max Check Size"])#, "Website", "Email"]) 
    r = get('https://www.failory.com/blog/pre-seed-venture-capital-firms')
    if r.status_code == 200:
        print("accessed site")
        soup = BeautifulSoup(r.content, 'html.parser')
        brand_names = soup.find_all('h3')
        brand_info = soup.find_all('ul', {'role': 'list'})
        brand_name_holder = []
        for i in range(0, len(brand_names)):
            brand_name_holder.append(brand_names[i].text.strip())
        tracker = 0
        #project_href = [i['href'] for i in soup.find_all('a', href=True)]
        #print(project_href)
        brand_website_holder = []
        brand_email_holder = []
        count = 0
        for link in soup.find_all('a', href=True):
            print(link['href'])
            if(count > 22 and count < 388):
                if(count % 2 == 1):
                    brand_website_holder.append(link['href'])
                else:
                    brand_email_holder.append(link['href'])
            count = count +1
            print(count)
        for brand in soup.find_all('ul'):
            brand_info = brand.find_all('li')
            country, city, founded, founders, industries, stages, first_min, first_max = ("", "", "", "", "", "", "", "")
            for i in range(0, len(brand_info)):
                split_phrase = brand_info[i].text.strip().split(":")
                if(split_phrase[0] == "City"):
                    city = split_phrase[1]
                elif(split_phrase[0] == "Country"):
                    country = split_phrase[1]
                elif(split_phrase[0] == "Started in"):
                    founded = split_phrase[1]
                elif(split_phrase[0] == "Founders"):
                    founders = split_phrase[1]
                elif(split_phrase[0] == "Industries"):
                    industries = split_phrase[1]
                elif(split_phrase[0] == "Stages"):
                    stages = split_phrase[1]
                elif(split_phrase[0] == "Minimum check size"):
                    first_min = split_phrase[1]
                elif(split_phrase[0] == "Maximum check size"):
                    first_max = split_phrase[1]

            entry = [brand_name_holder[tracker], country, city, founded, founders, industries, stages, first_min, first_max]#, brand_website_holder[tracker], brand_email_holder[tracker]]
            df.loc[len(df)] = entry
            tracker= tracker+1
        return df
            
df = failory_scrape()