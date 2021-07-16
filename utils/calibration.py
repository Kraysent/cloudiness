from typing import Tuple

import numpy as np


class ThresholdLine:
    def __init__(self, k: np.ndarray, b: np.ndarray) -> None:
        if k.shape == b.shape:
            self.k, self.b = k, b
        else:
            raise RuntimeError('Trying to initialize line with different shapes of ks and bs')

    def read_from_csv(k_filename: str, b_filename: str) -> 'ThresholdLine':
        k = np.genfromtxt(k_filename, delimiter = ',')
        b = np.genfromtxt(b_filename, delimiter = ',')
        return ThresholdLine(k, b)

    @property
    def shape(self):
        return self.k.shape

class Calibration:
    def __init__(self, shape: Tuple[int, int]) -> None:
        self.clear_line = ThresholdLine(np.zeros(shape), np.zeros(shape))
        self.cloud_line = ThresholdLine(np.zeros(shape), np.zeros(shape))
        self.fog_line = ThresholdLine(np.zeros(shape), np.zeros(shape))
        self.weights = np.ones(shape)

    def init_with_params(
        clear_line: ThresholdLine, 
        cloud_line: ThresholdLine, 
        fog_line: ThresholdLine, 
        weights: np.ndarray
    ) -> 'Calibration':
        res = Calibration(clear_line.shape)
        res.clear_line = clear_line
        res.cloud_line = cloud_line
        res.fog_line = fog_line
        res.weights = weights

        return res

    def _get_distance_along_x(self, line: ThresholdLine, x, y):
        return x - (y - line.b) / line.k

    def _get_line_distance_along_x(self, line1: ThresholdLine, line2: ThresholdLine, y):
        return (y - line2.b) / line2.k - (y - line1.b) / line2.k

    def get_cloudiness_and_fogginess(self, temp_sky: np.ndarray, temp: int) -> float:
        clear_rel_x = self._get_distance_along_x(self.clear_line, temp_sky, temp)
        clear_cloud_dist = self._get_line_distance_along_x(self.clear_line, self.cloud_line, temp)
        clear_fog_dist = self._get_line_distance_along_x(self.clear_line, self.fog_line, temp)
        clear_cloud_rel_x = np.clip(clear_rel_x, 0, clear_cloud_dist)
        clear_fog_rel_x = np.clip(clear_rel_x, 0, clear_fog_dist)

        return (clear_cloud_rel_x / clear_cloud_dist, clear_fog_rel_x / clear_fog_dist)

    def get_frame_weights(self):
        return self.weights

    def read_from_csv(filenames: list) -> 'Calibration':
        if len(filenames) < 7:
            raise RuntimeError('Not enough filenames provided')
            
        clear_line = ThresholdLine.read_from_csv(filenames[0], filenames[1])
        cloud_line = ThresholdLine.read_from_csv(filenames[2], filenames[3])
        fog_line = ThresholdLine.read_from_csv(filenames[4], filenames[5])
        weights = np.genfromtxt(filenames[6], delimiter = ',')

        return Calibration.init_with_params(clear_line, cloud_line, fog_line, weights)
        
    @property
    def shape(self):
        return self.clear_line.shape

