from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, Clock
from tracker import Tracker
import threading
from kivy.lang import Builder
from abc import ABC, abstractmethod
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout

Builder.load_file('layout_ex.kv')

class BoxLayoutMain(BoxLayout):
    exercise = StringProperty()
    tracker = Tracker("")
    
    menu_counter = StringProperty()
    menu_angle = StringProperty()
    menu_state = StringProperty()
    button_stage = StringProperty()

    tracker_started = False

    def __init__(self, **kwargs):
        super(BoxLayoutMain, self).__init__(**kwargs)
        self.init_menu()
        self.init_tracker()

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    @abstractmethod
    def init_tracker(self):
        pass

    def init_menu(self):
        self.menu_counter = "Counter: 0"
        self.menu_angle = "Angle"
        self.menu_state = "State"
        self.button_stage = "Start Tracker"

    def update(self, dt):
        self.exercise = self.tracker.exercise
        if self.tracker_started:
            self.menu_angle = str(self.tracker.angle)
            self.menu_counter = "Counter: " + str(self.tracker.counter)
            self.menu_state = self.tracker.stage
        

    def on_click_tracker(self):
        t = threading.Thread(target=self.tracker.main)

        self.tracker.switch_state()
        t.start()
        self.tracker_started = not self.tracker_started

        if self.tracker_started:
            self.button_stage = "Stop Tracker"
        else:
            self.init_menu()
            self.button_stage = "Start Tracker"

class ShoulderLayout(BoxLayoutMain):
    def init_tracker(self):
        self.tracker = Tracker('shoulder')
        self.exercse = 'shoulder'

class BicepLayout(BoxLayoutMain):
    def init_tracker(self):
        self.tracker = Tracker('bicep')
        self.excercise = 'bicep'


class StackLayoutExample(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.orientation = "lr-bt"
        for i in range(0, 100):
            #size = dp(100) + i*10
            size = dp(100)
            b = Button(text=str(i+1), size_hint=(None, None), size=(size, size))
            self.add_widget(b)