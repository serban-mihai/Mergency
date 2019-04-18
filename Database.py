import cx_Oracle
from Colors import *

__author__ = "Serban Mihai-Ciprian"

class Database():
    def __init__(self, host, name, port, user, password):
        self.host = host
        self.name = name
        self.port = port
        self.user = user
        self.password = password
        self.conn = None
        self.curr = None
        # self.is_connected = False

    def connect(self):
        try:
            dsn = cx_Oracle.makedsn(self.host, self.port, service_name=f"{self.name}")
            self.conn = cx_Oracle.connect(self.user, self.password, dsn)
            # self.is_connected = True
            print(f"> DEBUG: {OK}Connected{END} ")
        except cx_Oracle.Error as err:
            print(f"> DEBUG: {ERR}{err}{END}")
        except Exception as ex:
            print(f"> DEBUG: {ERR}{ex}{END}")
        return

    def disconnect(self):
        self.conn.close()
        self.conn = None
        #self.is_connected = False
        print(f"> DEBUG: {WAR}Disconnected{END}")
        return
        
    def query(self, string):
        if(self.conn != None):
            try:
                # Get requested data from DB ===================
                self.curr = self.conn.cursor()
                self.curr.execute(string)
                # result = self.curr.fetchmany(numRows=3)
                # result = self.curr.fetchall()
                # result = self.curr.fetchone()
                # Get requested data from DB ===================
                print(f"> DEBUG: {OK}Query OK{END} ")
            except Exception as ex:
                print(f"> DEBUG: {ERR}{ex}{END}")
        else:
            print(f"> DEBUG: {WAR}Query Failed!{END}")
        return

    def create_table(self, name, *args):
        q = f"CREATE TABLE IF NOT EXISTS {name}"
        self.query(q)
        return 
    
    def drop_table(self, name):
        q = f"DROP TABLE {name}"
        self.query(q)
        return 