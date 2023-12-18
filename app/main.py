import pandas as pd
import wget
import os
import json

from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from transliterate import translit

from zipfile import ZipFile
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, insert
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dotenv import load_dotenv

try:
    from geonames_yandex.app.pack import db_conn
    from geonames_yandex.app.pack import modules
except:     
    from pack import db_conn
    from pack import modules




dotenv_path = './config.env'
load_dotenv(dotenv_path=dotenv_path)

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')
print(db_host)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item2(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.post("/success")
async def success(request: Request, query: Annotated[str, Form()]= None):
    if query:
        df, dict_df = do_all(query)

        return templates.TemplateResponse("index.html", {"request": request, "query": query, 'df': df, 'dict_df': dict_df})
    else: return templates.TemplateResponse("index.html", {"request": request, "query": query})        

db_conn = db_conn.DatabaseConnection(db_host)

def do_all(user_query):
    #Читаем данные из БД
    try:
        df = db_conn.get_df('geonames')
    except:

        geonames_tables = modules.read_csv_from_geonames()

        country_info_cols, country_info, admin1, cities15000, alternate_name, geo_test = geonames_tables.read_csv_from_geonames_func()

        data = modules.data_preprocessing()
        cities = data.get_needed_countries(cities15000)
        #print(cities)

        df = data.create_main_df(cities, country_info, admin1)

        # Пишем df в БД
        df.columns = df.columns.str.lower()
        db_conn.write_df('geonames', df)


    result = modules.get_result()
    df.columns = df.columns.str.lower()
    full_df = df.copy()
    df, dict_df = result.get_result(user_query.lower(), df)
# Если косинусное сходство менее 0.99, сделаем транслитерацию и проверим результат на ней. 
# Потом объединим df и отберем 5 лучших результатов
    if df.cosine_similarity.max() < 0.99: 
        user_query = translit(user_query, 'ru', reversed=True)
        df2, dict_df2 = result.get_result(user_query.lower(), full_df)
        df = pd.concat([df, df2]).sort_values(by='cosine_similarity', ascending=False).head(5)
    
    return df, dict_df

#https://devpress.csdn.net/cloudnative/630557977e6682346619e00b.html



@app.get("/item", response_class=HTMLResponse)
async def read_item2(request: Request):
    return templates.TemplateResponse("item.html",{"request": request})

@app.post("/itempost")
async def create_item(request: Request, city_name: Annotated[str, Form()]= None, region_name: Annotated[str, Form()]= None, country_name: Annotated[str, Form()]= None):
    print(country_name)
    db_conn.add_row(city_ascii_name=city_name, alternatenames=city_name, country_code=None, region_code=None, country=country_name, iso=None, region_name=region_name)
    return templates.TemplateResponse("index.html", {"request": request, "city_name": city_name, "region_name": region_name, "country_name": country_name}) 
    

    #db_item = crud.create_item(db=db, item=item)
    #return db_item