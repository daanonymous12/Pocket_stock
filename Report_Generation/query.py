import sys
import pandas as pd 
sys.path.append("../")
from creden.connect_db import connect_db
import psycopg2

class query(connect_db):
    def __init__(self, start_date,end_date,ticker):
        super().__init__()
        self.raw_data = self.query_data(start_date, end_date, ticker)

    def query_data(self, start_date, end_date, ticker):
        select_statement = "select * from stock_data as s\
                             where s.ticker = %s and date(s.date)\
                                 between date(%s) and date(%s)\
                                     order by s.date asc"
        self.cursor.execute(select_statement,(ticker,start_date,end_date))
        data = pd.DataFrame(self.cursor.fetchall())
        data.columns = ['Ticker','Day', 'Date', 'Price']
        data['Price'] = data['Price'].round(2)
        return data