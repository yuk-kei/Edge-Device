from app.model import Device

device = Device("test_device", "localhost", 9000, type="sensor", category="test", location="calit2", status="active")


def test_register():
    device.register()
    print("Device registered, ID: {}".format(device.device_id))


def test_transmit():
    device.emit_data()
    device.flush()


def multi_device_test():
    dlist = []
    for i in range(20):
        device = Device("test_device_1", "localhost", 9000, type="sensor", category="test", location="calit2",
                        status="active",rate=0.01, device_id =1)
        dlist.append(device)
        device.start()


if __name__ == "__main__":
    multi_device_test()
