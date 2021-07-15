import unittest
import calibration

class TestCalibration(unittest.TestCase):
    def test_blank_calibration(self):
        calib = calibration.Calibration((8, 8))

        self.assertEqual(calib.get_frame_weights().shape, (8, 8))
        self.assertEqual(calib.shape, (8, 8))

