import kivy

from kivy.app        import App
from kivy.uix.button import Button

class Root(Button):
    def __init__(self, **kwargs):
        Button.__init__(self, **kwargs)
        self.text = 'Slide me'
    
    def on_touch_move(self, touch):
        dx, dy = touch.dx, touch.dy
        if dx > 0 and dy > 0:
            if dx > dy:
                self.text = 'Slide right'
            else:
                self.text = 'Slide up'
        elif dy > 0:
            self.text = 'Slide up'
        elif dx > 0:
            self.text = 'Slide right'
class LOL(App):
    build = lambda s: Root()

LOL().run()
