import pandas as pd
import matplotlib.pyplot as plt 
import sys
from matplotlib.backends.backend_pdf import PdfPages
sys.path.append("../")
from Report_Generation.transform import transform
      
class graph(transform):

    def __init__(self,output_name,start_date,end_date,ticker):
        super().__init__(start_date,end_date,ticker)
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
        xlabels = 'Date'
        ylabels = 'Price($) change with relation to previous day'
        msg = 'This Plot shows the changes in price with relation to the previous day'
        self.normal_graph('Price Change', self.date,self.data['change'],msg,xlabels,ylabels)
        return 

    def date_graph(self):
        temp_data = self.data.groupby('Day', as_index = False ).mean()
        bar_x = temp_data['Day']
        bar_y = temp_data['change']
        xticks_range = range(5)
        xticks_data = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        name = 'Trend in of change of stock price with day of week'
        xlabels = 'Day of the week'
        ylabels = 'Average Price Change($)'
        self.bar_graph(name,xlabels,ylabels,bar_x,bar_y,xticks_range,xticks_data,'')
        return 

    def normal_graph(self,name,plot_x,plot_y,text_msg,xlabels,ylabels):
        plt.plot(plot_x,plot_y)
        plt.text(.05,.95,text_msg,transform=self.fig.transFigure)
        plt.xlabel(xlabels)
        plt.title(name)
        plt.ylabel(ylabels)
        plt.xticks(fontsize = 8, rotation = 90)
        plt.title(name)
        self.output.savefig()
        plt.clf()
        print(name + ' finished')
        return 

    def sep_time(self,data,separator,param,new_name,return_index):
        temp  = (data[param].str.split(separator).tolist())
        data[new_name] = [value[return_index] for value in temp]
        return data
    
    def hourly(self):
        new_data = self.sep_time(self.data,':','Time','hour',0)
        new_data = new_data.groupby('hour', as_index = False).mean()
        name = 'Average Hourly Price Change'
        txt = 'The average price change for each hour between ' + self.start + ' and ' + self.end 
        xlabels = 'Hour'
        ylabels = 'Average Hourly Price($)'
        bar_x = new_data['hour']
        bar_y = new_data['change']
        x_range = range(len(new_data['hour']))
        x_data = [i for i in new_data['hour']]
        self.bar_graph(name,xlabels,ylabels,bar_x,bar_y,x_range,x_data,txt)
        return 

    def monthly(self):
        new_data = self.sep_time(self.data,'-','Date','month',1)
        new_data = new_data.groupby('month',as_index = False).mean()
        name = 'Average Monthly price Increment'
        txt = 'The average price change per month between ' + self.start + ' and ' + self.end 
        xlabels = 'Month'
        bar_x = new_data['month']
        bar_y = new_data['change']
        xtick_range = range(len(new_data['month']))
        xtick_data = [i for i in new_data['month']]
        ylabels = 'Average Monthly Price($)'
        self.bar_graph(name, xlabels, ylabels,bar_x,bar_y,xtick_range,xtick_data, txt)
        return

    def bar_graph(self,name, x_name,y_name, bar_x,bar_y,xtick_range,xtick_data,txt):
        plt.text(.05,.95,txt,transform=self.fig.transFigure)
        plt.bar(bar_x,bar_y, align = 'center')
        plt.ylabel(y_name)
        plt.xlabel(x_name)
        plt.title(name)
        plt.xticks(xtick_range,xtick_data,rotation = 'vertical')
        self.output.savefig()
        plt.clf()
        print(name + ' complete')
        return
        

    def weekday(self):
        temp_data = self.data.groupby('Date', as_index = False ).mean()
        txt = 'The average price change per day between ' + self.start + ' and ' + self.end 
        xlabels = 'Date'
        ylabels = 'Average Daily Price($)'
        plot_x = self.date_sep(temp_data)
        plot_y = temp_data['Price']
        self.normal_graph('Daily price movement',plot_x,plot_y,txt,xlabels,ylabels)
        return
        

    def price_movement(self):
        # price movement for last week
        plot_x = self.date
        plot_y = self.data['Price']
        xlabels = 'Date'
        ylabels = 'Price($)'
        txt = 'The price movement from ' + self.start + ' to ' + self.end 
        self.normal_graph('In depth Price Movement',plot_x,plot_y,txt,xlabels,ylabels)
        return

if __name__ == "__main__":
    graph(*sys.argv[1:])