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


step_count = SPR * 16
delay = .004 / 16

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