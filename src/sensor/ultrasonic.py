import RPi.GPIO as gpio
import time


def distance(measure='cm'):
    try:
        startTime = time.time()
        gpio.setmode(gpio.BOARD)
        gpio.setup(40, gpio.OUT)
        gpio.setup(38, gpio.IN)

        gpio.output(40, 1)
        time.sleep(0.06)
        gpio.output(40, 0)
        nosig = 0
        sig = 0
        while gpio.input(38) == 0 and time.time() - startTime < 1:
            nosig = time.time()
        while gpio.input(38) == 1 and time.time() - startTime < 1:
            sig = time.time()
        if nosig == 0:
            print("Measurment Failed")
            return 0
        tl = sig - nosig
        if measure == 'cm':
            distance = tl / 0.000058
        elif measure == 'in':
            distance = tl / 0.000148
        else:
            print('improper choice of measurement: in or cm')
            distance = None
        gpio.cleanup()
        return distance
    except (RuntimeError, TypeError, NameError) as err:
        print(err)
        gpio.cleanup()
        return 0

# if __name__ == '__main__':
#     gpio.cleanup()
#     while True:
#         print(distance("in"))
