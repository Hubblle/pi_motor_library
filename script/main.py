from time import sleep
import RPi.GPIO as GPIO

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 1.8)
EN = 2
SWITCH = 26

GPIO.setmode(GPIO.BCM)

#Enable the board
GPIO.setup(EN, GPIO.OUT)
GPIO.output(EN, GPIO.LOW)

#Setup the switch up
GPIO.setup(SWITCH, GPIO.IN)

GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

MODE = (25, 8, 7)   # Microstep Resolution GPIO Pins
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
GPIO.output(MODE, RESOLUTION['1/32'])

step_count = SPR
delay = .004 / 32

try :
    while True:
        print(GPIO.input(SWITCH))
        if GPIO.input(SWITCH) == GPIO.LOW:
            GPIO.output(DIR, CW)
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)

        elif GPIO.input(SWITCH) == GPIO.HIGH :
            GPIO.output(DIR, CCW)
            for x in range(step_count*5):
                GPIO.output(STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(STEP, GPIO.LOW)
                sleep(delay)

except :
    GPIO.output(EN, GPIO.HIGH)
    GPIO.cleanup()
    exit()

#stop the board and cleanup
GPIO.output(EN, GPIO.HIGH)
GPIO.cleanup()