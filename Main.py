import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

import kivy
from Database import Database
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget

__author__ = "Serban Mihai-Ciprian"

# Table creation order must be kept in order to work
DB_SCHEMA = ["Accident", "H_A", "D_P", "Hospital", "Ambulance", "Doctor", "Pacient"]

class ManageTab(Widget):
    pass

class Mergency(App):
    db = Database("80.96.123.131", "ora09", "1521", "hr", "oracletest")
    db.connect()
    if(db.conn != None):
        db.init_tables(DB_SCHEMA)
        db.add_accident(1, "Suceava", "Strada Marasesti", "Betivan la Volan")
        db.add_accident(2, "Botosani", "Parcul Mihai Eminescu")
        db.get_info("Accident", "accident_id", "city", "adress", "reason")
        db.rollback_tables(DB_SCHEMA)
    else:
        pass
    db.disconnect()
    def build(self):
        return ManageTab()
        
if(__name__ == "__main__"):
    Mergency().run()