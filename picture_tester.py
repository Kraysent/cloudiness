import os
from datetime import datetime, timedelta
from utils.photo_manager import FITSPhotoManager
from utils.calibration_parameters_manager import StandartCalibrationParametersManager
from utils import utils
from iotools import pickleio, fitsio
from cloudiness import get_cloudiness_and_fogginess
import pytz

def test_picture(dirpath: str, filename: str, temperature_pickle_filename: str):
    date = datetime.strptime(filename, utils.fits_filename_format)
    date = date.replace(tzinfo = pytz.utc).astimezone(pytz.timezone('Europe/Moscow'))
    
    calibration = StandartCalibrationParametersManager().get_current_calibration()
    photo = FITSPhotoManager(os.path.join(dirpath, filename)).get_current_photo()

    dates = pickleio.get_index(temperature_pickle_filename)
    temps = pickleio.get_field(temperature_pickle_filename, 'TEMP')

    (index, diff) = utils.find_nearest_date(date, dates)
    
    if diff > timedelta(minutes = 10):
        print(f'Closest date if {diff.seconds} seconds away. Might be inaccurate.')

    temp = temps[index]

    (cloudiness, fogginess) = get_cloudiness_and_fogginess(photo, temp, calibration)

    print(f'Cloudiness: {cloudiness}')
    print(f'Fogginess: {fogginess}')

test_picture('maps/2021/', 'MAP2021-04-01T00-09-22.612.fits', 'temperature/all_data.pkl')