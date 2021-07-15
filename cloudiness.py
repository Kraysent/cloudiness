import numpy as np
from utils.iomanager import IOManager, BlankIOManager
from utils import utils

def run(manager: IOManager):
    photo = manager.get_current_photo()
    temp = manager.get_current_temperature()
    calibration = manager.get_current_calibration()

    photo = utils.divide(photo, calibration.shape)
    temp_sky = np.mean(photo, axis = (2, 3))

    cloudiness, fogginess = calibration.get_cloudiness_and_fogginess(temp_sky, temp)

    weights = calibration.get_frame_weights()
    total_cloudiness = np.average(cloudiness, weights = weights)
    total_fogginess  = np.average(fogginess, weights = weights)

    print('Cloudiness: {}'.format(total_cloudiness))
    print('Fogginess: {}'.format(total_fogginess))

run(BlankIOManager())