from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.config import Config

from kivymd.list import BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase

__author__ = "Serban Mihai-Ciprian"

# Kivy Window Proprieties
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '850')
Config.set('graphics', 'height', '500')

class HackedDemoNavDrawer(MDNavigationDrawer):
    # DO NOT USE
    def add_widget(self, widget, index=0):
        if(issubclass(widget.__class__, BaseListItem)):
            self._list.add_widget(widget, index)
            if len(self._list.children) == 1:
                widget._active = True
                self.active_item = widget
            # widget.bind(on_release=lambda x: self.panel.toggle_state())
            widget.bind(on_release=lambda x: x._set_active(True, list=self))
        elif(issubclass(widget.__class__, NavigationDrawerHeaderBase)):
            self._header_container.add_widget(widget)
        else:
            super(MDNavigationDrawer, self).add_widget(widget, index)