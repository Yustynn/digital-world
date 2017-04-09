import kivy

from kivy.app            import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider     import Slider

kivy.require('1.9.1')

class RootWidget():
    pass

class IdealTempSlider(Slider):
    def __init__(self):
        super(IdealTempSlider, self).__init__()
        print self.background_width

class GUIApp(App):
    build = lambda s: RootWidget()

if __name__ == '__main__':
    GUIApp().run()
