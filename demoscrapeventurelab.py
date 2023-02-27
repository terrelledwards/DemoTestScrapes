#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 21:09:26 2023

@author: tedwards
"""

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata, unidecode
import re

"""
This is just a tester function for scraping the brand info from a specific site. 
The sections so far can be 
    [Brand Name, url, Brand Description, Sectors (categories in Thing Test), Incorporated (Founded in thingTest),  Headquarters, News Articles, Milestone News Articles, Awards]
"""
def scrape_brand_info(brand):
    print("Trying to scrape brand info for: " + brand)
    r = get(f'https://www.venturelab.swiss/{brand}')
    if r.status_code == 200:
        print("Successfully accessed website. ")
        soup = BeautifulSoup(r.content, 'html.parser')
        #This is a list of overarching information
        print(" ")
        print(" ")
        print("Section Data")
        section_data = soup.find_all('div', {'class': 'vl-startup-sidebar-section-data'})
        for section in section_data:
            print(section.text.strip())
        #This is a list of categories
        print(" ")
        print(" ")
        print("Categories")
        categories = soup.find_all('div', {'class': 'vl-tags'})
        for category in categories:
            print(category.text.strip())
        #this is the brand description
        print(" ")
        print(" ")
        print("Brand Description")
        print(soup.find('p').text.strip())
        print(" ")
        print(" ")
        print("News Articles")
        news_articles = soup.find_all('li', {'name': 'vl-hidden-news-article'})
        for article in news_articles:
            print(article.text.strip())
        print(" ")
        print(" ")
        print("Milestone News Articles")
        milestone_news_articles = soup.find_all('li', {'name': 'vl-hidden-milestones-article'})
        for article in milestone_news_articles:
            print(article.text.strip())
        print(" ")
        print(" ")
        print("Awards")
        awards = soup.find_all('div', {'class': 'vl-startup-sidebar-section-links'})
        for award in awards:
            print(award.text.strip())

"""
This is how we will scrape the homepage. We can succesfully access all 39 pages. 
"""
def scrape_homepage_venturelab():
    brand_holder = set()
    print("Trying to scrape brands from the homepage")
    #r = get('https://www.venturelab.swiss/startups')
    first_num = 1
    second_num = 1
    #Here we can just lower the range to scrape a lower number of pages. Total num of pages is 39 as of 2/27
    for i in range(1,39):
        #print("")
        r = get(f'https://www.venturelab.swiss/index.cfm?cfid=99481193&cftoken=495ae4e2be858b0a-C0196F1C-0665-64DE-F31E4CCE4EEAAA42&bericht_id=9735&start_liste_9735={first_num}&bericht_seite_9735={second_num}&page=137241#fgBerichtAnker_9735')
        if r.status_code == 200:
            #print("Successfully accessed homepage. ")
            soup = BeautifulSoup(r.content, 'html.parser')
            #print(" ")
            #print(" ")
            #print("Company Names")
            names = soup.find_all('h3')
            for name in names:
                #print(name.text.strip())
                name_as_string = name.text.strip()
                all_words = name_as_string.split(" ")
                #print(all_words[0])
                brand_holder.add(all_words[0])
        first_num = first_num + 21
        second_num = second_num +1
    return brand_holder

#scrape_brand_info_test()
brands = scrape_homepage_venturelab()
print(brands)
for brand in brands:
    print(brand)
    scrape_brand_info(brand)
    






