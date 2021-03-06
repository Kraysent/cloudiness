from datetime import datetime
from typing import Any, Callable, Tuple

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from iotools import pickleio
from matplotlib.axes import Axes

from utils.calibration_parameters import ThresholdLine
from utils import utils


class LineBuilder:
    def __init__(self, line):
        self.first = True
        self.xs, self.ys = list(line.get_xdata()), list(line.get_ydata())
        self.line = line
        self.cid = self.line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('Click: ({}, {})'.format(event.xdata, event.ydata))
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)

        if self.first:
            self.xs = [event.xdata]
            self.ys = [event.ydata]
            self.first = False
        else:
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            x1, y1 = self.xs[0], self.ys[0]
            x2, y2 = self.xs[1], self.ys[1]
            k = (y2 - y1) / (x2 - x1)
            b = (x2 * y1 - x1 * y2) / (x2 - x1)
            print('k = {}\tb = {}'.format(np.round(k, 2), np.round(b, 2)))
            self.first = True

        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()

class Visualizer:
    def __init__(self, draw_fragment: Tuple[int, int] = None):
        axes = None
        if draw_fragment == None:
            _, axes = plt.subplots((8, 8))
        else: 
            _, axes = plt.subplots()
        
        self.axes = axes
        self.fragment = draw_fragment

    def do_for_each_axes(self, action: Callable[[Axes, int, int], Any]):
        results = []

        if self.fragment != None:
            results.append(action(self.axes, self.fragment[0], self.fragment[1]))
        else:
            for ix, iy in np.ndindex(self.axes.shape):
                results.append(action(self.axes[ix, iy], ix, iy))

        return results

    def scatter_calibration(self, 
        filename: str, coloring: bool = True, clogscale: bool = True, 
        markersize: float = 0.1, colorbarlabel: str = ''
    ):
        temps = pickleio.get_field(filename, 'TEMP')

        if coloring:
            temps_sky_disp = pickleio.get_field(filename, 'STD_1_2')

            norm = None
        
            if clogscale:
                norm = mpl.colors.LogNorm()

            def action(axes: Axes, ix: int, iy: int):
                temps_sky = pickleio.get_field(filename, f'TEMP_SKY_{ix}_{iy}')
                im = axes.scatter(
                    temps_sky, temps, 
                    s = markersize, c = temps_sky_disp, 
                    cmap = 'plasma', norm = norm,
                    picker = 2
                )
                cbar = axes.figure.colorbar(im, ax = axes, label = colorbarlabel)
                cbar.set_ticks([0.5, 1, 2, 4, 8])
                cbar.set_ticklabels(['$2^{-1}$', '$2^0$', '$2^1$', '$2^2$', '$2^3$'])

        else:
            def action(axes, ix, iy):
                temps_sky = pickleio.get_field(filename, f'TEMP_SKY_{ix}_{iy}')
                axes.plot(temps_sky, temps, 'ro', markersize = markersize)

        self.do_for_each_axes(action)

    def set_labels_for_axes(self, xlabel: str, ylabel: str):
        self.do_for_each_axes(lambda axes, ix, iy: axes.set_xlabel(xlabel))
        self.do_for_each_axes(lambda axes, ix, iy: axes.set_ylabel(ylabel))

    def set_title(self, title: str):
        plt.suptitle(title)

    def plot_point(self, x, y):
        action = lambda axes, ix, iy: axes.plot(x[ix, iy], y, 'ro')

        self.do_for_each_axes(action)

    def plot_line(self, line: ThresholdLine, start: float, end: float):
        x = np.linspace(start, end, 10)

        action = lambda axes, ix, iy: axes.plot(x, line.k[ix, iy] * x + line.b[ix, iy])
        self.do_for_each_axes(action)

    def add_linebuilder(self):
        lines = self.do_for_each_axes(lambda axes, x, y: axes.plot([0], [0], 'g-'))
        for line in lines:
            LineBuilder(line[0])

    def add_picker(self, dates):
        self.dates = dates

        def on_pick(event):
            # artist = event.artist
            ind = event.ind[0]
            print(datetime.strftime(self.dates[ind], utils.fits_filename_format))

        def action(axes: Axes, ix: int, iy: int):
            axes.figure.canvas.mpl_connect('pick_event', on_pick)

        self.do_for_each_axes(action)

    def set_lims(self, xlim: Tuple[int, int], ylim: Tuple[int, int]):
        def action(axes, ix, iy):
            axes.set_xlim(xlim)
            axes.set_ylim(ylim)

        self.do_for_each_axes(action)

    def show(self):
        plt.show()
