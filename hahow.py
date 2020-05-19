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

def crawling(browser):
    dict_keys = ['_id', 'Course_Title', 'Price', 'Course-tag', 'Rating', 'Student']
    mylist2 = []

    course_lst2 = []
    price_lst2 = []
    #change page - pagnation container
    content_element = browser.find_element_by_id("root")
    content_html = content_element.get_attribute("innerHTML")

    soup3 = BeautifulSoup(content_html, 'html.parser')

    for page in range(18):
        print(soup3.contents[0].prettify())
        

        for idx, course in enumerate(soup3.find_all("h4", class_="title marg-t-20 marg-b-10")):
            #print(idx)
            pd_dict2 = {}
            pd_dict2['Course_Title'] = course.get_text()
            course_lst2.append(course.get_text())
            print(course.get_text())
            mylist2.append(pd_dict2)


        for idx, course in enumerate(soup3.find_all("div", class_="star-ratings")):
            print(course.get('title'))

        for idx, course in enumerate(soup3.find_all("div", class_="pad-rl-15 clearfix")):
            #print(course.string)
            item = course.next_sibling.select('span')
            #print(course.next_sibling.select('span'))
            time = course.string
            student = item[0].get_text()[1:]
            price = item[1].get_text()
            #print(item[0].get_text()[1:])
            #print(item[1].get_text())
            price_lst2.append(price)
            mylist2[idx]['Price'] = price
            mylist2[idx]['Duration'] = time
            mylist2[idx]['Attended Students'] = student
        print(mylist2)
        print(len(course_lst2))
        print(len(price_lst2))

        #next_page_ls = soup3.find("div", class_="pagination-container")
        #next_page = next_page_ls.select('li[class^="rc-pagination-next"]')[0]
        #print(next_page.prettify())
        browser.find_element_by_class_name("rc-pagination-next").click()
    
    return mylist2
    

def insertdb(mylist2):
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
    collect2 = mydb["Hahow"]

    collection_names = mydb.list_collection_names()
    y = collect2.insert_many(mylist2)
    print(y.inserted_ids)   



if __name__ == '__main__':
    browser = webdriver.Chrome('./chromedriver')
    browser.get("https://hahow.in/courses?page=1&status=PUBLISHED")
    time.sleep(3)
    mylist2 = crawling(browser)
    insertdb(mylist2)
    
