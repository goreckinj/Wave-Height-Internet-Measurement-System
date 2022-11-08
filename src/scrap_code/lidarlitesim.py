import math
from datetime import datetime


class lidarlitesim:
    __AMP_MAX = 8
    __AMP_MIN = 0
    __FREQ_MAX = 2.5
    __FREQ_MIN = 0.5
    __DIST_MIN = 10
    __DIST_MAX = 100

    def __init__(self, i2c, device_address=0x0):
        self.__start_time = datetime.now()
        self.__amp = 4
        self.__amp_tick = 0

        self.__freq = 1.5
        self.freq_tick = 0

        self.__dist = 55
        self.__dist_tick = 0

    def _write_reg(self, reg, value):
        pass

    def _read_reg(self, reg, num):
        pass

    def request(self):
        pass

    '''
    a * sin(bx) + c
    a: Amplitude
    b: Frequency
    c: Vertical Shift
    '''
    def read(self):
        self.__tick()
        return self.__amp * math.sin(self.__freq * (datetime.now() - self.__start_time).total_seconds()) + self.__dist

    def __tick(self):
        pass
