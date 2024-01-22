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
Need to make storage container (done) + catch edge cases (need to parse brands for correct link name)
Need to make storage container compatible with thingtesting's container
"""

"""
This is a  function for scraping the brand info from a specific site. 
The sections so far can be 
    [Brand Name, url, Brand Description, Sectors (categories in Thing Test), Incorporated (Founded in thingTest),  Headquarters, News Articles, Milestone News Articles, Awards]
"""
def scrape_brand_info(brand):
    print("Trying to scrape brand info for: " + brand)
    #If the brand contains a . the link will break
    #We know if we havent found the brand because the brand description will be the homepage 
    if brand == "":
        return
    if '.' in brand:
        return
    r = get(f'https://www.venturelab.swiss/{brand}')
    brand_url = "https://www.venturelab.swiss/" + brand
    if r.status_code == 200:
        print("Successfully accessed website. ")
        soup = BeautifulSoup(r.content, 'html.parser')
        section_data = soup.find_all('div', {'class': 'vl-startup-sidebar-section-data'})
        incorporated = ""
        headquarters = ""
        section_data_str = ""
        for section in section_data:
            section_data_str = section_data_str + section.text.strip() + " "
        if not section_data_str == "":
            #This raw split is not always going to work. Have to actually parse this to ensure as not every company has both pieces of data. 
            section_data_split = section_data_str.split(" ")
            incorporated = section_data_split[0]
            headquarters = section_data_split[1]
            #Need to check for Incorporated: and Headquarter:]
            print(incorporated)
            if incorporated[0:12] == "Incorporated":
                print("Found the incorporated section")
                print(incorporated[12:])

        categories = soup.find_all('div', {'class': 'vl-tags'})
        categories_str = ""
        for category in categories:
            categories_str = category.text.strip()
        categoryies_split = categories_str.split('\n')
        categories_str = ""
        for word in categoryies_split:
            categories_str = categories_str + word + ", "
            
        #If description = the line below we did not access the correct page for this brand.
        default_text = "Upcoming Events Since 2004, Venturelab has been designing and operating flagship startup programs to support the best entrepreneurial talents in Switzerland, including Venture Kick, Venture Leaders, the TOP 100 Swiss Startup Award, and Innosuisse Start-up Trainings. Together with successful founders, top academic collaborators, and leading industry partners, we support the best startups on their way to success."

        brand_description = (soup.find('p').text.strip())
        if not brand_description: brand_description = "Description Not Found"
        brand_description = brand_description.replace("\r","")
        brand_description = brand_description.replace("\n","")
        if brand_description == default_text:
            return
        
        brand_blurb = soup.find('h3').text.strip()
        if not brand_blurb: brand_blurb = "Blurb Not Found"
        
        news_articles = soup.find_all('li', {'name': 'vl-hidden-news-article'})
        j = 0
        news_articles_str = ""
        for article in news_articles:
            if not j == 0: news_articles_str = article.text.strip() + "| "
            else: j = 1 
        
        milestone_news_articles = soup.find_all('li', {'name': 'vl-hidden-milestones-article'})
        milestone_news_list = ""
        j = 0
        for article in milestone_news_articles:
            if not j == 0: milestone_news_list = milestone_news_list + article.text.strip() + "| "
            else: j =1

        awards = soup.find_all('div', {'class': 'vl-startup-sidebar-section-links'})
        award_list = ""
        award_list_str = ""
        for award in awards:
            award_list_str =  award.text.strip() 
        award_list_split = award_list_str.split('\n')
        for award in award_list_split:
            award_list = award_list + award + "|  "
        
        
        linkedin = ""
        count = 0
        for tag in soup.find_all('li', {'class': 'linkedin'}):
            if count == 0:
                for anchor in tag.find_all('a'): linkedin = anchor['href']
            count +=1
        if not linkedin: linkedin = "Not Found"
        if linkedin == "https://www.linkedin.com/company/venturelab/": linkedin = "Not Found"
        print(linkedin)
        
        brand_website = ""
        count = 0
        for tag in soup.find_all('li', {'class': 'home'}):
            if count == 0:
                for anchor in tag.find_all('a'): brand_website = anchor['href']
            count +=1
        if not brand_website: brand_website = "Not Found"
        print(brand_website)
        
        entry = [brand, brand_url, brand_blurb, brand_description, categories_str, incorporated, headquarters, linkedin, brand_website, news_articles_str, milestone_news_list, award_list]
        return entry

"""
This is how we will scrape the homepage. We can succesfully access all 39 pages. 
"""
def scrape_homepage_venturelab():
    brand_holder = set()
    print("Trying to scrape brands from the homepage")
    #First_Num should actually be page to start on. Second 
    first_num = 1
    second_num = 1
    for i in range(1,37):
        r = get(f'https://www.venturelab.swiss/index.cfm?cfid=99481193&cftoken=495ae4e2be858b0a-C0196F1C-0665-64DE-F31E4CCE4EEAAA42&bericht_id=9735&start_liste_9735={first_num}&bericht_seite_9735={second_num}&page=137241#fgBerichtAnker_9735')
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            names = soup.find_all('h3')
            for name in names:
                name_as_string = name.text.strip()
                all_words = name_as_string.split(" ")
                brand_holder.add(all_words[0])
        first_num = first_num + 21
        second_num = second_num +1
    return brand_holder
     
df = pd.DataFrame(columns = ["Brand Name", "Brand Url","Brand Blurb", "Brand Description", "Categories", "Founded",  "Headquarters", "LinkedIn", "Brand Website", "News Articles", "Milestone News Articles", "Awards"]) 
brands = scrape_homepage_venturelab()
for brand in brands:
    entry = scrape_brand_info(brand)
    df.loc[len(df)] = entry
   





