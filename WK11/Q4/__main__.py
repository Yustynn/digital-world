import kivy

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.app import App

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class MainApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.current = 'menu'

        return sm


if __name__ == '__main__':
    MainApp().run()
