import math
import sys
cm_to_ft = 0.0328084

class measure:
    def __init__(self, level):
        self._water_level = level
        self._max = sys.maxsize
        self._min = -1 * sys.maxsize
        
    def compare(self, height):
        self._max = min(self._max, height)
        self._min = max(self._min, height)

    def get_heights(self):
        return {(self._min * cm_to_ft) - self._water_level, (self._max * cm_to_ft) - self._water_level}
