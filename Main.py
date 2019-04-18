import kivy
from Database import Database
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget

__author__ = "Serban Mihai-Ciprian"

class ManageTab(Widget):
    # def __init__(self, **kwargs):
    #     super(ManageTab, self).__init__(*kwargs)
    #     self.rows = 2
    #     self.cols = 2
    #     self.add_widget(Label(text="Mergency Test"))
    pass

class Mergency(App):
    db = Database("80.96.123.131", "ora09", "1521", "hr", "oracletest")
    db.connect()
    if(db.conn != None):
        db.drop_table("Serban_Test")
    else:
        pass
    db.disconnect()
    def build(self):
        return ManageTab()
        
if(__name__ == "__main__"):
    Mergency().run()