import kivy

from kivy.app        import App
from kivy.uix.button import Button

class Root(Button):
    def __init__(self, **kwargs):
        Button.__init__(self, **kwargs)
        self.texts = ['Programming is fun', 'It is fun to program']
        self.text = self.texts[0]
    
    def on_touch_down(self, _):
       self.text = [t for t in self.texts if t != self.text][0]

class LOL(App):
    build = lambda s: Root()

LOL().run()
