# Edge Device

## Introduction

This project provides an interface and implementation to simulate, monitor, and control devices. It makes use of Flask for API endpoints, Kafka for data streaming, and Confluent Kafka as a producer to send data.

## Modules
### Tree Structure
```bash
.
├── app
│   ├── data_gen.py           # Functions for generating mock data and timestamps.
│   ├── devices_control.py    # Logic to load and control the device configuration.
│   ├── __init__.py
│   ├── model.py              # Defines the device behavior including Kafka data sending.
│   └── routes.py             # Flask routes for controlling the device.
├── device_config.yaml        # Configuration file for the device.
├── config.py                 # Contains configurations and environment variables retrievals.
├── README.md                 # This file.
├── requirements.txt          # (Needs to be updated with project dependencies.)
└── run.py                    # Entry point to run the application.
```

### Setup:

1. Ensure all necessary environment variables are set, as required by `config.py`. 

2. Modify `device_config.yaml` with the appropriate device settings and leave the `id` field blank.

3. In the `app/data_gen.py`, modify the `generate_data()` function to return a dict of data

   example 1:

   ``` python
   from datetime import datetime, timezone
   from .model import SensorData
   
   import adafruit_scd4x
   import board
   
   i2c = board.I2C()
   scd4x = adafruit_scd4x.SCD4X(i2c)
   
   scd4x.start_periodic_measurement()
   
   def generate_data():
       
       return {
               "CO2(ppm)": scd4x.CO2,
               "Temperature(*C)": scd4x.temperature,
               "Humidity(%)" : scd4x.relative_humidity
           }
       
   def gen_ts_data(values=None):
   
       dt = datetime.now(timezone.utc)
       timestamp = dt.strftime("%m/%d/%Y %H:%M:%S.%f")
   
       return SensorData(timestamp, values)
   ```

   example 2:

   ``` python
   from datetime import datetime, timezone
   from .model import SensorData
   
   import board
   from adafruit_lsm6ds.ism330dhcx import ISM330DHCX
   from adafruit_lsm6ds import Rate
   
   i2c = board.I2C()  # uses board.SCL and board.SDA
   sensor = ISM330DHCX(i2c, 0x6b)
   sensor.accelerometer_data_rate = Rate.RATE_833_HZ
   
   
   def gen_accelerometer_data():
   
       data1 = sensor.acceleration
       data2 = sensor.gyro
   
       return {
           "acc_x": data1[0],
           "acc_y": data1[1],
           "acc_z": data1[2],
           "gyro_x": data2[0],
           "gyro_y": data2[1],
           "gyro_z": data2[2],
       }
       
   def gen_ts_data(values=None):
   
       dt = datetime.now(timezone.utc)
       timestamp = dt.strftime("%m/%d/%Y %H:%M:%S.%f")
   
       return SensorData(timestamp, values)
   ```

   If you want to configure the default sending rate, you could modify the `Device` class  `rate` attribute's default value in `app/model`

   ``` python3
   class Device(threading.Thread):
       def __init__(self, name, ip, port, device_id=None, type=None, category=None, location=None, status=None, rate='your_default_rate_in_second'):
   ```

   

4. Install the necessary dependencies using:

```bash
pip install -r requirements.txt
```

1. Run the application:

```bash
python run.py
```

### API Endpoints:

- `/api/v1/measure/test`: Test endpoint to check if the service is alive
- `/api/v1/measure/pause`: Pause the device.
- `/api/v1/measure/resume`: Resume the device.
- `/api/v1/measure/stop`: Stop the device.
- `/api/v1/measure/status`: Get the status of the device.
