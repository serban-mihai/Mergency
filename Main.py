import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

import kivy
kivy.require('1.10.1')

from Database import Database
from kivy.app import App
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from functools import partial

from Designer import *

__author__ = "Serban Mihai-Ciprian"

# Table creation order must be kept in order to work
DB_SCHEMA = ["Accident", "Hospital", "Ambulance", "Doctor", "Patient", "H_A", "D_P"]

class Mergency(App):
    theme_cls = ThemeManager()
    title = "Mergency"
    
    def build(self):
        main_widget = Builder.load_file(
            os.path.join(os.path.dirname(__file__), "./Mergency.kv")
        )
        # self.theme_cls.theme_style = 'Dark'

        main_widget.ids.text_field_error.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message)
        self.bottom_navigation_remove_mobile(main_widget)
        return main_widget

    def bottom_navigation_remove_mobile(self, widget):
        # Removes some items from bottom-navigation demo when on mobile
        if DEVICE_TYPE == 'mobile':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_2)
        if DEVICE_TYPE == 'mobile' or DEVICE_TYPE == 'tablet':
            widget.ids.bottom_navigation_demo.remove_widget(widget.ids.bottom_navigation_desktop_1)

    def set_error_message(self, *args):
        if len(self.root.ids.text_field_error.text) == 2:
            self.root.ids.text_field_error.error = True
        else:
            self.root.ids.text_field_error.error = False

    def on_pause(self):
        return True

    def on_stop(self):
        pass
        
if(__name__ == "__main__"):
    Mergency().run()
    # db = Database("80.96.123.131", "ora09", "1521", "hr", "oracletest")
    # db.connect()
    # if(db.conn != None):
    #     db.init_tables(DB_SCHEMA)
    #     db.dummy_insert()
    #     db.dummy_select()
    #     db.rollback_tables(DB_SCHEMA)
    #     db.disconnect()
    # else:
    #     pass