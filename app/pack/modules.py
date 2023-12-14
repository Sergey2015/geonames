import pandas as pd
from zipfile import ZipFile
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class read_csv_from_geonames:
    def __init__(self):
        print("init")

    def read_csv_from_geonames_func(self):
        country_info_cols = ['ISO',	'ISO3',	'ISO-Numeric',	'fips',	'Country',	'Capital',	'Area(in sq km)',	'Population',	'Continent',	'tld',	'CurrencyCode',	'CurrencyName',	'Phone',	'Postal Code Format', 'Postal Code Regex',	'Languages',	'geonameid',	'neighbours',	'EquivalentFipsCode']
        country_info = pd.read_csv('http://download.geonames.org/export/dump/countryInfo.txt', sep='\t', comment='#', names=country_info_cols, usecols=['geonameid', 'ISO', 'Country'])
        admin1 = pd.read_csv('http://download.geonames.org/export/dump/admin1CodesASCII.txt', sep = '\t', quoting = 3, header = None, names=['code', 'name', 'ascii_name', 'geonameid'])
        cities15000 = pd.read_csv('http://download.geonames.org/export/dump/cities15000.zip', sep = '\t', header = None, quoting = 3, names = ['geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude', 'feature_class', 'feature_code', 'country_code', 'cc2', 'admin1_code', 'admin2_code', 'admin3_code', 'admin4_code', 'population', 'elevation', 'dem', 'timezone', 'modification_date'])
        geo_test = pd.read_csv('data/geo_test.csv', sep=';')
        alternate_name = pd.read_csv(ZipFile('data/alternateNamesV2.zip').open('alternateNamesV2.txt'), sep = '\t', quoting = 3, header = None)
       
   
        
        return country_info_cols, country_info, admin1, cities15000, alternate_name, geo_test
    
class data_preprocessing:
    def get_needed_countries(self, cities15000):
        cities = cities15000.copy().loc[cities15000['country_code'].isin(['RU', 'BY', 'KZ', 'AM', 'RS', 'KG', 'TR']), ['geonameid', 'asciiname', 'alternatenames', 'admin1_code', 'country_code']]
        cities['region_code'] =  cities['country_code'] +'.' + cities['admin1_code']
        cities.drop(['admin1_code'], axis=1, inplace=True)
     
        return cities
    
    def create_main_df(self, cities, country_info, admin1):
        cities['alternatenames'] = cities['alternatenames'].str.split(',')
        df = cities.explode('alternatenames').rename(columns={'asciiname':'city_ascii_name', 'geonameid':'city_geoname_id'}).reset_index()
        df = df.merge(country_info[['Country', 'ISO']], left_on='country_code', right_on='ISO', how='left')

        df = df.merge(admin1[['code', 'name']], left_on='region_code', right_on='code', how='left').rename(columns={'name':'region_name'}).drop(['code', 'city_geoname_id', 'index'], axis=1).dropna(subset='alternatenames').reset_index()
        df.drop('index', axis=1, inplace=True)

        df.columns = df.columns.str.lower()
        df['city_ascii_name'] = df['city_ascii_name'].str.lower()
        df['alternatenames'] = df['alternatenames'].str.lower()


        add_alternames = df[~df['city_ascii_name'].isin(df['alternatenames'])]
        add_alternames['alternatenames'] = add_alternames['city_ascii_name']
        #print("печатаем несовпадающие\n", add_alternames, "конец \n")
        add_alternames = add_alternames.drop_duplicates(subset='city_ascii_name')
        #print("без дублей\n", add_alternames, "конец \n")
        df = pd.concat([df, add_alternames])
        return df

class get_result():
    def __init__(self):
        print("init")

    def get_result(self, city, df):
        self.city = city
        #for city in user_query:
        #df = df2
        vectorizer = TfidfVectorizer(lowercase=True, analyzer="char", ngram_range=(2, 3))
        tfidf_matrix = vectorizer.fit_transform(df['alternatenames'])

        user_query_vector = vectorizer.transform([self.city])

        df['cosine_similarity'] = cosine_similarity(tfidf_matrix, user_query_vector).flatten()
        df = df.groupby('city_ascii_name').max().reset_index()
        df.sort_values('cosine_similarity', ascending=False, inplace=True)
        df[df['cosine_similarity']>0]
        df = df.head(5)
        # print(self.city)
        # print(df[['city_ascii_name', 'region_name', 'country', 'cosine_similarity']].reset_index(drop=True))
        df = df[['city_ascii_name', 'region_name', 'country', 'cosine_similarity']].reset_index(drop=True)
        dict_df = df[['city_ascii_name', 'region_name', 'country', 'cosine_similarity']].reset_index(drop=True).to_dict('records')
        return df, dict_df

