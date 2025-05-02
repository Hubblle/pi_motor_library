from time import sleep
import RPi.GPIO as GPIO

SPR = 200   # Steps per Revolution (360 / 1.8)
SPR = SPR * 16
delay = .004 / 16

class Motor:
    def __init__(self, motor_info : dict):
        self.motor_info = motor_info
        self.is_setup = 0
        

    def setup(self):
        motor = self.motor_info
        try :
            GPIO.setmode(GPIO.BCM)
            #Setup the switch up
            GPIO.setup(motor["SWITCH"], GPIO.IN)
            #setup the DIR and STEP pin
            GPIO.setup(motor["DIR"], GPIO.OUT)
            GPIO.setup(motor["STEP"], GPIO.OUT)
            self.is_setup = 1
        except Exception as e:
            return print(e)
        
    def high(self, step : int):
        motor_info = self.motor_info
        if self.is_setup == 0:
            print("This mottor wasn't setup.")
            return print("Aborting the program !")
        
        GPIO.output(motor_info["DIR"], 1)
        for i in range(step):
            GPIO.output(motor_info["STEP"], GPIO.HIGH)
            sleep(delay)
            GPIO.output(motor_info["STEP"], GPIO.LOW)
            sleep(delay)
            
    def low(self, step : int) :
        motor_info = self.motor_info
        if self.is_setup == 0:
            print("This mottor wasn't setup.")
            return print("Aborting the program !")
        
        GPIO.output(motor_info["DIR"], 0)
        for i in range(step):
            GPIO.output(motor_info["STEP"], GPIO.HIGH)
            sleep(delay)
            GPIO.output(motor_info["STEP"], GPIO.LOW)
            sleep(delay)