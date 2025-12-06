import time
import board
import pwmio
import digitalio
import neopixel

if board.board_id == 'adafruit_feather_rp2040':
    indicatorLedPin = board.D5
    buzzerPin = board.D6
    barrierLedPin = board.D9
    barrierSensorPin = board.D10
    solenoidPin = board.D11
    
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

# Upgrade to JLed and hack it to talk to the Neopixel?
# https://github.com/jandelgado/jled-circuitpython
rgbLed = neopixel.NeoPixel(board.NEOPIXEL, 1)
rgbLed[0] = (0, 255, 0)
rgbLed.brightness = 0.0
brightnessStepPerNs = 0.00000000007

lastLoopTime = time.monotonic_ns()

while True:
    if barrierSensor.value:
        solenoid.value = True
        time.sleep(.5)
        solenoid.value = False

        indicatorLed.value = True
        boardLed.value = True
        rgbLed.brightness = 0.0

        while True:
            buzzer.value = True
            time.sleep(0.1)
            buzzer.value = False

            time.sleep(60)

    thisLoopTime = time.monotonic_ns()
    elapsedNs = thisLoopTime - lastLoopTime
    rgbLed.brightness = rgbLed.brightness + (elapsedNs * brightnessStepPerNs)
    if (rgbLed.brightness >= 0.1 or rgbLed.brightness <= 0):
        brightnessStepPerNs = brightnessStepPerNs * -1
    
    lastLoopTime = thisLoopTime
