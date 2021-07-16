import numpy as np

from utils import utils
from utils.iomanager import BlankIOManager, IOManager
from utils.visualizer import Visualizer


def run(manager: IOManager):
    photo = manager.get_current_photo()
    temp = manager.get_current_temperature()
    calibration = manager.get_current_calibration()

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

run(BlankIOManager())
