from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import requests
import json

#accessing mongodb for data
def data_db(type):
    url = "https://ap-south-1.aws.data.mongodb-api.com/app/data-uilna/endpoint/data/v1/action/find"
    payload = json.dumps({
        "collection": type,
        "database": "World_population",
        "dataSource": "Cluster0",

    })
    headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': 'KRTVZBuxB5kasrcrM7KDCWWksvdrKnTwLnb4KQoS3j4N5cPfdZsZutrYgSpaeavn', 
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    if type!='History_data':
        data=pd.DataFrame(data)
        data=data.iloc[-1,0] #getting only latest data
        data = pd.DataFrame(data['data'])
        data.drop('Date',axis=1,inplace=True)
    else:
        data = pd.DataFrame(data['documents'])
        data.drop('_id',axis=1,inplace=True)
    return data

#returns data based on required type
def get_scrape_data(type):
    print(type)
    print(datetime.now())
    try:
        if type=='history':
            req_data=data_db('History_data')
        elif type=='live':
            req_data=data_db('Live_data')
        elif type=='religion':
            req_data=data_db('Religion_data')
        elif type=='age':
            req_data=data_db('Age_data')
        elif type=='continent':
            req_data=data_db('Continent_data')
        elif type=='country':
            req_data=data_db('Country_data')
        else:
            print('No such data')        
            req_data={}
    except:
        print('No such data')
    return req_data

# get_scrape_data('live')