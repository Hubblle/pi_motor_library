from time import sleep
import RPi.GPIO as GPIO
import math
import asyncio

SPR = 200   # Steps per Revolution (360 / 1.8)
delay = 0.0005 # min 0.00001 acording to the datasheet (and that's sheet (sith : that's a joke))
# this is actually the min delay that's work in 1/2 micro step mode

        
        

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
        print(f"The motor {self.name} is going up for {step} steps.")
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
        print(f"The motor {self.name} is going down for {step} steps.")
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
            self.go_to([-1, -1, 200])
            return print("The Stylus is up /!\ ")
        
        
        
    def down(self) :
        if self.Z_motor == None :
            return print("Sorry, the Z motor wasn't setup yet, please, do 'Stylus.add_motor(motor, 'Z')")
        else :
            self.go_to([-1, -1, 0])
            return print("The Stylus is down /!\ ")
    
    
    def circle(self, radius : int):
        #first, verify all the motor
        print("Naaah, i was to lazy to code that one, sorry :>")
        
        
        
    def line(self, starting : list[int, int], end : list[int, int]):
        #first put the pen up
        self.up()

        #check if the max isn't exceded
        if end[0] > self.max[0]:
            self.down()
            return print(f"Sorry, but the given point is outside of the limit for the X axis, you gaved {end[0]} and the max is {self.max[0]}")
        
        if end[1] > self.max[1]:
            self.down()
            return print(f"Sorry, but the given point is outside of the limit for the X axis, you gaved {end[1]} and the max is {self.max[1]}")
        
        
        print("Starting the processing of the value with the bresenham algorithm")
        #use the bresenham algorithm to get all the pos of the x and y axis
        # define everything we need
        coordinate_by_step = []
        
        x0, y0 = starting
        x1, y1 = end
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x1 >= x0 else -1
        sy = 1 if y1 >= y0 else -1
        
        if dx > dy:
            err = dx // 2
            while x0 != x1:
                coordinate_by_step.append([x0, y0])
                print([x0, y0])
                err -= dy
                if err < 0:
                    y0 += sy
                    err += dx
                x0 += sx
        else:
            err = dy // 2
            while y0 != y1:
                coordinate_by_step.append([x0, y0])
                print([x0, y0])
                err -= dx
                if err < 0:
                    x0 += sx
                    err += dy
                y0 += sy
        coordinate_by_step.append([x1, y1])
        print("All value have been processed")
        
        #get to the starting point
        self.go_to([starting[0], starting[1], -1])
        self.down()
        #remove the first coordinate since we already got there
        coordinate_by_step.__delitem__(0)
        
        print("Processing the movement based on the value")
        mov_by_step = []
        
        last_co = [starting[0], starting[1]]
        
        for coordinate in coordinate_by_step :
            mov = [coordinate[0]-last_co[0], coordinate[1]-last_co[1]]
            print(mov)
            mov_by_step.append(mov)
            last_co = coordinate
            
        #Now, we do the movement for each axis and each step
        for mov in mov_by_step:
            self.move_axis(0, mov[0])
            self.move_axis(1, mov[1])
        
        #Now, actualise the coordinates
        self.coordinate[0] = end[0]
        self.coordinate[1] = end[1]
        
        #at the end, we put the pen up again, and print the result.
        self.up()
        
        return print("The line was drawn sucessfully !")
        
        
    