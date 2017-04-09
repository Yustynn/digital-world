# kivy mods
import kivy

from kivy.app           import App
from kivy.clock         import Clock
from kivy.properties    import ListProperty, ObjectProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label     import Label
from kivy.uix.widget    import Widget

# kivy community mods
from kivy.garden.graph  import Graph, LinePlot

# personal kivy mods
from State              import state, unblock

# other personal mods
from colors             import BLUE, GREEN, ORANGE

### SETUP ###
kivy.require('1.9.1') # could propably go even earlier, but just in case

# I made a central source of truth. Don't like how kivy handles state
class RootWidget(Widget):
    state = ObjectProperty(state)

class DataDisplayRow(BoxLayout):
    color = ListProperty(None)
    data = NumericProperty(0)
    label = StringProperty('')


class TemperatureGraph(Graph):
    def __init__(self, **kwargs):
        super(TemperatureGraph, self).__init__(**kwargs)

        plot = LinePlot(color=ORANGE)
        plot.points = state.temp_history.points
        self.add_plot(plot)


        self.plot = plot
        Clock.schedule_interval(self.update, 1./10)

    def update(self, _):
        points = self.plot.points = state.temp_history.points
        xs = [point[0] for point in points]

        self.xmin, self.xmax = min(xs), max(xs)

        if not self.xmin - self.xmax: # avoid pesky div by 0 errors
            self.xmax += 0.1


# I did a bad thing and copy pasted. Will figure out how to DRY later (hopefully)
class PowerGraph(Graph):
    def __init__(self, **kwargs):
        super(PowerGraph, self).__init__(**kwargs)

        plot = LinePlot(color=BLUE)
        plot.points = state.power_history.points
        self.add_plot(plot)

        self.plot = plot
        Clock.schedule_interval(self.update, 1./10)

    def update(self, _):
        points = self.plot.points = state.power_history.points
        xs = [point[0] for point in points]

        self.xmin, self.xmax = min(xs), max(xs)

        if not self.xmin - self.xmax: # avoid pesky div by 0 errors
            self.xmax += 0.1


class GUIApp(App):
    build = lambda s: RootWidget()


if __name__ == '__main__':
    GUIApp().run()
