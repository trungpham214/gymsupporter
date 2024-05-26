from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '900')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button, Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.properties import StringProperty, Clock, NumericProperty, ObjectProperty
from kivy.lang import Builder

# from tracker import main
# from tracker import get_angle
from tracker import Tracker

import threading
import time
#1290, 2796

from navigation_screen_manager import NavigationScreenManager


class MyScreenManager(NavigationScreenManager):
    pass

class SupporterApp(App):
    manager = ObjectProperty(None)

    def build(self):
        self.manager = MyScreenManager()
        return self.manager

def main():
    app = SupporterApp()
    app.run()

if __name__ == '__main__':
    main()