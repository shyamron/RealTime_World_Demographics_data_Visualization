import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
from pymongo import MongoClient
from datetime import datetime

url="https://countrymeters.info/en/World"
page=requests.get(url)
if page.status_code==200:
    html=page.content
    soup = BeautifulSoup(html, 'html.parser')

cluster=MongoClient("<URL>")
db=cluster['World_population']


table_divs=soup.find_all('div',class_='data_div width45')
if len(table_divs)>=2:
    table=table_divs[0]
else:
    table=table_divs[0]
headers=[]
for i in table.find_all('th'):
    title=i.text
    headers.append(title)
mydata=pd.DataFrame(columns=headers)
print(headers)
n=0
for j in table.find_all('tr')[1:]:
    row_data=j.find_all('td')
    row = [i.text for i in row_data]
    print(row)
    mydata.loc[n] = row
    n+=1
print(mydata)
history_data=db['History_data']
mydata['Date']=datetime.now().strftime('%Y-%m-%d')
history_data.insert_many(mydata.to_dict('records'))