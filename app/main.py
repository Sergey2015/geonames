from fastapi import FastAPI, Request, File, UploadFile, BackgroundTasks, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated

import pandas as pd
#import sqlalchemy
from zipfile import ZipFile
import wget
import os
import json
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, insert
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

try:
    from geonames_yandex.app.pack import db_conn
    from geonames_yandex.app.pack import modules
except:     
    from pack import db_conn
    from pack import modules


from dotenv import load_dotenv

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
print("work it")


@app.get("/", response_class=HTMLResponse)
async def read_item2(request: Request):
    return templates.TemplateResponse("index.html",{"request": request, 'test':'привет'})



import pprint

@app.post("/success")
async def success(request: Request, query: Annotated[str, Form()]= None):
    try:
        query
    except : print("нет запроса")
    if query:
        df, dict_df = do_all(query)
        #dict_df = pprint.pprint(dict_df)
        return templates.TemplateResponse("index.html", {"request": request, "query": query, 'df': df, 'dict_df': dict_df})
    else: return templates.TemplateResponse("index.html", {"request": request, "query": query})        
    


from dotenv import load_dotenv

dotenv_path = './config.env'
load_dotenv(dotenv_path=dotenv_path)

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')
print(db_host)


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
        db_conn.write_df('geonames', df)



    result = modules.get_result()

    # def print_user_query(user_query):
    #     return print(user_query)

    #user_query = 'минСС'
    df, dict_df = result.get_result(user_query.lower(), df)
    # print(df)
    # print(dict_df)
    return df, dict_df

#https://devpress.csdn.net/cloudnative/630557977e6682346619e00b.html
#print('df\n', df)