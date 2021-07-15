import numpy as np
from utils.iomanager import IOManager, StandartIOManager
from utils import utils

def run(manager: IOManager):
    photo = manager.get_current_photo()
    temp = manager.get_current_temperature()
    calibration = manager.get_current_calibration()

    photo = utils.divide(photo, calibration.shape)
    temp_sky = np.mean(photo, axis = (3, 4))

    cloudiness = calibration.get_cloudiness(temp_sky, temp)
    fogginess = calibration.get_fogginess(temp_sky, temp)

    weights = calibration.get_frame_weights()
    total_cloudiness = np.mean(cloudiness * weights)
    total_fogginess = np.mean(fogginess * weights)

    print('Cloudiness: {}'.format(total_cloudiness))
    print('Fogginess: {}'.format(total_fogginess))

run(StandartIOManager())