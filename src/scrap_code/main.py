from sensor.lidarlite import lidar
import measurement
if __name__ == '__main__':
    import board, busio
    from time import sleep
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = lidar(i2c)
    m = measurement(lidar.read())
    time = 0
    while True:
        if(time % 2 == 0):
            for j in range(2):
                for i in range(10):
                    sensor.request()
                    m.compare(sensor.read())
                    sleep(.1)
                    heights = m.get_heights()
            sleep(30)
        else:
            sleep(60)
        time += 1
        if(time == 15):
            str = "max: " + heights[0]
            if(heights[0] < 0):
                str += " below base level"
            else:
                str += "above ase level"
            
            str += " min: " + heights[1]
            if(heights[1] < 0):
                str += " below base level"
            else:
                str += "above base level"
            print(str)
            time = 0
