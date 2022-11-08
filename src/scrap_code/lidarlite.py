from adafruit_register import i2c_bit
from adafruit_bus_device import i2c_device
STATUS_BUSY = 0x01

class lidar:
    def __init__(self, i2c, device_address=0x0):
        self.buf = bytearray(2)
        scan = i2c.scan()
        if len(scan) == 0:
            raise Exception('no I2C Devices found')
        device_address = scan[0]
        self.i2c_device = i2c_device.I2CDevice(i2c, device_address)

    def _write_reg(self, reg, value):
        self.buf[0] = reg
        self.buf[1] = value
        with self.i2c_device as i2c:
            i2c.write_then_readinto(self.buf, self.buf)
        return self.buf[0]

    def _read_reg(self, reg, num):
        self.buf[0] = reg
        with self.i2c_device as i2c:
            i2c.write_then_readinto(self.buf, self.buf, out_end=1, in_end=num)
        return self.buf

    def request(self):
        self._write_reg(0x00, 0x04)
    
    def read(self):
        status = [0]
        while status[0]%2 == 1:
            status = self._read_reg(0x01, 1)
        result = self._read_reg(0x10, 2)
        num = result[1]*0xff + result[0]
        print(num, 'cm  ', end = '\r')
        return(num)

if __name__ == '__main__':
    import board, busio
    from time import sleep
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = lidar(i2c)
    while True:
        sensor.request()
        sensor.read()
        sleep(0.1)


