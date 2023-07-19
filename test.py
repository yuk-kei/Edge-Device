import yaml

from model import Device

device = Device("Device 1", "localhost", 9001, type="sensor", location="calit2", status="active")


def test_register():
    device.register()
    print("Device registered, ID: {}".format(device.device_id))


def test_transmit():
    device.emit_data()
    device.flush()


def multi_device_test():
    device_1 = Device("Device 1", "localhost", 9001, type="sensor", location="calit2", status="active")
    device_2 = Device("Device 2", "localhost", 9002, type="sensor", location="calit2", status="active")
    device_3 = Device("Device 3", "localhost", 9003, type="sensor", location="calit2", status="active")
    device_4 = Device("Device 4", "localhost", 9004, type="sensor", location="calit2", status="active")
    device_5 = Device("Device 5", "localhost", 9005, type="sensor", location="calit2", status="active")
    device_6 = Device("Device 6", "localhost", 9006, type="sensor", location="calit2", status="active")

    device_1.start()
    device_2.start()
    device_3.start()
    device_4.start()
    device_5.start()
    device_6.start()





if __name__ == "__main__":
    test_transmit()
