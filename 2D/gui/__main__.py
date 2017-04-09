# kivy mods
import kivy

from kivy.app           import App
from kivy.clock         import Clock
from kivy.properties    import ObjectProperty
from kivy.uix.widget    import Widget

from State import state


from math import sin
from kivy.garden.graph import Graph, MeshLinePlot

### SETUP ###
kivy.require('1.9.1') # could propably go even earlier, but just in case

class RootWidget(Widget):
    state = ObjectProperty(state)

class CurrentData(Widget):
    pass

class TemperatureGraph(Widget):
    # graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
    # x_ticks_major=25, y_ticks_major=1,
    # y_grid_label=True, x_grid_label=True, padding=5,
    # x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
    # plot = MeshLinePlot(color=[1, 0, 0, 1])
    # plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
    # graph.add_plot(plot)
    # root.add_widget(graph)
    # def __init__(self):
    #     super(TemperatureGraph, self).__init__()
    #     plot = MeshLinePlot(color=[1, 0, 0, 1])
    #     plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
    #     self.add_plot(plot)
    pass



class GUIApp(App):
    build = lambda s: RootWidget()


if __name__ == '__main__':
    GUIApp().run()
