#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 08:56:24 2023

@author: tedwards
"""
import pandas as pd
def compare_csv(old_csv, new_csv):
    """
    Here we need to get the headers from the two csvs. 
    We need to check that those are all the same. 
    Next we need to make a map out of all the information in csv_one, mapping company name to everything else
    Then we need to iterate through csv_two and check that things are not different. 
    """
    df = pd.DataFrame(columns=new_csv.columns)
    #dict_attempt = dict()
    set_attempt = set()
    for index, row in old_csv.iterrows():
        print(row[0])
        set_attempt.add(row[0])
    for index, row in new_csv.iterrows():
        print(row[1])
        if not row[1] in set_attempt: df.loc[len(df)] = row
    print("done.")
    return df

old_csv = pd.read_csv("/Users/tedwards/Downloads/Scrape Amalgamations - ThingTesting after 7_19.csv")
new_csv = pd.read_csv("/Users/tedwards/Downloads/Scrape Outputs - ThingTesting Scrape on 8_21 10am.csv")
df = compare_csv(old_csv, new_csv)
        
        
        
        