# kivy mods
import kivy

from kivy.app           import App
from kivy.clock         import Clock
from kivy.properties    import ListProperty, ObjectProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget    import Widget

# personal kivy mods
from State              import state, unblock
from graphs             import PowerGraph, TemperatureGraph

# other personal mods
from constants          import SIM_MODE, UPDATE_INTERVAL
from logic.Controller   import Controller

### SETUP ###
kivy.require('1.9.1') # could propably go even earlier, but just in case

UPDATE_INTERVAL = 1.0/60

# I made a central source of truth. Don't like how kivy handles state
class RootWidget(Widget):
    state = ObjectProperty(state)

class DataDisplayRow(BoxLayout):
    color = ListProperty(None)
    data  = NumericProperty(0)
    label = StringProperty('')
    unit  = StringProperty('')

class MainContent(BoxLayout):
    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)

        if SIM_MODE:
            self.add_widget(SimDataDisplay())

class SimDataDisplay(BoxLayout):
    state = ObjectProperty(state)

class GUIApp(App):
    def __init__(self, **kwargs):
        App.__init__(self, **kwargs)

        self.controller = Controller(target_temp = state.target_temp)
        self.controller.start()

        Clock.schedule_interval(self.update, UPDATE_INTERVAL)

    def build(self):
        root = RootWidget()

        return root

    def update(self, _):
        controller = self.controller
        controller.target_temp = state.target_temp

        power = controller.step(state.temp).pump
        state.set('power', power)


if __name__ == '__main__':
    GUIApp().run()
