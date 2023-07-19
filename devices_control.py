import yaml

from model import Device


def find_device_by_id(device_id, devices):
    for device in devices:
        if device.device_id == device_id:

            return device
    return None


def delete_device_by_id(device_id, devices):
    for device in devices:
        if device.device_id == device_id:
            devices.remove(device)
            return device
    return None


def renew_device_by_id(device_id, devices):
    device_data = find_data_in_config(device_id)
    new_device = create_device(device_data)
    new_device.start()
    devices.append(new_device)


def create_device(device_data):
    device = Device(
        device_id=device_data["id"],
        name=device_data["name"],
        type=device_data["type"],
        location=device_data["location"],
        ip=device_data["ip_address"],
        port=device_data["port"]
    )
    return device


def pause_device(device):
    device.pause()


def resume_device(device):
    device.resume()


def stop_device(device):
    device.stop()


def find_data_in_config(device_id):
    with open("device_config.yaml", 'r') as file:
        config = yaml.safe_load(file)
        for device_data in config["devices"]:
            if device_data["id"] == device_id:
                return device_data
        return None


def loadconfig_and_start(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
        devices = []
        for device_data in config["devices"]:
            device = Device(
                device_id=device_data["id"],
                name=device_data["name"],
                type=device_data["type"],
                location=device_data["location"],
                ip=device_data["ip_address"],
                port=device_data["port"]
            )

            device.start()
            print(f"Device {Device.name} is running")
            if device_data["id"] is None:
                device_data["id"] = device.device_id
                with open(filename, 'w') as file:
                    yaml.dump(config, file)

            # device.register()
            devices.append(device)
        return devices
