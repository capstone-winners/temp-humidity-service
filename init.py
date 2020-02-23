import time
# Assumes I2C, a certain type of connection
import board
import busio
import adafruit_bmp280

import qrcode

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)


# QR Code format:
#  {
#   temperature: Float,
#   pressure: Float,
#   super: {
#    deviceId: String,
#    deviceType: "climate",
#    status: "ok", 
#    group: [String],
#    location: String
#  }
# }


def getState(sensor):
    data = {
        "temperature": sensor.temperature,
        "pressure": sensor.pressure,
        "super": {
            "deviceId": "hard coded",
            "deviceType": "climate",
            "status": "ok",
            "group": ["Trap House"],
            "location": "Tom's Room"
        }
    }
    return data

state = getState(sensor)
# TODO: add call to Nikhil's script to make sure qrCode has the right dimensions
# Then actually display on screen
qrCode = qrcode.make(state)


while True:
    time.sleep(30)
    if state != getState(sensor):
        # The temperature/humidity has changed, generate new QR Code
        state = getState(sensor)
        # TODO: add call to Nikhil's script to make sure qrCode has the right dimensions
        # Then actually display on screen
        qrCode = qrcode.make(state)


