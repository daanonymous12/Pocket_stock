import random 
import psycopg2
from datetime import datetime, date, timedelta

# data -> ['YI', 3, '2020-07-09-22:44', 6.74],
class simulate:
    """ simulates price for apple at start date and end date
    The price incremental change is completely random instead of 
    random walk because the purpose of this simulation is to generate
    data for mock visualization 
    start and endtime should be in year-month-day-9-30 format where 9-30 is hour,minute
    """

    def __init__(self,start_date,end_date,starting_price,interval,lower_limit,\
        upper_limit,user,password,host,port,database):
        self.cursor = self.database(user,password,host,port,database)
        self.starting_price = starting_price
        self.lower = lower_limit
        self.upper = upper_limit
        self.simulate(self.strip(start_date),self.strip(end_date),interval)

    def strip(self, time):
        return datetime(*[int(i) for i in time.split('-')])
    def database(self,user,password,host,port,database):
        self.connection = psycopg2.connect(user = user,
                                  password = password,
                                  host = host,
                                  port = port,
                                  database = database)
        cursor = self.connection.cursor()
        return cursor
    def price_sim(self, cur_price):
        cur_price = (1 - (10 - random.randint(0,20))/100) * cur_price # 2% max change in price since aapl is large stock
        if cur_price < self.lower * self.starting_price or cur_price > self.upper * self.starting_price:
            cur_price = self.starting_price
        return cur_price
    def simulate(self,start_date,end_date,interval):
        cur_price = self.starting_price
        prices = []
        minute_incre = timedelta(minutes = 60/interval)
        delta = timedelta(days = 1)
        while start_date <= end_date:
            dates = datetime.weekday(start_date)
            prices = []
            if dates < 5: # weekdays
                temp = start_date
                while temp <= start_date + timedelta(hours = 7, minutes = 30): # interval is # of times one wish to scan per hour
                    cur_price = self.price_sim(cur_price)
                    prices.append(['AAPL',dates,str(temp),cur_price])
                    temp += minute_incre
            start_date += delta
            self.writetodb(prices)
        print('Simulation Finished')

    def writetodb(self,prices):
        postgres_insert_query = """ INSERT INTO stock_data (ticker,Day,Date,Price) VALUES (%s,%s,%s,%s)"""
        self.cursor.executemany(postgres_insert_query, prices)
        self.connection.commit()
        count = self.cursor.rowcount
        print (count, "Record inserted successfully into table")

simulate('2019-01-01-9-30','2019-12-30-9-30',144,12,.6,3,'da','','localhost','5432','da')