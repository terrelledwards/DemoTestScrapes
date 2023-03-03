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
        #This is a list of overarching information
        
        #print(" ")
        #print(" ")
        #print("Section Data")
        section_data = soup.find_all('div', {'class': 'vl-startup-sidebar-section-data'})
        incorporated = ""
        headquarters = ""
        section_data_str = ""
        for section in section_data:
            #print(section.text.strip())
            section_data_str = section_data_str + section.text.strip() + " "
        if not section_data_str == "":
            #This raw split is not always going to work. Have to actually parse this to ensure as not every company has both pieces of data. 
            section_data_split = section_data_str.split(" ")
            incorporated = section_data_split[0]
            headquarters = section_data_split[1]
        #print("Section data as string: " + section_data_str)
        #print("Incorporated: " + incorporated)
        #print("Headquarters: " + headquarters)
                
            #Need to check for Incorporated: and Headquarter:
        #This is a list of categories
        #print(" ")
        #print(" ")
        #print("Categories")
        categories = soup.find_all('div', {'class': 'vl-tags'})
        categories_str = ""
        for category in categories:
            #print(category.text.strip())
            categories_str = category.text.strip()
            #Store all in one string thats just concatenated with commas
        categoryies_split = categories_str.split('\n')
        categories_str = ""
        for word in categoryies_split:
            #print("This is a category: " + word)
            categories_str = categories_str + word + ", "
            #We can outsource a function to turn this into a bunch of commas 
        #print(categories_str)
        
        #this is the brand description
        print(" ")
        print(" ")
        print("Brand Description")
        brand_description = (soup.find('p').text.strip())
        if not brand_description:
            print("Did not find brand description for: " + brand)
            brand_description = "Description Not Found"
        print(brand_description)
        brand_description = brand_description.replace("\r","")
        brand_description = brand_description.replace("\n","")
        
        brand_blurb = soup.find('h3').text.strip()
        if not brand_blurb:
            print("Could not find brand_blurb.")
            brand_blurb = "Blurb Not Found"
        print(" ")
        print(" ")
        print("Brand Blurb")
        print(brand_blurb)
        """
        If description = the line below we did not access the correct page for this brand.
        Upcoming Events Since 2004, Venturelab has been designing and operating flagship startup programs to support the best entrepreneurial talents in Switzerland, including Venture Kick, Venture Leaders, the TOP 100 Swiss Startup Award, and Innosuisse Start-up Trainings. Together with successful founders, top academic collaborators, and leading industry partners, we support the best startups on their way to success.
        """
        
        """
        The News articles follow a format of title followed by date + article header repeated. 
        We want to disregard the title, but save the data, articles pairs as chunks within a string.
        Maybe a counter where 0 is title followed by odd for dates and even for article headers is sensibl
        """     
        
        
        #print(" ")
       # print(" ")
        #print("News Articles")
        news_articles = soup.find_all('li', {'name': 'vl-hidden-news-article'})
        j = 0
        news_articles_str = ""
        for article in news_articles:
            if not j == 0: news_articles_str = article.text.strip() + "| "
            else: j = 1 
       # print(news_articles_str)
        
        
        #print(" ")
        #print(" ")
        #print("Milestone News Articles")
        milestone_news_articles = soup.find_all('li', {'name': 'vl-hidden-milestones-article'})
        milestone_news_list = ""
        j = 0
        for article in milestone_news_articles:
            if not j == 0: milestone_news_list = milestone_news_list + article.text.strip() + "| "
            else: j =1
        #print(milestone_news_list)
        
        #print(" ")
        #print(" ")
        #print("Awards")
        awards = soup.find_all('div', {'class': 'vl-startup-sidebar-section-links'})
        award_list = ""
        award_list_str = ""
        for award in awards:
            #print(award.text.strip())
            award_list_str =  award.text.strip() 
        award_list_split = award_list_str.split('\n')
        for award in award_list_split:
            award_list = award_list + award + "|  "
        
        #print(award_list)
        
        #entry = [brand, brand_url, brand_info, categories_str, incorporated, headquarters, news_articles_str, milestone_news_list, award_list]
        entry = [brand, brand_url, brand_blurb, brand_description, categories_str, incorporated, headquarters, news_articles_str, milestone_news_list, award_list]
        return entry

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
     
def scrape_brand_description_test(brand):
    if brand == "":
        return
    if '.' in brand:
        return
    r = get(f'https://www.venturelab.swiss/{brand}')
    #r = get('https://www.venturelab.swiss/Biopsomic')
    if r.status_code == 200:
        print("Successfully accessed website. ")
        soup = BeautifulSoup(r.content, 'html.parser')
        print(" ")
        print(" ")
        print("Brand Description")
        brand_description = (soup.find('p').text.strip())
        if not brand_description:
            print("Did not find brand description for: " + brand)
            brand_description = "Description Not Found"
        print(brand_description)
        brand_description = brand_description.replace("\r","")
        brand_description = brand_description.replace("\n","")
        entry = [brand, brand_description]
        return entry
     
#df = pd.DataFrame(columns = ["Brand Name", "Brand Url", "Brand Description", "Categories", "Founded",  "Headquarters", "News Articles", "Milestone News Articles", "Awards"]) 
df = pd.DataFrame(columns = ["Brand Name", "Brand Url","Brand Blurb", "Brand Description", "Categories", "Founded",  "Headquarters", "News Articles", "Milestone News Articles", "Awards"]) 
#scrape_brand_info_test()

brands = scrape_homepage_venturelab()
print(brands)
for brand in brands:
    print(brand)
    #scrape_brand_info(brand)
    entry = scrape_brand_info(brand)
    df.loc[len(df)] = entry





