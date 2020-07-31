import sys
import pandas as pd 
sys.path.append("../")
from Report_Generation.query import query

class transform(query):
    def __init__(self,start_date,end_date,ticker):
        super().__init__(start_date,end_date,ticker)
        self.data = self.update_data()

    def update_data(self):
        data = self.data_feature(self.raw_data)
        return data

    def data_feature(self, data):
        data = self.time_mod(data)
        data['change'] = data['Price'].diff()
        data['change'].loc[0] = 0
        return data

    def time_mod(self,data):
        new_data = data.filter(['Day','Price'])
        temp = pd.DataFrame(data['Date'].str.split(' ').tolist())
        new_data['Date'],new_data['Time'] = temp[0],temp[1]
        return new_data 