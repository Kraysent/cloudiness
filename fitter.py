from iotools.pickleio import PickleIO
import matplotlib.pyplot as plt
import numpy as np

filename = 'pickles/105000.pkl'
dates = PickleIO.get_field_from_pickle(filename, 'DATE')[1]
temps = PickleIO.get_field_from_pickle(filename, 'TEMP')[1]

def automatic_fit():
    def first_fraction_elements_indexes(array: np.ndarray, max: bool, fraction: int):
        num_of_points = int(fraction * len(array))
        if max: 
            return np.argsort(array)[-num_of_points:]
        else:
            return np.argsort(array)[:num_of_points] 

    temps_sky = PickleIO.get_field_from_pickle(filename, 'TEMP_SKY_6_6')[1]
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

automatic_fit()