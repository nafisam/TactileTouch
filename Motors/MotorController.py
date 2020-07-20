
import RPi.GPIO as GPIO
from gpiozero import InputDevice, OutputDevice, PWMOutputDevice
import time
GPIO.setmode(GPIO.BCM)
##GPIO.setwarnings(False)
import numpy as np
import math

left = 27
right = 25


motor_GPIO = [27, 25, 16, 12]
motor_00 = PWMOutputDevice(27)
motor_01 = PWMOutputDevice(25)
motor_10 = PWMOutputDevice(16)
motor_11 = PWMOutputDevice(12)

motors = np.array([[27, 0, 0], [25, 0, 1], [16, 1, 0], [12, 1, 1]])

intensity = [0,0,0,0]

def energy_function(motor_x, motor_y, touch_x, touch_y):
    beta_x = abs(motor_x-touch_x)/((motor_x+1)-motor_x)
    inside_square = 1 - beta_x
    if inside_square >= 0:
        phantom_h = math.sqrt(1-beta_x) * touch_x
        phantom_h_plus_1 = math.sqrt(beta_x) * touch_x
        beta_y = abs(motor_y - touch_y)/1
        return amplitude = math.sqrt(1-beta_y) * touch_y
    else:
        return amplitude = 0
        
def stop_vibration():
    GPIO.output(left,GPIO.LOW)
    GPIO.output(right,GPIO.LOW)

            
while True:
    for i in range 4:
        intensity[i] = energy_function
    motor_00.value = energy_function(0, 0, touch_x, touch_y)
    
    
                   
        
