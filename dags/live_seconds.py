from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.hooks.mongo_hook import MongoHook
from airflow.operators.python import PythonOperator
from bs4 import BeautifulSoup
import requests
import pandas as pd

default_args={
    'owner':'shyamron',
    'retries':5,
    'retry_delay':timedelta(minutes=5)
}

#getting live data
def live_data():
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    url = "https://countrymeters.info/en/World"
    page = requests.get(url)
    html = page.content
    soup = BeautifulSoup(html, 'html.parser')
    table=soup.find('div', id='population_clock')
    mongo=MongoHook(conn_id='mongo_connection')
    headers=[]
    data=[]
    for i in table.find_all('tr'):
        row_data=i.find_all('td')
        headers.append(row_data[1].text) #getting only attributes
        data.append(row_data[0].text) #getting values
    mydata = pd.DataFrame(columns = headers)   
    # print(data)
    mydata.loc[0]=data
    documents = mongo.get_collection('Live_data')
    filter={'Date':datetime.now().strftime('%Y-%m-%d')}
    mydata['Date']=datetime.now().strftime('%Y-%m-%d')
    mydata['Time']=datetime.now().strftime('%H:%M:%S')
    #updating database datewise. data is inserted based on date
    documents.update_many(
        filter,
        {"$push": {"data": {"$each":mydata.to_dict('records')}}},
        upsert=True)

#only one task for every 3 seconds
with DAG(
    dag_id='get_live_data',
    default_args=default_args,
    start_date=datetime(2023,5,20),
    schedule_interval=timedelta(seconds=3)
) as dag:
    task1=PythonOperator(
        task_id='live_data',
        python_callable=live_data
    )
    task1