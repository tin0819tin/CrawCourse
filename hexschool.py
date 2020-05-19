import requests
import re
from bs4 import BeautifulSoup
import copy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import numpy as np
import os
import re
from sshtunnel import SSHTunnelForwarder
import pymongo


def crawling(req1):
    soup1 = BeautifulSoup(req1.content, 'lxml')

    dict_keys = ['_id', 'Course_Title', 'Price', 'Course-tag', 'Rate', 'Student']
    mylist1 = []

    price_lst = []

    for idx, i in enumerate(soup1.find_all(href=re.compile("^https://shop"))):
        #print(i.prettify())
        pd_dict = {}
        if i.get("data-price"):
            price_lst.append(i.get("data-price"))
            #pd_dict['_id'] = idx+1
            pd_dict['Price'] = i.get("data-price")
            pd_dict['Coures_Title'] = i.get('data-title')
            pd_dict['Course-tag'] = i.get('data-id').upper()
            mylist1.append(pd_dict)
        print(i.get("data-price"))


    print(len(mylist1) == len(price_lst))
    print(mylist1)
    return mylist1

def insert_db(mylist1):
    #Connecting to MongoDB
    MONGO_HOST = "3.95.254.201"
    MONGO_USER = "ubuntu"
    #MONGO_DB = "TTRI"
    # MONGO_COLLECTION = "COLLECTION_NAME"
    # define ssh tunnel
    server = SSHTunnelForwarder(
        MONGO_HOST,
        ssh_username=MONGO_USER,
        ssh_pkey="/Users/apple/Desktop/Bigdata & E-commerce/EC_ec2-key.pem.txt",
        remote_bind_address=('127.0.0.1', 27017)
    )

    server.start()

    client = pymongo.MongoClient('127.0.0.1', server.local_bind_port) # server.local_bind_port is assigned local port
    mydb = client["CrawCourse"]
    collect1 = mydb["Hexschool"]
    collection_names = mydb.list_collection_names()
    x = collect1.insert_many(mylist1)
    print(x.inserted_ids)



if __name__ == '__main__':
    hexschool_url = "https://www.hexschool.com/courses/#"
    req1 = requests.get(hexschool_url)
    print(req1.status_code)
    mylist1 = crawling(req1)
    insert_db(mylist1)




 