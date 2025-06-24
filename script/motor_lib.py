from time import sleep
import RPi.GPIO as GPIO
import math
import asyncio

SPR = 200   # Steps per Revolution (360 / 1.8)
delay = 0.002

def locate(element, input_list : list) :
    for i in range(len(input_list)) :
        if input_list[i] == element:
            return i
        
    return None
        
        

class Motor:
    def __init__(self, motor_info : dict, name : str, d_d : int, d_u : int):
        self.motor_info = motor_info
        self.is_setup = 0
        self.name = name
        self.DIR = motor_info["DIR"]
        self.SWITCH = motor_info["SWITCH"]
        self.STEP = motor_info["STEP"]
        self.dir_down = d_d
        self.dir_up = d_u
        

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

        
        GPIO.output(self.DIR, self.dir_up)
        print(f"The motor {self.name} is going up for {step} 1/16 steps.")
        STEP = self.STEP
        for i in range(step):
            GPIO.output(STEP, 1)
            sleep(delay)
            GPIO.output(STEP, 0)
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

        
        GPIO.output(self.DIR, self.dir_down)
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
        GPIO.output(self.DIR, self.dir_down)
        while True :
            print(GPIO.input(self.SWITCH))
            if GPIO.input(self.SWITCH) == 1 :
                sleep(0.2)
                if GPIO.input(self.SWITCH) == 0 :
                    pass
                elif GPIO.input(self.SWITCH) == 1:
                    return print(f"The motor {self.name} was set to 0 on the main axis !")
            elif GPIO.input(self.SWITCH) == 0 :
                GPIO.output(self.STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(self.STEP, GPIO.LOW)
                sleep(delay)
                
    def get_max(self):
        if self.is_setup == 0:
            print("This mottor wasn't setup.")
            return print("Aborting the program !")
        
        
        print("Warning ! If the motor is not placed at his maximum, the result could be falsed.")
        input("Press enter to confirm.")
        motor_max = 0
        GPIO.output(self.DIR, self.dir_down)
        while True :
            print(GPIO.input(self.SWITCH))
            if GPIO.input(self.SWITCH) == 1 :
                sleep(0.2)
                if GPIO.input(self.SWITCH) == 0 :
                    pass
                elif GPIO.input(self.SWITCH) == 1:
                    return print(f"The motor {self.name} has a maximum of {motor_max} step.")
            elif GPIO.input(self.SWITCH) == 0 :
                motor_max += 1
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
        self.full_setup = False
        
        
        
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
        if axis == "X":
            self.X_motor = motor
        elif axis == "Y":
            self.Y_motor = motor
        else :
            self.Z_motor = motor
        
        return print(f"The motor {motor.name} was sucessfully added to the {axis} axis.")
    
    
    
    
    def setup(self):
        #first set all the motors to 0
        setup_motor = 0
        for motor in [self.X_motor, self.Y_motor, self.Z_motor] :
            if not motor == None:
                setup_motor += 1
                motor.reset()
                print(f"Reseting the {motor.name} motor")
        
        if setup_motor == 3 :
            self.full_setup = True
        
        print("The Stylus was setup sucessfully")
        #set the coordinate to the default
        self.coordinate = [0, 0, 0]
        
        
        
        
    def go_to(self, next_coordinate : list):
        motor_list = [self.X_motor, self.Y_motor, self.Z_motor]
        #cannot move if the stylus isn't setup :
        if self.coordinate == None :
            return print("Error, the stylus wasn't setup yet.")
        

        for i in range(len(self.co_list)) :
            if next_coordinate[i] == -1 :
                pass
            
            elif next_coordinate[i] - self.coordinate[i] != 0 and i == None :
                return print(f"Error, you tried to move an axis wich coresponding motor wasn't setup! Please setup the {self.co_list[i]} motor.")
            
            elif next_coordinate[i] > self.max[i] or next_coordinate[i] < 0 :
                return print(f"Error, you tried to reach a coordinate that is out of reach! The max for the {self.co_list[i]} axis is {self.max[i]} and min is 0, you tried {next_coordinate[i]}")
            
            elif next_coordinate[i] != self.coordinate[i] :
                mouvement = next_coordinate[i] - self.coordinate[i]
                self.move_axis(i, mouvement)
                
                
                
                
    def center(self):
        motor_list = [self.X_motor, self.Y_motor, self.Z_motor]
        for i in range(len(motor_list)) :
            
            destination = self.max[i] / 2
            movement = destination - self.coordinate[i]
            self.move_axis(i, movement)
            self.coordinate[i] = destination
                
                
                
    def move_axis(self, axis : str, movement : int) :
        i = axis
        if self.coordinate[i] + movement < 0 or self.coordinate[i] + movement > self.max[i] :
            return print(f"Error, you tried to reach a coordinate that is out of reach! The max for the {self.co_list[i]} axis is {self.max[i]} and min is 0, you tried {self.coordinate[i] + movement}")
                
        if axis == 0 :
            self.X_motor.move(movement)
        elif axis == 1 :
            self.Y_motor.move(movement)
        elif axis == 2 :
            self.Z_motor.move(movement)
        else :
            return print("Error, the axis you gaved isn't right.")
        
        self.coordinate[i] += movement
        
        
        
    def up(self) :
        if self.Z_motor == None :
            return print("Sorry, the Z motor wasn't setup yet, please, do 'Stylus.add_motor(motor, 'Z')")
        else :
            self.go_to([-1, -1, 15])
            return print("The Stylus is up /!\ ")
        
        
        
    def down(self) :
        if self.Z_motor == None :
            return print("Sorry, the Z motor wasn't setup yet, please, do 'Stylus.add_motor(motor, 'Z')")
        else :
            self.go_to([-1, -1, 0])
            return print("The Stylus is up /!\ ")
    
    
    def circle(self, radius : int):
        #first, verify all the motor
        print("Naaah, i was to lazy to code that one, sorry :>")
        
        
        
    def line(self, starting : list[int, int], end : list[int, int], mode : str):
        #first put the pen up
        self.up()
        
        #after that, get to the starting point 
        self.go_to([starting[0], starting[1], -1])
        
        #calc the motion so when can create tow async tasks
        if mode == "point" :
            x_motion_value = end[0] - starting[0]
            y_motion_value = end[1] - starting[1]
        
        elif mode == "vector" :
            x_motion_value = end[0]
            y_motion_value = end[1]
            
        else :
            return print("Wrong mode choosen, please select 'point' or 'vector' .")
        
        #now that we have to motion for both of the axis, we just have to create tow async task
        async def x_motion_task(self, x_motion):
            #do the motion we deffined previously
            self.move_axis("X", movement=x_motion)
            
        async def y_motion_task(self, y_motion):
            #do the motion we deffined previously
            self.move_axis("Y", movement=y_motion)
            
        #now, we just have to put the pen down, and do both tasks at the same time
        async def draw():
            await asyncio.gather(x_motion_task(self=self, x_motion=x_motion_value), y_motion_task(self=self, y_motion=y_motion_value))
        
        asyncio.run(draw)
        
        #at the end, we put the pen up again, and print the result.
        
        self.up()
        
        return print("The line was drawn sucessfully !")
        
        
    