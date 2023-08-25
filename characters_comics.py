#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 17:44:43 2023

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
df_char = pd.read_csv('result/result_characters 22 Aug.csv')
df_char_com = pd.DataFrame()
limit = 100
offset_2 = 0

current_GMT = time.gmtime()
ts = str(calendar.timegm(current_GMT))
pvkey = os.getenv("MARVEL_PVKEY")
pbkey = os.getenv("MARVEL_PBKEY")
assemble = ts+pvkey+pbkey
juru = hashlib.md5(assemble.encode())

i = 684    
for i in range(1562):
    getLoop = True
    offset = 0
    char_id = df_char.loc[i,'id']
    url = "https://gateway.marvel.com/v1/public/characters/"+str(char_id)+"/comics"
    while(getLoop):
        querystring = {"apikey": str(pbkey),
                       "ts": ts,
                       "hash": juru.hexdigest(),
                       "limit": limit,
                       "offset": offset}
        response = requests.request("GET", 
                                    url, 
                                    params=querystring)
        jsondata = json.loads(response.text)
        print(url)
        j=0
        for j in range(limit):
            try:
                char_com = jsondata['data']['results'][j]
                
                com_id = char_com['id']
                rev_row = pd.Series([char_id, com_id])
                row_df_rev = pd.DataFrame([rev_row], index=[j+offset])
                df_char_com = pd.concat([df_char_com, row_df_rev])
                
            except IndexError:
                getLoop = False
                continue
            j=j+1
        offset = limit+offset
    print("\t Offset", offset, 
          ". Limit:", limit, 
          ". Items: ", df_char_com.shape[0])
    i=i+1
    print("loop at: "+str(i))
df_char_com = df_char_com.rename(columns={
    0: 'char_id',
    1: 'com_id',
})
df_char_com.to_csv('result_char_com.csv')

print(df_char.loc[684,'id'])
x_df_char_com = df_char_com[df_char_com.char_id != 1009508]
