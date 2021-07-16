from typing import Callable, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

import utils.utils as utils
from utils.calibration import ThresholdLine


class Visualizer:
    def __init__(self, draw_fragment: Tuple[int, int] = None):
        axes = None
        if draw_fragment == None:
            _, axes = plt.subplots((8, 8))
        else: 
            _, axes = plt.subplots()
        
        self.axes = axes
        self.fragment = draw_fragment

    def scatter_calibration(self, filename: str, clogscale: bool = True, markersize: float = 0.1, coloring: bool = True):
        (_, temps) = utils.get_field_from_pickle(filename, 'TEMP')

        if coloring:
            (_, temps_sky_disp) = utils.get_field_from_pickle(filename, 'STD_1_2')

            norm = None
        
            if clogscale:
                norm = mpl.colors.LogNorm()

            def action(axes, ix, iy):
                (_, temps_sky) = utils.get_field_from_pickle(filename, f'TEMP_SKY_{ix}_{iy}')
                im = axes.scatter(
                    temps_sky, temps, 
                    s = markersize, c = temps_sky_disp, 
                    cmap = 'plasma', norm = norm
                )
                axes.figure.colorbar(im, ax = axes)

        else:
            def action(axes, ix, iy):
                (_, temps_sky) = utils.get_field_from_pickle(filename, f'TEMP_SKY_{ix}_{iy}')
                axes.plot(temps_sky, temps, 'ro', markersize = markersize)

        self.do_for_each_axes(action)

    def do_for_each_axes(self, action: Callable[[Axes, int, int], None]):
        if self.fragment != None:
            action(self.axes, self.fragment[0], self.fragment[1])
        else:
            for ix, iy in np.ndindex(self.axes.shape):
                action(self.axes[ix, iy], ix, iy)

    def plot_point(self, x, y):
        action = lambda axes, ix, iy: axes.plot(x[ix, iy], y, 'ro')

        self.do_for_each_axes(action)

    def plot_line(self, line: ThresholdLine, start: float, end: float):
        x = np.linspace(start, end, 10)

        action = lambda axes, ix, iy: axes.plot(x, line.k[ix, iy] * x + line.b[ix, iy])
        self.do_for_each_axes(action)

    def set_lims(self, xlim: Tuple[int, int], ylim: Tuple[int, int]):
        def action(axes, ix, iy):
            axes.set_xlim(xlim)
            axes.set_ylim(ylim)

        self.do_for_each_axes(action)

    def show(self):
        plt.show()
