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

#getting html
def get_html(ti):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    url = "https://countrymeters.info/en/World"
    page = requests.get(url)
    html = page.content.decode('utf-8')
    ti.xcom_push(key='html',value=html)

#getting age data
def age_data(ti):
    html = ti.xcom_pull(task_ids='get_html',key='html')
    soup = BeautifulSoup(html, 'html.parser')
    mongo=MongoHook(conn_id='mongo_connection')
    age_data = mongo.get_collection('Age_data')
    table=soup.find('table',class_='perc')
    age_data_df=pd.DataFrame(columns=['Under 15','Between 15 and 64','Above 64'])
    for i in table.find_all('tr'):
        row_data=i.find_all('td')
        age=[i.text for i in row_data]
        if row_data:
            age_data_df.loc[0]=age
    filter={'Date':datetime.now().strftime('%Y-%m')}
    age_data_df['Date']=datetime.now().strftime('%Y-%m')
    #updating database based on month
    age_data.update_many(
        filter,
        {"$set": {"data": age_data_df.to_dict('records')}},
        upsert=True)

#getting religion data
def religion_data(ti):
    html = ti.xcom_pull(task_ids='get_html',key='html')
    soup = BeautifulSoup(html, 'html.parser')
    mongo=MongoHook(conn_id='mongo_connection')
    religion_data = mongo.get_collection('Religion_data')
    table1=soup.find('table', class_='years')
    headers=[]
    for i in table1.find_all('tr'):
        row_data=i.find_all('td')
        headers.append(row_data[0].text)
    mydata = pd.DataFrame(columns = headers)   
    data=[]
    for row in table1.find_all('tr')[0:]:
        columns = row.find_all('td')[1:2]
        if columns:
            row_values = [col.text.strip() for col in columns]
            data.append(row_values[0])
    mydata.loc[0]=data
    filter={'Date':datetime.now().strftime('%Y-%m')}
    mydata['Date']=datetime.now().strftime('%Y-%m')
    #updating databased based on month
    religion_data.update_many(
        filter,
        {"$set": {"data": mydata.to_dict('records')}},
        upsert=True)


with DAG(
    dag_id='get_monthly',
    default_args=default_args,
    start_date=datetime(2023,5,21),
    schedule_interval='0 9 * 1-12 1'
) as dag:
    task1=PythonOperator(
        task_id='get_html',
        python_callable=get_html,
        provide_context=True
    )
    task2=PythonOperator(
        task_id='age_data',
        python_callable=age_data
    )
    task3=PythonOperator(
        task_id='religion_data',
        python_callable=religion_data
    )
    task1 >> [task2,task3]