import cx_Oracle
import re
import inspect
from Colors import *

__author__ = "Serban Mihai-Ciprian"

PFIX = "Serban_"

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

    # Utilities for Oracle DB Connection =====================================================
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
        print(f"> DEBUG: {OK}Disconnected{END}")
        return
    
    # Base Method for SQL Queries ============================================================
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
            print(f"> DEBUG: {WAR}Connection Lost!{END}")
        return

    # Table Schema Management Methods ========================================================
    def init_tables(self, args):
        tables = []
        tables.append(f"CREATE TABLE {PFIX}{args[0]} (          \
                        accident_id NUMBER PRIMARY KEY,         \
                        city VARCHAR(50) NOT NULL,              \
                        adress VARCHAR(70) NOT NULL,            \
                        reason VARCHAR(100) DEFAULT 'Unknown'   \
                        )")
        tables.append(f"CREATE TABLE {PFIX}{args[1]} (              \
                        hospital_id NUMBER NOT NULL UNIQUE,         \
                        ambulance_id NUMBER NOT NULL UNIQUE        \
                        )")
        tables.append(f"CREATE TABLE {PFIX}{args[2]} (      \
                        doctor_id NUMBER NOT NULL UNIQUE,   \
                        patient_id NUMBER NOT NULL UNIQUE   \
                        )")
        tables.append(f"CREATE TABLE {PFIX}{args[3]} (                          \
                        hospital_id NUMBER PRIMARY KEY,                         \
                        name VARCHAR(50) NOT NULL,                              \
                        adress VARCHAR(70) NOT NULL,                            \
                        ambulance_id NUMBER REFERENCES {PFIX}H_A(ambulance_id)  \
                        )")
        tables.append(f"CREATE TABLE {PFIX}{args[4]} (                                  \
                        ambulance_id NUMBER PRIMARY KEY,                                \
                        model VARCHAR(50) NOT NULL,                                     \
                        capacity NUMBER DEFAULT 5 NOT NULL,                             \
                        license_plate VARCHAR(7) NOT NULL,                              \
                        dispatched NUMBER(1) DEFAULT 0 NOT NULL,                        \
                        hospital_id NUMBER REFERENCES {PFIX}H_A(hospital_id)            \
                        )")
        tables.append(f"CREATE TABLE {PFIX}{args[5]} (                                  \
                        doctor_id NUMBER PRIMARY KEY,                                   \
                        name VARCHAR(50) NOT NULL,                                      \
                        surname VARCHAR(50) NOT NULL,                                   \
                        birthday DATE NOT NULL,                                         \
                        available NUMBER(1) DEFAULT 0 NOT NULL,                         \
                        patient_id NUMBER REFERENCES {PFIX}D_P(patient_id)              \
                        )")
        tables.append(f"CREATE TABLE {PFIX}{args[6]} (                                          \
                        patient_id NUMBER PRIMARY KEY,                                          \
                        name VARCHAR(50) DEFAULT 'Unknown' NOT NULL,                            \
                        surname VARCHAR(50) DEFAULT 'Unknown' NOT NULL,                         \
                        birthday DATE,                                                          \
                        blood_type VARCHAR(2),                                                  \
                        rh VARCHAR(1),                                                          \
                        ambulance_id NUMBER REFERENCES {PFIX}Ambulance(ambulance_id),           \
                        accident_id NUMBER REFERENCES {PFIX}Accident(accident_id),              \
                        doctor_id NUMBER REFERENCES {PFIX}D_P(doctor_id)                        \
                        )")
        for num, table in enumerate(tables, 0):
            print(f"> DEBUG: Creating table: {WAR}{PFIX}{args[num]}{END}")
            self.query(table)
        return 
    
    def rollback_tables(self, args):
        for table in reversed(args):
            print(f"> DEBUG: Dropping table: {WAR}{PFIX}{table}{END}")
            self.query(f"DROP TABLE {PFIX}{table}")
        return

    # Dedicated Methods fo INSERT like queries ===============================================
    def add_accident(self, accident_id, city, adress, reason='Unknown'):
        arguments = str(inspect.getfullargspec(self.add_accident)[0]).replace("['self', ", "")
        columns = re.sub("[\[\]']", "", arguments)
        print(f"> DEBUG: Inserting Into: {WAR}{PFIX}Accident{END}")
        self.query(f"INSERT INTO {PFIX}Accident ({columns}) \
                     VALUES({accident_id}, '{city}', '{adress}', '{reason}')")
        self.conn.commit()
        return

    def add_hospital(self, hospital_id, name, adress, ambulance_id=None):
        arguments = str(inspect.getfullargspec(self.add_accident)[0]).replace("['self', ", "")
        columns = re.sub("[\[\]']", "", arguments)
        print(f"> DEBUG: Inserting Into: {WAR}{PFIX}Hospital{END}")
        self.query(f"INSERT INTO {PFIX}Accident ({columns}) \
                     VALUES({hospital_id}, '{name}', '{adress}', '{ambulance_id}')")
        self.conn.commit()
        return

    def add_bound_H_A(self, hospital_id, ambulance_id):
        arguments = str(inspect.getfullargspec(self.add_accident)[0]).replace("['self', ", "")
        columns = re.sub("[\[\]']", "", arguments)
        print(f"> DEBUG: Inserting Into: {WAR}{PFIX}H_A{END}")
        self.query(f"INSERT INTO {PFIX}Accident ({columns}) \
                     VALUES({hospital_id}, {ambulance_id})")
        self.conn.commit()
        return
    
    # Universal Method for SELECT like queries ===============================================
    def get_info(self, table_name, *args):
        if(len(args) == 1):
            data = re.sub("[()',]", "", str(args))
        else:
            data = re.sub("[()']", "", str(args))
        print(f"> DEBUG: Getting {data} From {WAR}{PFIX}{table_name}{END}")
        self.query(f"SELECT {data}  \
                     FROM {PFIX}{table_name}")
        res = self.curr.fetchall()
        print(res)
        return