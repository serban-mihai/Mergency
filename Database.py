import cx_Oracle
import re
import inspect
from pprint import pprint
from datetime import datetime
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

    # Utilities for Oracle DB Connection =====================================================
    def connect(self):
        try:
            dsn = cx_Oracle.makedsn(self.host, self.port, service_name=f"{self.name}")
            self.conn = cx_Oracle.connect(self.user, self.password, dsn)
            # self.is_connected = True
            print(f"> DEBUG: {OK}Connected{END} ")
            return
        except cx_Oracle.Error as err:
            print(f"> DEBUG: {ERR}{err}{END}")
            return
        except Exception as ex:
            print(f"> DEBUG: {ERR}{ex}{END}")
            return

    def disconnect(self):
        try:
            self.conn.close()
            self.conn = None
            print(f"> DEBUG: {OK}Disconnected{END}")
            return
        except Exception as ex:
            print(f"> DEBUG: {ERR}{ex}{END}")
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
            print(f"> DEBUG: {ERR}Connection Lost!{END}")
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
        tables.append(f"CREATE TABLE {PFIX}{args[1]} (                          \
                        hospital_id NUMBER PRIMARY KEY,                         \
                        name VARCHAR(50) NOT NULL,                              \
                        adress VARCHAR(70) NOT NULL                            \
                        )")
        tables.append(f"CREATE TABLE {PFIX}{args[2]} (                                  \
                        ambulance_id NUMBER PRIMARY KEY,                                \
                        model VARCHAR(50) NOT NULL,                                     \
                        license_plate VARCHAR(10) NOT NULL,                              \
                        capacity NUMBER DEFAULT 5 NOT NULL,                             \
                        dispatched NUMBER(1) DEFAULT 0 NOT NULL                        \
                        )")
        tables.append(f"CREATE TABLE {PFIX}{args[3]} (                                  \
                        doctor_id NUMBER PRIMARY KEY,                                   \
                        name VARCHAR(50) NOT NULL,                                      \
                        surname VARCHAR(50) NOT NULL,                                   \
                        sex VARCHAR(1) DEFAULT 'M' NOT NULL,                                      \
                        birthday DATE NOT NULL,                                         \
                        available NUMBER(1) DEFAULT 0 NOT NULL                         \
                        )")
        tables.append(f"CREATE TABLE {PFIX}{args[4]} (                                          \
                        patient_id NUMBER PRIMARY KEY,                                          \
                        name VARCHAR(50) DEFAULT 'Unknown' NOT NULL,                            \
                        surname VARCHAR(50) DEFAULT 'Unknown' NOT NULL,                         \
                        sex VARCHAR(1) DEFAULT 'M' NOT NULL,                         \
                        birthday DATE,                                                          \
                        blood_type VARCHAR(2),                                                  \
                        rh VARCHAR(1),                                                          \
                        ambulance_id NUMBER REFERENCES {PFIX}Ambulance(ambulance_id),           \
                        accident_id NUMBER REFERENCES {PFIX}Accident(accident_id)              \
                        )")
        tables.append(f"CREATE TABLE {PFIX}{args[5]} (              \
                        hospital_id NUMBER NOT NULL REFERENCES {PFIX}Hospital(hospital_id) ON DELETE CASCADE,         \
                        ambulance_id NUMBER NOT NULL REFERENCES {PFIX}Ambulance(ambulance_id) ON DELETE CASCADE,        \
                        PRIMARY KEY(hospital_id, ambulance_id)        \
                        )")
        tables.append(f"CREATE TABLE {PFIX}{args[6]} (      \
                        doctor_id NUMBER NOT NULL REFERENCES {PFIX}Doctor(doctor_id) ON DELETE CASCADE,   \
                        patient_id NUMBER NOT NULL REFERENCES {PFIX}Patient(patient_id) ON DELETE CASCADE,   \
                        PRIMARY KEY(doctor_id, patient_id)        \
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

    # Dedicated Methods for INSERT like queries ===============================================
    def add_accident(self, accident_id, city, adress, reason='Unknown'):
        arguments = str(inspect.getfullargspec(self.add_accident)[0]).replace("['self', ", "")
        columns = re.sub("[\[\]']", "", arguments)
        print(f"> DEBUG: Inserting {columns} Into: {WAR}{PFIX}Accident{END}")
        self.query(f"INSERT INTO {PFIX}Accident ({columns}) \
                     VALUES({accident_id}, '{city}', '{adress}', '{reason}')")
        try:
            self.conn.commit()
        except Exception:
            pass
        return

    def add_hospital(self, hospital_id, name, adress):
        arguments = str(inspect.getfullargspec(self.add_hospital)[0]).replace("['self', ", "")
        columns = re.sub("[\[\]']", "", arguments)
        print(f"> DEBUG: Inserting {columns} Into: {WAR}{PFIX}Hospital{END}")
        self.query(f"INSERT INTO {PFIX}Hospital ({columns}) \
                     VALUES({hospital_id}, '{name}', '{adress}')")
        try:
            self.conn.commit()
        except Exception:
            pass
        return

    def add_ambulance(self, ambulance_id, model, license_plate, capacity=5, dispatched=0):
        arguments = str(inspect.getfullargspec(self.add_ambulance)[0]).replace("['self', ", "")
        columns = re.sub("[\[\]']", "", arguments)
        print(f"> DEBUG: Inserting {columns} Into: {WAR}{PFIX}Ambulance{END}")
        self.query(f"INSERT INTO {PFIX}Ambulance ({columns}) \
                     VALUES({ambulance_id}, '{model}', '{license_plate}', {capacity}, {dispatched})")
        try:
            self.conn.commit()
        except Exception:
            pass
        return

    def add_doctor(self, doctor_id, name, surname, sex, birthday, available=1):
        arguments = str(inspect.getfullargspec(self.add_doctor)[0]).replace("['self', ", "")
        columns = re.sub("[\[\]']", "", arguments)
        print(f"> DEBUG: Inserting {columns} Into: {WAR}{PFIX}Doctor{END}")
        self.query(f"INSERT INTO {PFIX}Doctor ({columns}) \
                     VALUES({doctor_id}, '{name}', '{surname}', '{sex}', {birthday}, {available})")
        try:
            self.conn.commit()
        except Exception:
            pass
        return

    def add_patient(self, patient_id, name, surname, sex, birthday, blood_type, rh, ambulance_id=None, accident_id=None):
        arguments = str(inspect.getfullargspec(self.add_patient)[0]).replace("['self', ", "")
        columns = re.sub("[\[\]']", "", arguments)
        print(f"> DEBUG: Inserting {columns} Into: {WAR}{PFIX}Patient{END}")
        self.query(f"INSERT INTO {PFIX}Patient ({columns}) \
                     VALUES({patient_id}, '{name}', '{surname}', '{sex}', {birthday}, '{blood_type}', '{rh}', {ambulance_id}, {accident_id})")
        try:
            self.conn.commit()
        except Exception:
            pass
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
        try:
            res = self.curr.fetchall()
            pprint(res)
        except Exception:
            pass
        return res

    # Universal Methods for TRUNCATE and DROP like queries ===============================================
    def truncate_table(self, table_name):
        print(f"> DEBUG: Truncating all data From {WAR}{PFIX}{table_name}{END}")
        self.query(f"TRUNCATE TABLE {PFIX}{table_name}")
        try:
            self.conn.commit()
        except Exception:
            pass

    def drop_table(self, table_name):
        print(f"> DEBUG: Dropping table {WAR}{PFIX}{table_name}{END}")
        self.query(f"DROP TABLE {PFIX}{table_name}")
        try:
            self.conn.commit()
            
        except Exception:
            pass

    # Universal Method for DELETE like queries ===============================================
    def delete_record(self, table_name, element_id, condition):
        print(f"> DEBUG: Deleting {element_id} From {WAR}{PFIX}{table_name}{END}")
        self.query(f"DELETE FROM {PFIX}{table_name}  \
                     WHERE {element_id} = {condition}")
        try:
            self.conn.commit()
        except Exception:
            pass
    # DEV TOOLS ===============================================================================
    def dummy_insert(self):
        print(f"{WAR}INSERT ========================================================================{END}")
        # REMEMBER to implement increment id and modify above
        self.add_accident(1, "Suceava", "Strada Marasesti", "Betivan la Volan")
        self.add_accident(2, "Botosani", "Parcul Mihai Eminescu")
        self.add_accident(3, "Suceava", "Strada Tipografiei", "Accident de masina")
        self.add_accident(4, "Suceava", "Bulevardul George Enescu", "Cadere de la etaj")
        self.add_accident(5, "Piatra Neamt", "Strada Florilor")
        self.add_accident(6, "Botosani", "Parcul Voda", "Dezastru natural")
        self.add_accident(7, "Gura Humorului", "Strada Dacilor", "Incendiu in apartament")
        self.add_accident(8, "Suceava", "Bulevardul Victoriei")
        self.add_accident(9, "Suceava", "Strada Cuza")
        self.add_accident(10, "Radauti", "Parcul Carol", "Jaf armat la magazin")
        self.add_hospital(1, "Spitalul Comunal", "Universitate")
        self.add_hospital(2, "Spitalul Judetean", "Calea Unirii")
        self.add_ambulance(1, "Toyota", "SV 12 DAX", 5, 0)
        self.add_ambulance(2, "Audi", "SV 01 RAN")
        self.add_ambulance(3, "Mustang", "SV 43 UNK", 1)
        self.add_ambulance(4, "Dacia", "SV 67 LGD", 0)
        self.add_ambulance(5, "Toyota", "NT 09 DGW", 7, 1)
        self.add_ambulance(6, "Audi", "BT 12 PWN", 10, 0)
        self.add_doctor(1, "Ion", "Vasile", "M", "TO_DATE('1989-12-09','YYYY-MM-DD')", 1)
        self.add_doctor(2, "Bianca", "Cazacu", "F", "TO_DATE('1969-10-22','YYYY-MM-DD')", 0)
        self.add_doctor(3, "Dumitru", "Pelinescu", "M", "TO_DATE('1955-05-09','YYYY-MM-DD')", 1)
        self.add_doctor(4, "Dimitrie", "Random", "M", "TO_DATE('1976-02-09','YYYY-MM-DD')", 1)
        self.add_doctor(5, "Ionela", "Ilote", "F", "TO_DATE('1981-09-09','YYYY-MM-DD')", 1)
        self.add_doctor(6, "Teodora", "Bors", "F", "TO_DATE('1953-08-09','YYYY-MM-DD')", 0)
        self.add_doctor(7, "Mihai", "Ungureanu", "M", "TO_DATE('1977-11-09','YYYY-MM-DD')", 1)
        self.add_patient(1, "Laura", "Popescu", "F", "TO_DATE('1996-03-22','YYYY-MM-DD')", "AB", "+", 1, 1)
        self.add_patient(2, "Oana", "Mosneagu", "F", "TO_DATE('1986-11-04','YYYY-MM-DD')", "0", "-", 1, 1)
        self.add_patient(3, "Marius", "Luparu", "M", "TO_DATE('1954-01-11','YYYY-MM-DD')", "B", "+", 1, 1)
        self.add_patient(4, "Dragos", "Creanga", "M", "TO_DATE('1987-04-01','YYYY-MM-DD')", "A", "-", 1, 1)
        self.add_patient(5, "Mihai-Ciprian", "Serban", "M", "TO_DATE('1944-11-22','YYYY-MM-DD')", "0", "-", 1, 1)
        self.add_patient(6, "Maria", "Tenciu", "F", "TO_DATE('2002-06-28','YYYY-MM-DD')", "0", "+", 1, 1)
        self.add_patient(7, "Diana", "Damian", "F", "TO_DATE('2010-08-21','YYYY-MM-DD')", "AB", "+", 1, 1)
        self.add_patient(8, "Alin", "Rosu", "M", "TO_DATE('2003-10-08','YYYY-MM-DD')", "A", "-", 1, 1)
        self.add_patient(9, "Paul", "Serban", "M", "TO_DATE('2002-06-13','YYYY-MM-DD')", "0", "+", 1, 1)
        self.add_patient(10, "Geanina", "Random", "F", "TO_DATE('1997-03-17','YYYY-MM-DD')", "A", "-", 1, 1)
        self.add_patient(11, "Radu", "Bradea", "M", "TO_DATE('1999-12-09','YYYY-MM-DD')", "B", "+", 1, 1)
        return

    def dummy_select(self):
        print(f"{WAR}SELECT ========================================================================{END}")
        self.get_info("Accident", "accident_id", "city", "adress", "reason")
        self.get_info("Hospital", "hospital_id", "name", "adress")
        self.get_info("Ambulance", "ambulance_id", "model", "license_plate", "capacity", "dispatched")
        self.get_info("Doctor", "*")
        self.get_info("Patient", "*")
        self.get_info("H_A", "*")
        self.get_info("D_P", "*")
        return