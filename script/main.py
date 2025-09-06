from time import sleep
import RPi.GPIO as GPIO
import json
from motor_lib import Motor, Stylus

with open("./script/config.json", "r") as raw_conf:
    config = json.load(raw_conf)
Z_motor_info = config["Z_motor_info"]

X_motor_info = config["X_motor_info"]

Y_motor_info = config["Y_motor_info"]

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 1.8)
EN = 18 # Enable GPIO Pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(EN, GPIO.OUT)

Y_motor = Motor(Y_motor_info, "Y_motor", 0, 1)
Y_motor.setup()

X_motor = Motor(X_motor_info, "X_motor", 0, 1)
X_motor.setup()

Z_motor = Motor(Z_motor_info, "Z_motor", 0, 1)
Z_motor.setup()


Main_stylus = Stylus([2599, 2543, 6530])
Main_stylus.add_motor(Y_motor, "Y")
Main_stylus.add_motor(X_motor, "X")
Main_stylus.add_motor(Z_motor, "Z")
Main_stylus.setup()

step_count = SPR * 16

try:
    pass
            
except KeyboardInterrupt :
    #stop the board and cleanup
    GPIO.output(EN, GPIO.HIGH)
    GPIO.cleanup()
    exit()

def cleanup():
    #stop the board and cleanup
    GPIO.output(EN, GPIO.HIGH)
    GPIO.cleanup()
    exit()