import matplotlib.pyplot as plt
from read_pickle import get_field_from_pickle
import numpy as np

filename = 'pickles/105000.pkl'
dates = get_field_from_pickle(filename, 'DATE')[1]
temps = get_field_from_pickle(filename, 'TEMP')[1]

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

def manual_fit():
    for i in range(3, 8):
        for j in range(8):
            temps_sky = get_field_from_pickle(filename, 'TEMP_SKY_{}_{}'.format(i, j))[1]
            fig, ax = plt.subplots()
            plt.suptitle('TEMP_SKY_{}_{}'.format(i, j))
            plt.xlabel('TEMP_SKY_{}_{}'.format(i, j))
            plt.ylabel('TEMP')

            ax.plot(temps_sky, temps, 'ro', markersize = 0.1)
            line, = ax.plot([0], [0], 'g-')
            builder = LineBuilder(line)

            ax.set_xlim(-45, 10)
            ax.set_ylim(-25, 15)
            plt.show()

def automatic_fit():
    def first_fraction_elements_indexes(array: np.ndarray, max: bool, fraction: int):
        num_of_points = int(fraction * len(array))
        if max: 
            return np.argsort(array)[-num_of_points:]
        else:
            return np.argsort(array)[:num_of_points] 

    temps_sky = get_field_from_pickle(filename, 'TEMP_SKY_6_6')[1]
    plt.plot(temps_sky, temps, 'bo', markersize = 0.05)

    def plot_left():
        span = (-40, -22)
        N = 100
        fraction = 0.2
        top = True

        step = (span[1] - span[0]) / N
        res_temps_sky = np.empty((0,))
        res_temps = np.empty((0,))

        for i in range(N):
            filter = np.logical_and(temps_sky > span[0] + step * i, temps_sky < span[0] + step * (i + 1))
            curr_temps = temps[filter]
            ind = first_fraction_elements_indexes(curr_temps, top, fraction)
            plt.plot(temps_sky[filter][ind], temps[filter][ind], 'ro', markersize = 0.5)
            res_temps_sky = np.concatenate((res_temps_sky, temps_sky[filter][ind]))
            res_temps = np.concatenate((res_temps, temps[filter][ind]))
            
        fit = np.polyfit(res_temps_sky, res_temps, 1)
        print(fit)
        plt.plot(res_temps_sky, fit[1] + res_temps_sky * fit[0])

    def plot_right():
        span = (-17, 0)
        N = 100
        fraction = 0.15
        top = False

        step = (span[1] - span[0]) / N
        res_temps_sky = np.empty((0,))
        res_temps = np.empty((0,))

        for i in range(N):
            filter = np.logical_and(temps_sky > span[0] + step * i, temps_sky < span[0] + step * (i + 1))
            curr_temps = temps[filter]
            ind = first_fraction_elements_indexes(curr_temps, top, fraction)
            plt.plot(temps_sky[filter][ind], temps[filter][ind], 'ro', markersize = 0.5)
            res_temps_sky = np.concatenate((res_temps_sky, temps_sky[filter][ind]))
            res_temps = np.concatenate((res_temps, temps[filter][ind]))
            
        fit = np.polyfit(res_temps_sky, res_temps, 1)
        print(fit)
        plt.plot(res_temps_sky, fit[1] + res_temps_sky * fit[0])

    plot_left()
    plot_right()

    plt.xlim(-45, 10)
    plt.ylim(-25, 15)
    plt.show()

manual_fit()