from datetime import timedelta

import numpy as np

from iotools import pickleio
from utils import utils
from utils.calibration_parameters_manager import (CalibrationParametersManager,
                                                  StandartCalibrationParametersManager)
from utils.photo_manager import BlankPhotoManager, FITSPhotoManager, PhotoManager
from utils.temperature_manager import BlankTemperatureManager, TemperatureManager, WebTemperatureManager
from utils.visualizer import Visualizer


def run(
    photo_manager: PhotoManager, 
    temp_manager: TemperatureManager, 
    calib_manager: CalibrationParametersManager
):
    photo = photo_manager.get_current_photo()
    temp = temp_manager.get_current_temperature()
    calibration = calib_manager.get_current_calibration()
    dates = calib_manager.get_list_of_dates()

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
    visualizer.add_picker(dates)

    weights = calibration.get_frame_weights()
    total_cloudiness = np.average(cloudiness, weights = weights)
    total_fogginess  = np.average(fogginess, weights = weights)

    print('Cloudiness: {}'.format(total_cloudiness))
    print('Fogginess: {}'.format(total_fogginess))
    visualizer.show()

def extract_calibration_data(
    photo_manager: PhotoManager, 
    temperature_manager: TemperatureManager, 
    dump_filename: str
):
    photo_dates, photo_data = photo_manager.get_historical_photo_data()
    temp_dates, temps = temperature_manager.get_historical_temperature_data()

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
    (mean_intensity, std_intensity) = utils.get_statistical_parameters(photo_data)

    dump = {}
    dump['DATE'] = photo_dates
    dump['TEMP'] = matched_temps

    for ix, iy in np.ndindex(division_shape):
        dump['TEMP_SKY_{}_{}'.format(ix, iy)] = mean_intensity[:, ix, iy]
        dump['STD_{}_{}'.format(ix, iy)] = std_intensity[:, ix, iy]

    pickleio.dump_dict(dump_filename, dump)

def get_calibration_parameters(dump_filename: str):
    for ix, iy in np.ndindex((8, 8)):
        visualizer = Visualizer((ix, iy))
        visualizer.set_title(f'Plot {ix}-{iy}')
        visualizer.scatter_calibration(dump_filename, coloring = False)
        visualizer.add_linebuilder()
        visualizer.show()
    
# extract_calibration_data(FITSPhotoManager(), WebTemperatureManager(), 'pickles/example.pkl')
# get_calibration_parameters('pickles/example.pkl')

run(
    FITSPhotoManager(),
    WebTemperatureManager(),
    StandartCalibrationParametersManager() 
)
