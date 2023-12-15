

# engine = create_engine('postgresql://admin:admin@172.20.110.2/default', echo = True)
# metadata = MetaData()
print("111111111")
import pandas as pd




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
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, insert #,MetaDatafrom
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime




class DatabaseConnection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.metadata = MetaData()
        

    def connect(self):
        connection = self.engine.connect()
        return connection

    def get_table(self, table_name):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        return table
    def get_df(self, table_name):
        return pd.read_sql_table(table_name, self.engine)
   
    def write_df(self, table_name, df):
        return df.to_sql(table_name, self.engine, if_exists='replace', index=False)
    
    def add_row(self, city_ascii_name, alternatenames, country_code, region_code, country, iso, region_name):
        add_row = (
            insert(get_table('geonames')).
            values(city_ascii_name = city_ascii_name, alternatenames = alternatenames, country_code = country_code, region_code = region_code, country = country, iso = iso, region_name = region_name)
                )
        # Компиляция словарика (не обязательно)
        # compiled = stmt.compile()
        # compiled.params
        with self.engine.connect() as conn:
            result = conn.execute(add_row)
            conn.commit()
    def remove_table(self, table_name):
        self.table_name = table_name
        with self.engine.connect() as connection:
            result = connection.execute(text(f"DROP table {self.table_name}"))
            connection.commit()            

    

# import os

# username = os.environ.get('DATABASE_USERNAME', 'default_username')
# password = os.environ.get('DATABASE_PASSWORD', 'default_password')
# print(username)