import pandas as pd
import psycopg2
import matplotlib.pyplot as plt 
import sys
from matplotlib.backends.backend_pdf import PdfPages


class queryandTransform:
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

class graph(queryandTransform):

    def __init__(self,output_name,start_date,end_date,ticker,user,password,host,port,database):
        super().__init__(start_date,end_date,ticker,user,password,host,port,database)
        self.ticker = ticker
        self.start = start_date
        self.end = end_date
        self.date = self.date_sep()
        self.output =  PdfPages(output_name)
        self.fig = plt.figure(figsize=(10,10))
        self.graph_data()

    def graph_data(self):
        self.price_movement()
        self.price_change()
        self.weekday()
        # self.monthly()
        print('Complete')
        self.output.close()

    def date_sep(self):
        temp = (self.data['Date'].str.split('-').tolist())
        return ['/'.join(i[1:]) for i in temp]

    def price_change(self):
        plt.plot(self.date,self.data['change'])
        plt.text(0.05,0.95,'This Plot shows the changes in price with relation to the previous' +\
            ' day',transform=self.fig.transFigure)
        plt.xticks(fontsize=8, rotation=90)
        plt.grid(True)
        self.output.savefig()
        plt.clf()
        return 

    def hourly(self):
        pass

    def monthly(self):
        pass

    def weekday(self):
        pass 

    def price_movement(self):
        # price movement for last week
        plt.plot(self.date,self.data['Price'])
        plt.xticks(fontsize=8, rotation=90)
        plt.title('Price Movement')
        txt = 'The price movement from ' + self.start + ' to ' + self.end 
        plt.text(0.05,0.95,txt,transform=self.fig.transFigure)
        plt.grid(True)
        self.output.savefig()
        plt.clf()
        return 

if __name__ == "__main__":
    graph(*sys.argv[1:])