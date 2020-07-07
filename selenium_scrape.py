import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import string 
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

class crawler:
    def __init__(self,directory):
        self.company_list = self.open_name(directory)
        self.date = datetime.today().weekday()

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
        data = []
        for i in range(frequency):
            start = time.time()
            counter = 0
            for ticker in self.company_list:
                link = 'https://finance.yahoo.com/quote/' + ticker + '/?p=' + ticker
                driver.get(link)
                html = driver.execute_script("return document.body.innerHTML;")
                if not html:
                    continue
                soup = BeautifulSoup(html, 'lxml')
                cur_price = [entry.text for entry in soup.find_all('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
                data.append([i,self.date, datetime.today().strftime('%Y-%m-%d-%H:%M:%S'),cur_price])
                counter += 1 
                print(counter)
            print(time.time() - start)
        print(data)
a = crawler('/users/da/documents/github/Auto-Crawler/Nasdaq_tickers.csv')
a.crawler(0,1)
# link = "https://finance.yahoo.com/quote/AAPL/?p=AAPL%27"
# driver.get(link)
# html = driver.execute_script("return document.body.innerHTML;")
# soup = BeautifulSoup(html, 'lxml')
# cur_price = [entry.text for entry in soup.find_all('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
# print(cur_price)