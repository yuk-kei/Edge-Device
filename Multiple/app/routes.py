from flask import Blueprint

pressure_blueprint = Blueprint('pressure', __name__, url_prefix="/api/v1/pressure")

@app.route('/api/v1/device/pause', methods=['POST'])
def pause_device():
    device_id = request.json.get('device_id')
    device = find_device_by_id(device_id, devices)
    if device is None:
        return "Device not found", 404
    else:
        if device.status != "running":
            return "Device is not running", 400
        else:
            device.pause()
            device.status = "paused"
            return "Device paused", 200


@app.route('/api/v1/device/resume', methods=['POST'])
def resume_device():
    device_id = request.json.get('device_id')
    device = find_device_by_id(device_id, devices)
    if device is None:
        return "Device not found", 404
    else:
        if device.status != "paused":
            return "Device is not paused", 400
        else:
            device.resume()
            return "Device resumed", 200


@app.route('/api/v1/device/stop', methods=['POST'])
def stop_device():
    device_id = request.json.get('device_id')
    device = find_device_by_id(device_id, devices)
    if device is None:
        return "Device not found", 404
    else:
        if device.status != "stopped":
            device.stop()
            return "Device stopped", 200
        else:
            return "Device already stopped", 400


def restart_device():
    device_id = request.json.get('device_id')
    device = find_device_by_id(device_id, devices)
    if device is None:
        return "Device not found", 404
    else:
        renew_device_by_id(device_id, devices)


def get_device_status():
    device_id = request.json.get('device_id')
    device = find_device_by_id(device_id, devices)
    if device is None:
        return "Device not found", 404
    else:
        return device.status, 200


@app.route('/api/v1/sensor/', methods=['GET', 'POST'])
def test():  # put application's code here
    return 'Hello World!'