from kivy.clock         import Clock

# kivy community mods
from kivy.garden.graph  import Graph, LinePlot

from State              import state, unblock
from constants          import BLUE, GREEN, ORANGE, UPDATE_INTERVAL


# I am a bad bad man who copy pasted instead of abstracting for the code
# shared between TemperatureGraph and PowerGraph. Hopefully I will undo
# my sin later.
 
class TemperatureGraph(Graph):
    def __init__(self, **kwargs):
        super(TemperatureGraph, self).__init__(**kwargs)

        plot = LinePlot(color=ORANGE)
        plot.points = state.temp_history.points
        self.add_plot(plot)
        self.temp_plot = plot

        plot = LinePlot(color=GREEN)
        plot.points = state.temp_history.points
        self.add_plot(plot)

        self.target_temp_plot = plot
        Clock.schedule_interval(self.update, UPDATE_INTERVAL)

    def update(self, _):
        # refresh points, not sure why they don't just auto
        # update. Possibly being shallow copied?
        points = self.temp_plot.points = state.temp_history.points
        self.target_temp_plot.points = state.target_temp_history.points

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
        Clock.schedule_interval(self.update, UPDATE_INTERVAL)

    def update(self, _):
        points = self.plot.points = state.power_history.points
        xs = [point[0] for point in points]

        self.xmin, self.xmax = min(xs), max(xs)

        if not self.xmin - self.xmax: # avoid pesky div by 0 errors
            self.xmax += 0.1
