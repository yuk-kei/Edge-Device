from app import gen_sensor_data, produce_data
from app import Sensor


def test():
    sensor = Sensor("mock", "sensor_01")
    sensor_data = gen_sensor_data()
    sensor.set_sensor_data(sensor_data)
    print(sensor.dump_data())

def test2():
    produce_data()

if __name__ == "__main__":
    test2()
