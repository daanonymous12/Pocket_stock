import pandas as pd
import psycopg2
from io import BytesIO
import matplotlib.pyplot as plt 

class data_generation:
    def __init__(self, start_date,end_date,ticker,user,password,host,port,database):
        
        raw_data = self.query_data(start_date, end_date, ticker,user,password,host,port,database)
        self.data = self.data_feature(raw_data)

    def data_feature(self, data):
        # add diff
        data = self.time_mod(data)
        data['change'] = data['Price'].diff()
        data['change'].loc[0] = 0
        return data

    def time_mod(self,data):
        new_data = data.filter(['Day','Price'])
        temp = pd.DataFrame(data['Date'].str.split(' ').tolist())
        new_data['Date'],new_data['Time'] = temp[0],temp[1]
        return new_data 

    def query_data(self, start_date, end_date, ticker,user,password,host,port,database):
        self.connection = psycopg2.connect(user = user,
                                  password = password,
                                  host = host,
                                  port = port,
                                  database = database)
        cursor = self.connection.cursor()
        select_statement = "select * from stock_data as s\
                             where s.ticker = %s and date(s.date)\
                                 between date(%s) and date(%s)\
                                     order by s.date asc"
        cursor.execute(select_statement,(ticker,start_date,end_date))
        data = pd.DataFrame(cursor.fetchall())
        data.columns = ['Ticker','Day', 'Date', 'Price']
        data['Price'] = data['Price'].round(2)
        return data

class graph(data_generation):

    def __init__(self,output_name,start_date,end_date,ticker,user,password,host,port,database):
        super().__init__(start_date,end_date,ticker,user,password,host,port,database)
        self.ticker = ticker
        self.start = start_date
        self.end = end_date
        self.output =  open(output_name,'wb')
        # self.weekday()
        # self.monthly()
        print(self.data)
        self.price_movement()

    def hourly(self):
        pass

    def monthly(self):
        pass

    def weekday(self):
        pass 

    def price_movement(self):
        # price movement for last week
        temp = (self.data['Date'].str.split('-').tolist())
        date = ['/'.join(i[1:]) for i in temp]
        plt.plot(date,self.data['Price'])
        plt.xticks(fontsize=8, rotation=90)
        # img = BytesIO()
        # plt.savefig(img,format = "png")
        # self.output.write(img.getvalue())

x = graph('output.txt','2019-09-01','2019-12-01','AAPL','da','','localhost','5432','da')
    