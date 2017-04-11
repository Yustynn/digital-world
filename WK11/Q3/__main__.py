import kivy

from kivy.app        import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout 
from kivy.properties import NumericProperty, StringProperty

class Root(BoxLayout):
    future_val = NumericProperty(0)

class Row(BoxLayout):
    val= NumericProperty(0) 
    label = StringProperty('')

class FutureApp(App):
    build = lambda s: Root()

FutureApp().run()
