
import RPi.GPIO as GPIO
from gpiozero import InputDevice, OutputDevice, PWMOutputDevice
import time
GPIO.setmode(GPIO.BCM)
##GPIO.setwarnings(False)
import numpy as np
import math
from time import sleep

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
    x = (motor_x-touch_x)
    if x < -1 or x > 1:
        amplitude = 0
    y = (motor_y-touch_y)
    beta_x = abs(motor_x-touch_x)/1
    beta_y = abs(motor_y-touch_y)/1
    if previous_x != 
    if -0.1 < x < 0.1:
        if -0.1 < y < 0.1:
            amplitude = 100
    elif -1 < x < 0:
        phantom_h_x = math.sqrt(1-beta_x) * 1
        if y <= 0:
            amplitude = math.sqrt(1-beta_y) * phantom_h_x
        elif y > 0:
            amplitude = math.sqrt(1-beta_y) * phantom_h_x
    elif 0 < x < 1:
        phantom_h_x_plus_1 = math.sqrt(1-beta_x) * 1
        if y <= 0:
            amplitude = math.sqrt(1-beta_y) * phantom_h_x_plus_1
        elif y > 0:
            amplitude = math.sqrt(1-beta_y) * phantom_h_x_plus_1
    
    previous_x = touch_x
    previous_y = touch_y
    return amplitude


        
def stop_vibration():
    GPIO.output(left,GPIO.LOW)
    GPIO.output(right,GPIO.LOW)

            
while True:
    amplitude = [0,0,0,0,0,0,0,0]
    amplitude[0] = energy_function(0, 0, touch_x, touch_y)
    amplitude[0] = energy_function(1, 0, touch_x, touch_y)
    amplitude[0] = energy_function(2, 0, touch_x, touch_y)
    amplitude[0] = energy_function(3, 0, touch_x, touch_y)
    amplitude[0] = energy_function(0, 1, touch_x, touch_y)
    amplitude[0] = energy_function(1, 1, touch_x, touch_y)
    amplitude[0] = energy_function(2, 1, touch_x, touch_y)
    amplitude[0] = energy_function(3, 1, touch_x, touch_y)
    
    motor_00.value = energy_function(0, 0, touch_x, touch_y)
    motor_10.value = energy_function(1, 0, touch_x, touch_y)
    motor_20.value = energy_function(2, 0, touch_x, touch_y)
    motor_30.value = energy_function(3, 0, touch_x, touch_y)
    motor_01.value = energy_function(0, 1, touch_x, touch_y)
    motor_11.value = energy_function(1, 1, touch_x, touch_y)
    motor_21.value = energy_function(2, 1, touch_x, touch_y)
    motor_31.value = energy_function(3, 1, touch_x, touch_y)
    
    
    
                   
        
