# kivy mods
import kivy

from kivy.app           import App
from kivy.clock         import Clock
from kivy.properties    import ObjectProperty
from kivy.uix.widget    import Widget

### SETUP ###
kivy.require('1.9.1') # could propably go even earlier, but just in case

class RootWidget(Widget):
    state = ObjectProperty(None)

class CurrentData(Widget):
    pass

class GUIApp(App):
    build = lambda s: RootWidget()

if __name__ == '__main__':
    GUIApp().run()
