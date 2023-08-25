#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 16:02:55 2023

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
df_cre = pd.DataFrame()
getLoop = True

url = "https://gateway.marvel.com/v1/public/creators"
firstName = ""
middleName = ""
lastName = ""
suffix = ""
nameStartsWith = ""
firstNameStartsWith = ""
middleNameStartsWith = ""
lastNameStartsWith = ""
modifiedSince = ""
comics = ""
series = ""
events = ""
stories = ""
orderBy = "modified"
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
            cre = jsondata['data']['results'][i]
            
            cre_id = cre['id']
            cre_firstName = cre['firstName']
            cre_middleName = cre['middleName']
            cre_lastName = cre['lastName']
            cre_suffix = cre['suffix']
            cre_modified = cre['modified']
            
            rev_row = pd.Series([cre_id,cre_firstName,cre_middleName,cre_lastName,cre_suffix,cre_modified])
            row_df_rev = pd.DataFrame([rev_row], index=[i+offset])
            
            df_cre = pd.concat([df_cre, row_df_rev])
            
        except IndexError:
            getLoop = False
            print("All Done. Retrieved items:", df_cre.shape[0])
            break  
            
            
    print("\t offset", offset, ". limit:", limit, ". items: ", df_cre.shape[0]) 
    offset = limit+offset
    
df_cre = df_cre.rename(columns={
    0: 'id',
    1: 'firstName',
    2: 'middleName',
    3: 'lastName',
    4: 'suffix',
    5: 'modified'
})
df_cre.to_csv('result_creators.csv')

