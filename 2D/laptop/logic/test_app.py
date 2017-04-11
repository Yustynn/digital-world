import kivy

from kivy.app           import App
from kivy.clock         import Clock
from kivy.properties    import ListProperty, NumericProperty, StringProperty, Property
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget    import Widget

from time import sleep

from Controller         import Controller

kivy.require('1.9.1') # could propably go even earlier, but just in case

controller = Controller()
controller.start()

class ValueAdjuster(BoxLayout):
    range = ListProperty([0, 100])
    step  = NumericProperty(0.1)
    title = StringProperty('')
    value = NumericProperty(50)


class Root(BoxLayout):
    # listens to value changes and changes controller accordingly

    temp         = NumericProperty(35)
    target_temp  = NumericProperty(30)
    kd           = NumericProperty(0.5286)
    kp           = NumericProperty(1.0991)
    power        = NumericProperty(0)

    def __init__(self, **kwargs):
        BoxLayout.__init__(self, **kwargs)

        self._temp       = 35
        Clock.schedule_interval(self.update, 1./10)

    def on_temp(self, _, val):
        self._temp = val
        controller.temp = val

    def update(self, _):
        # controller.step(self._temp - 0.02)
        # controller.step(self._temp - 0.02)
        # sleep(0.1)
        print self._temp
        controller.step(self._temp)
        self.power = controller.step(self._temp)[0]

    binder = lambda key: lambda self, _, val: controller.set(key, val)
    on_target_temp = binder('target_temp')
    on_kd          = binder('kd')
    on_kp          = binder('kp')



class TestApp(App):
    build = lambda s: Root()

if __name__ == '__main__':
    TestApp().run()
