from flask import Blueprint, request
from .devices_control import load_device
import os

measure_blueprint = Blueprint('measure', __name__, url_prefix="/api/v1/measure")
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'device_config.yaml')


device = load_device(CONFIG_FILE)

@measure_blueprint.route('/test', methods=['GET', 'POST'])
def test():  # put application's code here
    return 'Hello World!'


@measure_blueprint.route('/pause', methods=['POST'])
def pause_device():
    if device is None:
        return "Device not found", 404
    else:
        if device.status != "running":
            return "Device is not running", 400
        else:
            device.pause()
            device.status = "paused"
            return "Device paused", 200


@measure_blueprint.route('/resume', methods=['POST'])
def resume_device():
    # device_id = request.json.get('device_id')

    if device is None:
        return "Device not found", 404
    else:
        if device.status != "paused":
            return "Device is not paused", 400
        else:
            device.resume()
            return "Device resumed", 200


@measure_blueprint.route('/stop', methods=['POST'])
def stop_device():
    # device_id = request.json.get('device_id')
    if device is None:
        return "Device not found", 404
    else:
        if device.status != "stopped":
            device.stop()
            return "Device stopped", 200
        else:
            return "Device already stopped", 400


@measure_blueprint.route('/status', methods=['POST'])
def get_device_status():
    # device_id = request.json.get('device_id')
    if device is None:
        return "Device not found", 404
    else:
        return device.status, 200
# @measure_blueprint.route('/restart')
# def restart_device():
#     device_id = request.json.get('device_id')
#     device = find_device_by_id(device_id, devices)
#     if device is None:
#         return "Device not found", 404
#     else:
#         renew_device_by_id(device_id, devices)
