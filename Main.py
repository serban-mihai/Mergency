import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

import kivy
from Database import Database
from kivy.app import App
from functools import partial
from kivy.uix.popup import Popup
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
        db.add_bound_H_A(1, 1)
        db.add_hospital(1, "Spitalul Judetean", "Calea Unirii", 1)
        db.add_hospital(2, "Spitalul Judetean", "Calea Unirii")
        db.get_info("Accident", "accident_id", "city", "adress", "reason")
        # 
        db.get_info("Hospital", "hospital_id", "name", "adress", "ambulance_id")
        db.rollback_tables(DB_SCHEMA)
    else:
        pass
    db.disconnect()

    def stop(self, *largs):
        # Open the popup you want to open and declare callback if user pressed `Yes`
        popup = ExitPopup(title="Are you sure?")
        popup.bind(on_confirm=partial(self.close_app, *largs))
        popup.open()

    def close_app(self, *largs):   
        super(Mergency, self).stop(*largs)

    def build(self):
        return ManageTab()

class ExitPopup(Popup):
    def __init__(self, **kwargs):
        super(ExitPopup, self).__init__(**kwargs)
        self.register_event_type('on_confirm')

    def on_confirm(self):
        pass

    def on_button_yes(self):
        self.dispatch('on_confirm')
        
if(__name__ == "__main__"):
    Mergency().run()