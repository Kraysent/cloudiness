import numpy as np

from utils import utils
from utils.calibration_manager import (CalibrationManager,
                                       StandartCalibrationManager)
from utils.photo_manager import FITSPhotoManager, PhotoManager
from utils.temperature_manager import (TemperatureManager, 
                                       WebTemperatureManager)
from utils.visualizer import Visualizer


def run(
    photo_manager: PhotoManager, 
    temp_manager: TemperatureManager, 
    calib_manager: CalibrationManager
):
    photo = photo_manager.get_current_photo()
    temp = temp_manager.get_current_temperature()
    calibration = calib_manager.get_current_calibration()

    photo = utils.divide(photo, calibration.shape)
    temp_sky = np.mean(photo, axis = (2, 3))

    cloudiness, fogginess = calibration.get_cloudiness_and_fogginess(temp_sky, temp)

    visualizer = Visualizer((4, 4))
    xlim = (-45, 10)
    ylim = (-25, 20)
    visualizer.scatter_calibration('pickles/res.pkl')
    visualizer.plot_line(calibration.clear_line, xlim[0], xlim[1])
    visualizer.plot_line(calibration.cloud_line, xlim[0], xlim[1])
    visualizer.plot_line(calibration.fog_line, xlim[0], xlim[1])
    visualizer.plot_point(temp_sky, temp)
    visualizer.set_lims(xlim, ylim)

    weights = calibration.get_frame_weights()
    total_cloudiness = np.average(cloudiness, weights = weights)
    total_fogginess  = np.average(fogginess, weights = weights)

    print('Cloudiness: {}'.format(total_cloudiness))
    print('Fogginess: {}'.format(total_fogginess))
    visualizer.show()

run(
    FITSPhotoManager(),
    WebTemperatureManager(),
    StandartCalibrationManager() 
)
