from datetime import date
from select import select
import urllib.request
from bs4 import BeautifulSoup as bs
import ssl
import certifi
import json
import mysql.connector
from git import Repo
import git
import os

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "github",
    auth_plugin='mysql_native_password'
)
cursor = mydb.cursor()
date = date.today()
text = "ansible"
urlp = 'https://github.com/search?p=1&q=' +text+'&type=Repositories'
page = urllib.request.urlopen(urlp,context=ssl.create_default_context(cafile=certifi.where()))
soup = bs(page,features = "html.parser")
tags = soup.find_all('a',attrs ={'class': 'v-align-middle'})
length = len(tags)
j = 0
for i in range(length):
    link = tags[i]['data-hydro-click']
    folder_link = tags[i]['href']
    print(folder_link)
    folder_link = folder_link.replace('/','')
    res = json.loads(link)
    val = res['payload']['result']['url']
    sql = "INSERT INTO gitlink (number,link,date) VALUES (%s,%s,%s)"
    value = (j,val,date)
    cursor.execute(sql,value)
    j += 1
mydb.commit()
