import time
import board
import qwiic
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX
from adafruit_lsm6ds import Rate

#print(qwiic.list_devices())
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = ISM330DHCX(i2c, 0x6b)
sensor.accelerometer_data_rate = Rate.RATE_833_HZ

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (sensor.gyro))
    print(sensor.acceleration)
    print(sensor.gyro)
    print("")
    #time.sleep(0.05)
