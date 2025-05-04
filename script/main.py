from time import sleep
import RPi.GPIO as GPIO
from motor_lib import Motor, Stylus

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

GPIO.setmode(GPIO.BCM)
GPIO.setup(EN, GPIO.OUT)

Y_motor = Motor(Y_motor_info, "Y_motor")
Y_motor.setup

X_motor = Motor(X_motor_info, "X_motor")

Z_motor = Motor(Z_motor_info, "Z_motor")


Main_stylus = Stylus([1, 5000, 1])
Main_stylus.add_motor(Y_motor, "Y")
Main_stylus.setup()

step_count = SPR * 16
delay = .004 / 16

try:
    input("Press enter to start the program.")
    Main_stylus.go_to([0, 1000, 0])
    sleep(1)
    Main_stylus.go_to([0, 0, 0])
            
except KeyboardInterrupt :
    #stop the board and cleanup
    GPIO.output(EN, GPIO.HIGH)
    GPIO.cleanup()
    exit()

#stop the board and cleanup
GPIO.output(EN, GPIO.HIGH)
GPIO.cleanup()
exit()