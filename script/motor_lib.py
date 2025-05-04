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
            print(f"The motor {self.name} was setup sucessfully.")
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
     
     
    def move(self, step : int):
        if self.is_setup == 0:
            print("This mottor wasn't setup.")
            return print("Aborting the program !")
        
        if step > 0:
            self.high(step)
        
        else :
            self.down(abs(step))
     
            
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
        GPIO.output(self.DIR, 0)
        while True :
            print(GPIO.input(self.SWITCH))
            if GPIO.input(self.SWITCH) == 1 :
                return print(f"The motor {self.name} was set to 0 on the main axis !")
            elif GPIO.input(self.SWITCH) == 0 :
                GPIO.output(self.STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(self.STEP, GPIO.LOW)
                sleep(delay)
                
                
                
                
                
                
class Stylus():
    def __init__(self, max : list):
        self.Y_motor = None
        self.X_motor = None
        self.Z_motor = None
        self.co_list = ["X", "Y", "Z"]
        self.max = max
        self.coordinate = None
        
    def add_motor(self, motor : object, axis : str):
        #cannot add a motor if the stylus was already setup :
        if not self.coordinate == None :
            return("The stylus was already setup, please add the motor before the setup.")
        #verify if the argument motor is an object from the motor class
        if not isinstance(motor, Motor)  :
            return print(f"Error, the motor {motor} isn't a motor.")
        #check if the axis is fine
        if not axis in ["X", "Y", "Z"] :
            return print("The selected axis isn't right !")
        
        #add the motor to the coresponding axis
        exec(f"self.{axis}_motor = motor")
        return print(f"The motor {motor.name} was sucessfully added to the {axis} axis.")
    
    def setup(self):
        #first set all the motors to 0
        for i in [self.X_motor, self.Y_motor, self.Z_motor] :
            if not i == None:
                i.reset()
                print(f"Reseting the {i.name} motor")
        
        print("The Stylus was setup sucessfully")
        #set the coordinate to the default
        self.coordinate = [0, 0, 0]
        
    def go_to(self, next_coordinate : list):
        #cannot move if the stylus isn't setup :
        if self.coordinate == None :
            return print("Error, the stylus wasn't setup yet.")
        
        for i in range(3) :
            if next_coordinate[i] - self.coordinate[i] != 0 and exec(f"self.{self.co_list[i]}_motor") == None :
                return print(f"Error, you tried to move an axis wich coresponding motor wasn't setup! Please setup the {self.co_list[i]} motor.")
            
            elif next_coordinate[i] > self.max[i] or next_coordinate[i] < 0 :
                return print(f"Error, you tried to reach a coordinate that is out of reach! The max for the {self.co_list[i]} axis is {self.max[i]} and min is 0, you tried {next_coordinate[i]}")
            
            else :
                mouvement = next_coordinate[i] - self.coordinate[i]
                exec(f"self.{self.co_list[i]}_motor.move({mouvement})")
                self.coordinate[i] = next_coordinate[i]
                
    def center(self):
        for i in range(3) :
            if exec(f"self.{self.co_list[i]}_motor") == None :
                return

            else :
                destination = self.max[i] / 2
                mouvement = destination - self.coordinate[i]
                exec(f"self.{self.co_list[i]}_motor.move({mouvement})")
                self.coordinate[i] = destination
                
        
                

    