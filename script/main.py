from time import sleep
import RPi.GPIO as GPIO
from motor_lib import Motor

Y_mottor_info = {
    "DIR" : 3, # Direction GPIO Pin
    "STEP" : 2, # Step GPIO Pin
    "SWITCH" : 4 # Switch GPIO Pin
}

X_mottor_info = {
    "DIR" : 27, # Direction GPIO Pin
    "STEP" : 17, # Step GPIO Pin
    "SWITCH" : 22 # Switch GPIO Pin
}

Z_mottor_info = {
    "DIR" : 9, # Direction GPIO Pin
    "STEP" : 10, # Step GPIO Pin
    "SWITCH" : 11 # Switch GPIO Pin
}

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 1.8)
EN = 18 # Enable GPIO Pin

Y_mottor = Motor(Y_mottor_info)
Y_mottor.setup()

X_mottor = Motor(X_mottor_info)

Z_mottor = Motor(Z_mottor_info)


step_count = SPR * 16
delay = .004 / 16

Y_mottor.high(SPR)
Y_mottor.low(SPR)

#stop the board and cleanup
GPIO.output(EN, GPIO.HIGH)
GPIO.cleanup()