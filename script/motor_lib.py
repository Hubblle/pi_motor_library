from time import sleep
import RPi.GPIO as GPIO

SPR = 200   # Steps per Revolution (360 / 1.8)
SPR = SPR * 16
delay = .004 / 16

class Motor:
    def __init__(self, motor_info : dict, name : str):
        self.motor_info = motor_info
        self.is_setup = 0
        self.name = name
        self.DIR = motor_info["DIR"]
        self.SWITCH = motor_info["SWITCH"]
        self.STEP = motor_info["STEP"]
        

    def setup(self):
        motor = self.motor_info
        try :
            GPIO.setmode(GPIO.BCM)
            #Setup the switch up
            GPIO.setup(self.SWITCH, GPIO.IN)
            #setup the DIR and STEP pin
            GPIO.setup(self.DIR, GPIO.OUT)
            GPIO.setup(self.STEP, GPIO.OUT)
            GPIO.output(self.STEP, GPIO.LOW)
            GPIO.output(self.DIR, 1)
            self.is_setup = 1
        except Exception as e:
            return print(e)
        
    def high(self, step : int):
        if self.is_setup == 0:
            print("This mottor wasn't setup.")
            return print("Aborting the program !")

        
        GPIO.output(self.DIR, 1)
        print(f"The motor {self.name} is going up for {step} 1/16 steps.")
        for i in range(step):
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(delay)
     
     
            
    def down(self, step : int) :
        if self.is_setup == 0:
            print("This mottor wasn't setup.")
            return print("Aborting the program !")

        
        GPIO.output(self.DIR, 0)
        print(f"The motor {self.name} is going down for {step} 1/16 steps.")
        for i in range(step):
            GPIO.output(self.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.STEP, GPIO.LOW)
            sleep(delay)
            
            
            
    def reset(self):
        if self.is_setup == 0:
            print("This mottor wasn't setup.")
            return print("Aborting the program !")

        
        print(f"Setting the motor {self.name} to 0 on the main axis.")
        GPIO.output(self.DIR, 1)
        while True :
            if GPIO.input(self.SWITCH) == 1 :
                return print(f"The motor {self.name} was set to 0 on the main axis !")
            elif GPIO.input(self.SWITCH) == 0 :
                GPIO.output(self.STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(self.STEP, GPIO.LOW)
                sleep(delay)
                
                
class Stylus():
    def __init__(self):
        self.Y_motor = None
        self.X_motor = None
        self.Z_motor = None
        self.coordinate = None
        
    def add_motor(self, motor, axis):
        #first verify if an object from the motor class
        if not motor == Motor :
            return print(f"Error, the motor {motor} isn't a motor.")

    