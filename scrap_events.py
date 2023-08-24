#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 14:51:43 2023

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
df_ev = pd.DataFrame()
getLoop = True

url = "https://gateway.marvel.com/v1/public/events"
name = ""
nameStartsWith = ""
modifiedSince = ""
creators = ""
characters = ""
series = ""
comics = ""
stories = ""
orderBy = "startDate"
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
            ev = jsondata['data']['results'][i]
            
            ev_id = ev['id']
            ev_title = ev['title']
            ev_start = ev['start']
            ev_end = ev['end']
            ev_next = ev['next']
            ev_previous = ev['previous']
            ev_modified = ev['modified']
            
            rev_row = pd.Series([ev_id, ev_title, ev_start, ev_end, ev_next, ev_previous, ev_modified])
            row_df_rev = pd.DataFrame([rev_row], index=[i+offset])
            
            df_ev = pd.concat([df_ev, row_df_rev])
        except IndexError:
             getLoop = False
             print("All Done. Retrieved items:", df_ev.shape[0])
             break
    print("\t offset", offset, ". limit:", limit, ". items: ", df_ev.shape[0]) 
    offset = limit+offset
    
df_ev = df_ev.rename(columns={
    0: "id",
    1: "title",
    2: "start",
    3: "end",
    4: "next",
    5: "previous",
    6: "modified"})
df_ev.to_csv("result_events.csv")