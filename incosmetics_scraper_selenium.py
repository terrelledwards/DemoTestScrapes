#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 09:35:15 2023

@author: tedwards
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def scrape_directory():
    url_set = set()
    #driver.get('https://www.in-cosmetics.com/global/en-gb/exhibitor-directory.html#/')
    accept_cookies('https://www.in-cosmetics.com/global/en-gb/exhibitor-directory.html#/')
    driver.implicitly_wait(30)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 40);")
    time.sleep(10)
    """
    try:
        brand_urls = driver.find_elements(By.XPATH, "//a[@data-dtm='exhibitorDirectory_exhibitorName_bronze']")
        for brand in brand_urls:
            brand_url = brand.get_attribute('href')
            url_set.add(brand_url)
    except:
        url_set.add("Not Working")
    """    
    try:
        brand_names = driver.find_elements(By.XPATH, "//h3[@class='text-center-mobile wrap-word']")
        for brand in brand_names:
            print(brand.text.strip())
            brand_url = brand.find_element(By.XPATH, "./..")
            brand_url = brand_url.get_attribute('href')
            print(brand_url)
            url_set.add(brand_url)
    except:
        print("Not Working")
    
    #driver.quit()
    return url_set

def accept_cookies(url):
    driver.get(url)
    driver.implicitly_wait(10)
    cookies = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='cookie-setting-link']")))
    cookies.click()
    
    cookies_accept = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='save-preference-btn-handler onetrust-close-btn-handler button-theme']")))
    cookies_accept.click()

def brandpage_scrape(url):
    #accept_cookies(url)
    driver.implicitly_wait(30)
    time.sleep(5)
    driver.get(url)
    time.sleep(10)
    """
    brand_name = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//h1[@class='wrap-word']")))
    print(brand_name.text.strip())
    """
    try:
        brand_name = driver.find_element(By.XPATH, "//h1[@class='wrap-word']")
        brand_name = brand_name.text.strip()
    except:
        brand_name = "Not Found"

    try:
        brand_description = driver.find_element(By.XPATH, "//div[@class='form-group-view-mode wrap-word exhibitor-details-description']")
        brand_description = brand_description.text.strip()
        brand_description = brand_description[11:]
    except:
        brand_description = "Not Found"

    try:
        brand_link = driver.find_element(By.XPATH, "//div[@class='form-group-view-mode wrap-word zero-top-margin-in-laptop website']")
        brand_link = brand_link.text.strip()
        brand_link = brand_link[15:]
    except:
        brand_link = "Not Found"
    print(brand_link)

    try:
        location = driver.find_element(By.XPATH, "//div[@class='form-group-view-mode wrap-word address']")
        location = location.text.strip()
        location = location[8:]
        location = location.replace("\r"," ")
        location = location.replace("\n"," ")
    except:
        location = "Location Not Found"
    print(location)

    try:
        categories = driver.find_element(By.XPATH, "//div[@data-dtm-category-name='Trend categories']")
        categories = categories.text.strip()
        categories = categories[17:]
    except:
        categories = "Not Found"
    print(categories)

    try:
        linkedin = driver.find_element(By.XPATH, "//a[@data-dtm='exhibitorDetails_follow_linkedin']")
        linkedin = linkedin.get_attribute('href')
    except:
        linkedin = "LinkedIn Not Found"
    print(linkedin)
    
    try:
        company_activity = driver.find_element(By.XPATH, "//div[@data-dtm-category-name='Company Activity']")
        company_activity = company_activity.text.strip()
        company_activity = company_activity[13:]
    except:
        company_activity = "Company Activity Not Found"
    print(company_activity)
    
    try:
        company_size = driver.find_element(By.XPATH, "//div[@data-dtm-category-name='Company Size']")
        company_size = company_size.text.strip()
        company_size = company_size[13:]
    except:
        company_size = "Company Size Not Found"
    print(company_size)
    
    return [brand_name, brand_link, brand_description, categories, location, linkedin, company_activity, company_size, url]

df = pd.DataFrame(columns = ["Brand Name", "Brand Url", "Brand Description", "Categories", "Location", "LinkedIn", "Company Activity", "Company Size", "Site Url"])
options = Options()
options.page_load_strategy = 'normal'
driver = webdriver.Chrome('/Users/tedwards/Desktop/Files and Images/chromedriver_mac64/chromedriver', options = options)
#url = 'https://www.in-cosmetics.com/global/en-gb/exhibitor-details.org-e0d0675f-8db3-4644-aacf-84547b6ef8e0.html#/'
#url = 'https://www.in-cosmetics.com/global/en-gb/exhibitor-details.org-817717a0-91fe-46b4-925a-25714292b175.html#/'
url_set = scrape_directory()
#count = 0
for url in url_set:
    #if count > 10: break
    entry = brandpage_scrape(url)
    df.loc[len(df)] = entry
    #count +=1
#driver.quit()






















"""
players = driver.find_element_by_xpath("//h1[@class='wrap-word']")
for player in players:
    print(player.text.strip())
"""
    
print("Finished.")