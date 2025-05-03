from time import sleep
import RPi.GPIO as GPIO
from motor_lib import Motor

Z_motor_info = {
    "DIR" : 3, # Direction GPIO Pin
    "STEP" : 2, # Step GPIO Pin
    "SWITCH" : 4 # Switch GPIO Pin
}

X_motor_info = {
    "DIR" : 27, # Direction GPIO Pin
    "STEP" : 17, # Step GPIO Pin
    "SWITCH" : 22 # Switch GPIO Pin
}

Y_motor_info = {
    "DIR" : 9, # Direction GPIO Pin
    "STEP" : 10, # Step GPIO Pin
    "SWITCH" : 11 # Switch GPIO Pin
}

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 1.8)
EN = 18 # Enable GPIO Pin

Y_motor = Motor(Y_motor_info, "Y_motor")
Y_motor.setup()

X_motor = Motor(X_motor_info, "X_motor")

Z_motor = Motor(Z_motor_info, "Z_motor")


step_count = SPR * 16
delay = .004 / 16

Y_motor.high(SPR)
Y_motor.down(SPR)
Y_motor.reset()
Y_motor.down(step_count)

#stop the board and cleanup
GPIO.output(EN, GPIO.HIGH)
GPIO.cleanup()