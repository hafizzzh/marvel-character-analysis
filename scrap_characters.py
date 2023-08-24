#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 12:02:06 2023

@author: Ibrahim Hafizhan Witsqa
"""
import json
import time
import calendar
import hashlib
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
df_chars = pd.DataFrame()
getLoop = True

url = "https://gateway.marvel.com/v1/public/characters"
name = ""
nameStartsWith = ""
modifiedSince = ""
comics = ""
series = ""
events = ""
stories = ""
orderBy = "name"
limit = 100
offset = 0

current_GMT = time.gmtime()
ts = str(calendar.timegm(current_GMT))
pvkey = os.getenv("MARVEL_PVKEY")
pbkey = os.getenv("MARVEL_PBKEY")
assemble = ts+pvkey+pbkey
juru = hashlib.md5(assemble.encode())

while(getLoop):
    querystring = {"orderBy": str(orderBy),
                   "apikey": str(pbkey),
                   "ts": ts,
                   "hash": juru.hexdigest(),
                   "limit": limit,
                   "offset": offset}
    
    response = requests.request("GET", 
                                url, 
                                params=querystring)
    
    jsondata = json.loads(response.text)
    
    for i in range(limit):
        try: 
            char = jsondata['data']['results'][i]
            
            char_id = char['id']
            char_name = char['name']
            char_date = char['modified']
            
            rev_row = pd.Series([char_id,char_name,char_date])
            row_df_rev = pd.DataFrame([rev_row], index=[i+offset])
            
            df_chars = pd.concat([df_chars, row_df_rev])
        except IndexError:
            getLoop = False
            break
            print("All done")
        
    print("\t offset", offset, ". limit:", limit) 
    offset = limit+offset
    
df_chars = df_chars.rename(columns={
    0: 'id',
    1: 'name',
    2: 'last_modified'})
df_chars.to_csv("result_characters.csv")