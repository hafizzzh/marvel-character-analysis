#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 14:46:46 2023

@author: hafizzzh
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
df_com = pd.DataFrame()
getLoop = True

url = "https://gateway.marvel.com/v1/public/comics"
format = ""
formatType = ""
noVariants = ""
dateDescriptor = ""
dateRange = ""
title = ""
titleStartsWith = ""
startYear = ""
issueNumber = ""
diamondCode = ""
digitalId = ""
upc = ""
isbn = ""
ean = ""
issn = ""
hasDigitalIssue = ""
modifiedSince = ""
creators = ""
characters = ""
series = ""
events = ""
stories = ""
sharedAppearances = ""
collaborators = ""
orderBy = "onsaleDate"
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
            com = jsondata['data']['results'][i]
            
            com_id = com['id']
            com_title = com['title']
            com_issueNumber = com['issueNumber']
            com_modified = com['modified']
            com_format = com['format']
            com_pageCount = com['pageCount']
            
            for j in range(len(com['dates'])):
                if com['dates'][j]['type']=="onsaleDate":
                    com_onsaleDate = com['dates'][j]['date']
                    print(com['title'], com['dates'][j]['type'])
            
            for k in range(len(com['prices'])):
                if com['prices'][k]['type']=="printPrice":
                    com_printPrice = com['prices'][k]['price']
                    com_digitalPrice = ""
                else:
                    com_digitalPrice = com['prices'][k]['price']

            com_series = com['series']
            rev_row = pd.Series([com_id,com_title,com_issueNumber,com_modified,com_format,com_pageCount,com_onsaleDate,com_printPrice,com_digitalPrice,com_series])
            row_df_rev = pd.DataFrame([rev_row], index=[i+offset])
            
            df_com = pd.concat([df_com, row_df_rev])
        except IndexError:
             getLoop = False
             print("All Done. Retrieved items:", df_com.shape[0])
             break
    print("\t offset", offset, ". limit:", limit, ". items: ", df_com.shape[0]) 
    offset = limit+offset
    
df_com = df_com.rename(columns={
    0: 'id',
    1: 'title',
    2: 'issueNumber',
    3: 'modified',
    4: 'format',
    5: 'pageCount',
    6: 'onsaleDate',
    7: 'printPrice',
    8: 'digitalPrice',
    9: 'series'
})
df_com.to_csv('result_comics.csv')