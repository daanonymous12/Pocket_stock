import psycopg2

class postgres_setup:
    def __init__(self,user,password,host,port,database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.create_table()

    def create_table(self):
        connection = psycopg2.connect(user = self.user,
                                  password = self.password,
                                  host = self.host,
                                  port = self.port,
                                  database = self.database)
        cursor = connection.cursor()
        create_table_query = '''CREATE TABLE stock_data
          (ticker TEXT    NOT NULL,
          Day           TEXT    Not Null,
          Date          TEXT     NOT NULL, 
          PRICE         float); '''

        cursor.execute(create_table_query)
        connection.commit()
        print('Table Created')
a = postgres_setup('da','','localhost','5432','da')
