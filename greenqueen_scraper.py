#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 15:32:25 2023

@author: tedwards
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata, unidecode
import re
from urllib.request import Request, urlopen

"""
Will have to access website. 
Access all links to articles.
Scrape each article. 

"""

categories = set({"vegan", "climate-change-asia", "food-tech-alt-protein-asia", "cellbased-protein-cultivated-meat",
                 "fermented-foods", "zero-waste-hong-kong", "fashion", "eco-lifestyle"})

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

def scrape_greenqueen_by_topic(category):
    links_to_topics = set()
    r = requests.get(f'https://www.greenqueen.com.hk/category/{category}/', headers=HEADERS)
    #print(r.text)
    #print(r.status_code)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        topics = soup.find_all('p', {'class': 'title'})
        for topic in topics:
            for anchor in topic.find_all('a'):
                curr_topic_link = anchor['href']
                #curr_topic = anchor.text.strip()
                print(curr_topic_link)
                links_to_topics.add(curr_topic_link)
        print("  ")
        print("  ")
    return links_to_topics

def scrape_greenqueen_article(article_link):
    article_in_chunks
    
count = 0
for category in categories:
    print(category)
    links_to_topics = scrape_greenqueen_by_topic(category)
    #if count >=1: break
    count +=1 



