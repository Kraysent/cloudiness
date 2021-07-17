from datetime import timedelta

import numpy as np

from iotools import pickleio
from utils import utils
from utils.calibration_parameters_manager import (CalibrationParametersManager,
                                                  StandartCalibrationManager)
from utils.photo_manager import FITSPhotoManager, PhotoManager
from utils.temperature_manager import TemperatureManager, WebTemperatureManager
from utils.visualizer import Visualizer


def run(
    photo_manager: PhotoManager, 
    temp_manager: TemperatureManager, 
    calib_manager: CalibrationParametersManager
):
    photo = photo_manager.get_current_photo()
    temp = temp_manager.get_current_temperature()
    calibration = calib_manager.get_current_calibration()

    photo = utils.divide_plane(photo, calibration.shape)
    temp_sky = np.mean(photo, axis = (2, 3))

    cloudiness, fogginess = calibration.get_cloudiness_and_fogginess(temp_sky, temp)

    visualizer = Visualizer((4, 4))
    xlim = (-45, 10)
    ylim = (-25, 20)
    visualizer.scatter_calibration('pickles/res.pkl', 
        colorbarlabel = 'Standart deviation of the observatory fragment')
    visualizer.plot_line(calibration.clear_line, xlim[0], xlim[1])
    visualizer.plot_line(calibration.cloud_line, xlim[0], xlim[1])
    visualizer.plot_line(calibration.fog_line, xlim[0], xlim[1])
    visualizer.plot_point(temp_sky, temp)
    visualizer.set_labels_for_axes('Temperature of the sky, Celcius', 'Temperature of the air, Celcius')
    visualizer.set_title('Temperature-temperature relation for cloudiness')
    visualizer.set_lims(xlim, ylim)

    weights = calibration.get_frame_weights()
    total_cloudiness = np.average(cloudiness, weights = weights)
    total_fogginess  = np.average(fogginess, weights = weights)

    print('Cloudiness: {}'.format(total_cloudiness))
    print('Fogginess: {}'.format(total_fogginess))
    visualizer.show()

def calibrate(manager, dump_filename: str):
    photo_data, photo_dates = manager.get_sample_data()
    temps, temp_dates = manager.get_temperature_data()

    matched_temps = np.zeros(len(photo_dates))

    for i in range(len(photo_dates)):
        if i % 1000 == 0: print(i)
        (index, diff) = utils.find_nearest_date(photo_dates[i], temp_dates)

        if diff < timedelta(minutes = 10):
            matched_temps[i] = temps[index]
        else:
            matched_temps[i] = np.nan

    filter = np.logical_not(np.isnan(matched_temps))
    photo_dates = photo_dates[filter]
    matched_temps = matched_temps[filter]

    division_shape = (8, 8)
    photo_data = utils.divide_cube(photo_data[filter], division_shape)
    (mean_intensity, std_intensity) = manager.get_statistical_parameters(photo_data)

    # for ix, iy in np.ndindex(division_shape):
    #     mean_intensity[:, ix, iy] = mean_intensity[:, ix, iy][filter]
    #     std_intensity[:, ix, iy] = std_intensity[:, ix, iy][filter]

    dump = {}
    dump['DATE'] = photo_dates
    dump['TEMP'] = matched_temps

    for ix, iy in np.ndindex(division_shape):
        dump['TEMP_SKY_{}_{}'.format(ix, iy)] = mean_intensity[:, ix, iy]
        dump['STD_{}_{}'.format(ix, iy)] = std_intensity[:, ix, iy]

    pickleio.dump_dict(dump_filename, dump)

    visualizer = Visualizer((4, 4))
    visualizer.scatter_calibration(dump_filename, coloring = False)
    visualizer.add_linebuilder()
    visualizer.show()
    
# calibrate(None, 'pickles/105000.pkl')

run(
    FITSPhotoManager(),
    WebTemperatureManager(),
    StandartCalibrationManager() 
)
