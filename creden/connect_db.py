import psycopg2
import sys
sys.path.append("../")
from creden.credential import cred

class connect_db(cred):
    def __init__(self):
        super().__init__()
        self.cursor = self.connect()

    def connect(self):
        self.connection = psycopg2.connect(user = self.user,
                                    password = self.password,
                                    host = self.host,
                                    port = self.port,
                                    database = self.database)
        return self.connection.cursor()
