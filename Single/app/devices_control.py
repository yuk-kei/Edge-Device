from time import sleep

import yaml

from .model import Device


def load_device(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
        device_info = config["device"]
        device = Device(
            device_id=device_info["id"],
            name=device_info["name"],
            type=device_info["type"],
            location=device_info["location"],
            ip=device_info["ip_address"],
            port=device_info["port"],
            category=device_info["category"]
        )

        device.start()
        print(f"Device {device.name} is running")
        sleep(1)
        print(device.device_id)
        if device_info["id"] is None or device_info["id"] == "":
            device_info["id"] = device.device_id
            with open(filename, 'w') as file:
                yaml.dump(config, file)
        return device


