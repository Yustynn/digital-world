import kivy

from kivy.app           import App
from kivy.clock         import Clock
from kivy.properties    import NumericProperty   
from kivy.uix.widget    import Widget

#from logic.fb import get_temp

kivy.require('1.9.1')

class RootWidget(Widget):
    def __init__(self):
        super(RootWidget, self).__init__()

        self.ideal_temp = 30.0
        self.power      = 0
        self.temp       = NumericProperty(30.0)


    def update(self):
        self.temp = get_temp()
#        self.update()

class CurrentData(Widget):
    pass

class GUIApp(App):
    build = lambda s: RootWidget()

if __name__ == '__main__':
    GUIApp().run()
