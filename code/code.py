import time
import board
import pwmio
import digitalio
import neopixel

boardLed = digitalio.DigitalInOut(board.LED)
boardLed.direction = digitalio.Direction.OUTPUT

indicatorLed = digitalio.DigitalInOut(board.D5)
indicatorLed.direction = digitalio.Direction.OUTPUT

buzzer = digitalio.DigitalInOut(board.D6)
buzzer.direction = digitalio.Direction.OUTPUT

barrierLed = pwmio.PWMOut(board.D9, frequency=38000, duty_cycle=2 ** 15)

barrierSensor = digitalio.DigitalInOut(board.D10)
barrierSensor.direction = digitalio.Direction.INPUT

solenoid = digitalio.DigitalInOut(board.D11)
solenoid.direction = digitalio.Direction.OUTPUT

# This is hardware dependent. Upgrade to JLed and hack it
# to talk to the Neopixel
# https://github.com/jandelgado/jled-circuitpython
rgbLed = neopixel.NeoPixel(board.NEOPIXEL, 1)
rgbLed[0] = (0, 255, 0)
rgbLed.brightness = 0.0
brightnessStep = 0.00002

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

    rgbLed.brightness = rgbLed.brightness + brightnessStep
    if (rgbLed.brightness >= 0.1 or rgbLed.brightness <= 0):
        brightnessStep = brightnessStep * -1
