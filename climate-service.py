import time
# Assumes I2C, a certain type of connection
import board
import busio
import adafruit_bmp280

import qrcode
import json

import py_resize
from qrcode.image.pure import PymagingImage

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
    return json.dumps(data)

def generateQRCode(state):
    qr = qrcode.make(state, image_factory=PymagingImage)
    qr.save(f'{state.super.deviceId}.bmp')
    py_resize.main(f'-f {state.super.deviceId}.bmp')


i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
generateQRCode(getState(sensor))


while True:
    time.sleep(30)
    newState = getState(sensor)
    if state != newState:
        # The temperature/humidity has changed, generate new QR Code
        state = newState
        generateQRCode(state)


