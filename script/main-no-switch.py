from time import sleep
import RPi.GPIO as GPIO

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 1.8)
EN = 2

GPIO.setmode(GPIO.BCM)

#Enable the board
GPIO.setup(EN, GPIO.OUT)
GPIO.output(EN, GPIO.LOW)


GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

MODE = (25, 8, 7)   # Microstep Resolution GPIO Pins
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (1, 1, 1)}
GPIO.output(MODE, RESOLUTION['1/16'])

step_count = SPR * 16
delay = .004 / 16


for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)


#stop the board and cleanup
GPIO.output(EN, GPIO.HIGH)
GPIO.cleanup()