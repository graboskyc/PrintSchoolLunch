from fastapi import FastAPI, Response
import datetime
from fastapi.staticfiles import StaticFiles
import json
import os
import requests
from typing import Dict, Any
from fastapi.middleware.cors import CORSMiddleware
import dateparser

api_app = FastAPI(title="api-app")
app = FastAPI(title="spa-app")
app.mount("/api", api_app)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

from fastapi import Query

@api_app.get("/menu")
async def menu(d: str = Query(None, description="Date in MM/DD/YYYY format")):
    url = os.environ["LUNCHURL"].strip()
    if d:
        url = url + f"&date={d}"
    else:
        # Default to today's date if not provided
        today = datetime.datetime.now().strftime("%m/%d/%Y")
        url = url + f"&date={today}"

    response = requests.get(url)
    data = response.json()

    simplifiedResult = [{"key":"Today's Menu Features", "replace":"features", "dow":[[],[],[],[],[]]}
                      ,{"key":"Specials", "replace":"specials", "dow":[[],[],[],[],[]]}
                      ,{"key":"Soups", "replace":"soups", "dow":[[],[],[],[],[]]}
                      ,{"key":"Salads", "replace":"salads", "dow":[[],[],[],[],[]]}
                      ,{"key":"Entr\u00e9es", "replace":"entrees", "dow":[[],[],[],[],[]]}
                      ,{"key":"Sides and Vegetables", "replace":"sides", "dow":[[],[],[],[],[]]}
                      ,{"key":"Desserts", "replace":"desserts", "dow":[[],[],[],[],[]]}]

    for d, v in data.items():
        print(d)
        convertToDate = dateparser.parse(d.strip().replace("\\",""))
        # if it is not a date, skip  it
        if convertToDate is None:
            continue
        # if not a weekend
        if convertToDate.weekday() < 5: 
            for k, i in v.items():
                for item in simplifiedResult:
                    if k == item["key"]:
                        for menuitem in i:
                            index = int(menuitem["day"]) - 1
                            item["dow"][index].append(menuitem)
                            
    return simplifiedResult
