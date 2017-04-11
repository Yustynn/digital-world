import kivy

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.app import App

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)

        self.add_widget(Button(text='lol'))

class SettingsScreen(Screen):
    pass

class MainApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.current = 'menu'


if __name__ == '__main__':
    MainApp().run()
