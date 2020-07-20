import pandas as pd
import psycopg2
import matplotlib.pyplot as plt 
import sys
from matplotlib.backends.backend_pdf import PdfPages

class transform:
    def __init__(self,data):
        self.raw = data 
        self.data = self.update_data()

    def update_data(self):
        data = self.data_feature(self.raw)
        return data

    def data_feature(self, data):
        data = self.time_mod(data)
        data['change'] = data['Price'].diff()
        data['change'].loc[0] = 0
        return data

    def time_mod(self,data):
        new_data = data.filter(['Day','Price'])
        temp = pd.DataFrame(data['Date'].str.split(' ').tolist())
        print(temp,new_data)
        new_data['Date'],new_data['Time'] = temp[0],temp[1]
        return new_data 

class query(transform):
    def __init__(self, start_date,end_date,ticker,user,password,host,port,database):
        raw_data = self.query_data(start_date, end_date, ticker,user,password,host,port,database)
        super().__init__(raw_data)

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

class graph(query):

    def __init__(self,output_name,start_date,end_date,ticker,user,password,host,port,database):
        super().__init__(start_date,end_date,ticker,user,password,host,port,database)
        self.ticker = ticker
        self.start = start_date
        self.end = end_date
        self.date = self.date_sep(self.data)
        self.output =  PdfPages(output_name)
        self.fig = plt.figure(figsize=(10,10))
        self.graph_data()

    def graph_data(self):
        self.price_movement()
        self.price_change()
        self.weekday()
        self.date_graph()
        self.monthly()
        self.hourly()
        print('Complete')
        self.output.close()

    def date_sep(self,data):
        temp = (data['Date'].str.split('-').tolist())
        return ['/'.join(i[1:]) for i in temp]

    def price_change(self):
        plt.plot(self.date,self.data['change'])
        plt.text(0.05,0.95,'This Plot shows the changes in price with relation to the previous' +\
            ' day',transform=self.fig.transFigure)
        plt.xlabel('Date')
        plt.ylabel('Price($) change with relation to previous day')
        plt.xticks(fontsize = 8, rotation = 90)
        self.output.savefig()
        plt.clf()
        return 

    def date_graph(self):
        temp_data = self.data.groupby('Day', as_index = False ).mean()
        # plt.xticks(fontsize=8, rotation=90)
        plt.bar(temp_data['Day'],temp_data['change'], align = 'center')
        plt.xticks(range(5),['Monday','Tuesday','Wednesday','Thursday','Friday'],rotation = 'vertical')
        plt.title('Trend in of change of stock price with day of week')
        plt.xlabel('Day of the week')
        plt.ylabel('Average Price Change($)')
        self.output.savefig()
        plt.clf()
        return 

    def sep_time(self,data,separator,param,new_name,return_index):
        temp  = (data[param].str.split(separator).tolist())
        data[new_name] = [value[return_index] for value in temp]
        return data

    def hourly(self):
        new_data = self.sep_time(self.data,':','Time','hour',0)
        new_data = new_data.groupby('hour', as_index = False).mean()
        plt.title('Average Hourly Price Change')
        plt.xticks(fontsize=8, rotation=90)
        txt = 'The average price change for each hour between ' + self.start + ' and ' + self.end 
        plt.xlabel('Date')
        plt.ylabel('Average Hourly Price($)')
        plt.text(0.1, 0.95, txt, transform = self.fig.transFigure)
        plt.bar(new_data['hour'],new_data['change'], align = 'center')
        plt.xticks(range(len(new_data['hour'])),[i for i in new_data['hour']],rotation = 'vertical')
        self.output.savefig()
        plt.clf()
        return 

    def monthly(self):
        new_data = self.sep_time(self.data,'-','Date','month',1)
        new_data = new_data.groupby('month',as_index = False).mean()
        plt.title('Average Monthly price Increment')
        plt.xticks(fontsize=8, rotation=90)
        txt = 'The average price change per month between ' + self.start + ' and ' + self.end 
        plt.xlabel('Date')
        plt.bar(new_data['month'],new_data['change'], align = 'center')
        plt.xticks(range(len(new_data['month'])),[i for i in new_data['month']],rotation = 'vertical')
        plt.ylabel('Average Monthly Price($)')
        plt.text(0.1, 0.95, txt, transform = self.fig.transFigure)
        self.output.savefig()
        plt.clf()
        return

    def weekday(self):
        temp_data = self.data.groupby('Date', as_index = False ).mean()
        plt.title('Daily price movement')
        plt.xticks(fontsize=8, rotation=90)
        txt = 'The average price change per day between ' + self.start + ' and ' + self.end 
        plt.xlabel('Date')
        plt.ylabel('Average Daily Price($)')
        plt.text(0.05,0.95,txt,transform=self.fig.transFigure)
        plt.plot(self.date_sep(temp_data),temp_data['Price'])
        self.output.savefig()
        plt.clf()
        return
        

    def price_movement(self):
        # price movement for last week
        plt.plot(self.date,self.data['Price'])
        plt.xticks(fontsize=8, rotation=90)
        plt.title('In depth Price Movement')
        plt.xlabel('Date')
        plt.ylabel('Price($)')
        txt = 'The price movement from ' + self.start + ' to ' + self.end 
        plt.text(0.05,0.95,txt,transform=self.fig.transFigure)
        self.output.savefig()
        plt.clf()
        return 

if __name__ == "__main__":
    graph(*sys.argv[1:])