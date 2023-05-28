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

#getting html for population of year 2023
def get_html(ti):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    url = "https://countrymeters.info/en/World"
    page = requests.get(url)
    html = page.content.decode('utf-8')
    ti.xcom_push(key='html',value=html)

#getting html for population of continents
def get_html_continent(ti):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    url = "https://countrymeters.info/en"
    page = requests.get(url)
    html = page.content.decode('utf-8')
    ti.xcom_push(key='html_continent',value=html)

#getting html for population of countries
def get_html_country(ti):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    url='https://countrymeters.info/en/list/List_of_countries_and_dependent_territories_of_the_World_by_population'
    page = requests.get(url)
    html = page.content.decode('utf-8')
    ti.xcom_push(key='html_country',value=html)

#getting country population data
def country_data(ti):
    html = ti.xcom_pull(task_ids='get_html_country',key='html_country')
    soup = BeautifulSoup(html, 'html.parser')
    mongo=MongoHook(conn_id='mongo_connection')
    country = mongo.get_collection('Country_data')
    table = soup.find('table', class_='facts')
    headers=[]
    for i in table.find_all('th'):
        title=i.text.strip()
        headers.append(title)
    mydata=pd.DataFrame(columns=headers)
    n=0
    for j in table.find_all('tr')[1:-1]:
        row_data=j.find_all('td')[2:]
        row = [i.text for i in row_data]
        # print(row)
        mydata.loc[n] = row
        n+=1
    filter={'Date':datetime.now().strftime('%Y-%m-%d')}
    mydata['Date']=datetime.now().strftime('%Y-%m-%d')
    #updating database based on date
    country.update_many(
        filter,
        {"$set": {"data": mydata.to_dict('records')}},
        upsert=True)

#getting continent population data
def continent_data(ti):
    html = ti.xcom_pull(task_ids='get_html_continent',key='html_continent')
    soup = BeautifulSoup(html, 'html.parser')
    mongo=MongoHook(conn_id='mongo_connection')
    continent = mongo.get_collection('Continent_data')
    table_divs = soup.find_all('div', class_='data_div')
    if len(table_divs) >= 2:
        table = table_divs[2]
    else:
        table=table_divs[1]
        print('There are less than 3 div elements with the class name data_div.')
    headers=['Continent','Population','Percent']
    mydata=pd.DataFrame(columns=headers)
    n=0
    for i in table.find_all('tr'):
        columns = i.find_all('td')[1:]
        if columns:
            row = [i.text for i in columns]
            mydata.loc[n] = row
            n+=1
    filter={'Date':datetime.now().strftime('%Y-%m-%d')}
    mydata['Date']=datetime.now().strftime('%Y-%m-%d')
    #updating databased based on date
    continent.update_many(
        filter,
        {"$set": {"data": mydata.to_dict('records')}},
        upsert=True)

#data for year 2023 is updated everyday. getting population for year 2023
def history_update(ti):
    html = ti.xcom_pull(task_ids='get_html',key='html')
    soup = BeautifulSoup(html, 'html.parser')
    mongo=MongoHook(conn_id='mongo_connection')
    history_data = mongo.get_collection('History_data')

    table_divs=soup.find_all('div',class_='data_div width45')
    if len(table_divs)>=2:
        table=table_divs[0]
    else:
        table=table_divs[0]
    last_row = table.find_all('tr')[-1]
    row_data = last_row.find_all('td')
    row = [i.text for i in row_data]
    filter={"Year":row[0]}
    new_data={"Population":row[1],"Growth Rate":row[2]}
    new_data['Date']=datetime.now().strftime('%Y-%m-%d')
    #replacing old 2023 year's data with today's 2023 year data
    history_data.update_one(filter,{"$set":new_data},upsert=True)

with DAG(
    dag_id='get_daily_data',
    default_args=default_args,
    start_date=datetime(2023,5,21),
    schedule_interval='0 9 * * *'
) as dag:
    task1=PythonOperator(
        task_id='get_html',
        python_callable=get_html,
        provide_context=True
    )
    task11=PythonOperator(
        task_id='get_html_continent',
        python_callable=get_html_continent,
        provide_context=True
    )
    task12=PythonOperator(
        task_id='get_html_country',
        python_callable=get_html_country,
        provide_context=True
    )
    task2=PythonOperator(
        task_id='country_data',
        python_callable=country_data
    )
    task3=PythonOperator(
        task_id='continent_data',
        python_callable=continent_data
    )
    task4=PythonOperator(
        task_id='history_update',
        python_callable=history_update
    )
    #getting html for each task and then getting data
    task1 >> task4
    task11 >> task3
    task12 >> task2