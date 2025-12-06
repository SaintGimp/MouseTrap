import time
import board
import pwmio
import digitalio
import neopixel
import wifi
import os
import ssl
import socketpool
import adafruit_requests
import adafruit_connection_manager

if board.board_id == 'adafruit_feather_esp32_v2':
    indicatorLedPin = board.D14
    buzzerPin = board.D32
    barrierLedPin = board.D15
    barrierSensorPin = board.D33
    solenoidPin = board.D27
    
boardLed = digitalio.DigitalInOut(board.LED)
boardLed.direction = digitalio.Direction.OUTPUT

indicatorLed = digitalio.DigitalInOut(indicatorLedPin)
indicatorLed.direction = digitalio.Direction.OUTPUT

buzzer = digitalio.DigitalInOut(buzzerPin)
buzzer.direction = digitalio.Direction.OUTPUT

barrierLed = pwmio.PWMOut(barrierLedPin, frequency=38000, duty_cycle=2 ** 15)

barrierSensor = digitalio.DigitalInOut(barrierSensorPin)
barrierSensor.direction = digitalio.Direction.INPUT

solenoid = digitalio.DigitalInOut(solenoidPin)
solenoid.direction = digitalio.Direction.OUTPUT

rgbLed = neopixel.NeoPixel(board.NEOPIXEL, 1)
rgbLed[0] = (0, 255, 0)
rgbLed.brightness = 0.0

boardLed.value = False

wifi.radio.enabled = False

lastLoopSeconds = time.time()

while True:
    time.sleep(.1)
    
    thisLoopSeconds = time.time()
    if thisLoopSeconds - lastLoopSeconds >= 2:
        rgbLed.brightness = 0.1
        time.sleep(0.01)
        rgbLed.brightness = 0.0
        lastLoopSeconds = thisLoopSeconds
        
    if barrierSensor.value:
        solenoid.value = True
        time.sleep(.5)
        solenoid.value = False

        rgbLed.brightness = 0.0

        boardLed.value = True
        wifi.radio.enabled = True
        wifi.radio.connect(ssid=os.getenv("CIRCUITPY_WIFI_SSID"), password=os.getenv("CIRCUITPY_WIFI_PASSWORD"))
        boardLed.value = False
        
        # Send email
        pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
        ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
        requests = adafruit_requests.Session(pool, ssl_context)
        url = os.getenv("EMAIL_URL")
        try:
            response = requests.post(url, json={"subject": "You've got mouse!", "message": "The barrier sensor was triggered."})
            print(f"Response: {response.status_code}")
            response.close()
        except Exception as e:
            print(f"Error sending request: {e}")

        wifi.radio.enabled = False
        
        while True:
            time.sleep(2)
            indicatorLed.value = True
            time.sleep(.01)
            indicatorLed.value = False
