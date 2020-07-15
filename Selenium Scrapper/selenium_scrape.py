import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import string 
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
import psycopg2
import sys
sys.path.append("../")
from creden.credential import cred

class crawler:
    def __init__(self,directory,user,password,host,port,database):
        self.company_list = self.open_name(directory)
        self.date = datetime.today().weekday() # Monday is 0, sunday is 6
        self.cursor = self.database(user,password,host,port,database)

    def database(self,user,password,host,port,database):
        self.connection = psycopg2.connect(user = user,
                                  password = password,
                                  host = host,
                                  port = port,
                                  database = database)
        cursor = self.connection.cursor()
        return cursor

    def open_name(self,directory):
        csv = pd.read_csv(directory)
        return list(csv['Symbol'])

    def driver_param(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
        return driver

    def crawler(self, waittime, frequency):
        driver = self.driver_param()
        while True:
            data = []
            for _ in range(frequency):
                for ticker in self.company_list[:5]:
                    link = 'https://finance.yahoo.com/quote/' + ticker + '/?p=' + ticker
                    driver.get(link)
                    html = driver.execute_script("return document.body.innerHTML;")
                    if not html:
                        continue
                    soup = BeautifulSoup(html, 'lxml')
                    cur_price = [entry.text for entry in soup.find_all('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
                    data.append([ticker,self.date, datetime.today().strftime('%Y-%m-%d %H:%M:%S'),float(cur_price[0])])
            print(data)
            self.write(data)

    def write(self,data):
        postgres_insert_query = """ INSERT INTO stock_data (ticker,Day,Date,Price) VALUES (%s,%s,%s,%s)"""
        self.cursor.executemany(postgres_insert_query, data)
        self.connection.commit()
        count = self.cursor.rowcount
        print (count, "Record inserted successfully into mobile table")

a = crawler('/Users/da/Documents/GitHub/auto_crawler/Mock_Data/Nasdaq_tickers.csv','da','','localhost','5432','da')
a.crawler(0,1)