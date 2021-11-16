import RPi.GPIO as GPIO
from gpiozero import PWMLED
import time
GPIO.setmode(GPIO.BCM)
##GPIO.setwarnings(False)
import numpy as np
import math
from array import *
import socket
import struct
from struct import *
import select
import sys
#adding i2c imports
from board import SCL, SDA 
import busio
from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime

# looking for an active Ethernet or WiFi device
def find_interface():
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name

# find an active IP on the first LIVE network device and return IP address
def parse_ip():
    find_ip = "ip addr show %s" % interface
    find_ip = "ip addr show %s" % interface
    ip_parse = run_cmd(find_ip)
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]
    return ip

# Finds an active connection and its IP address
interface = find_interface()
ip_address = parse_ip()
# Prepare the UDP connection
UDP_IP = ip_address
print ("Receiver IP: ", UDP_IP)
UDP_PORT = 50000
print ("Port: ", UDP_PORT)
sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


from adafruit_pca9685 import PCA9685
# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 60

#Implementation of syncopated energy algorithm
#Calculates the amplitudes of the motors to simulate the tactile gestures
def energy_function(motor_x, motor_y, touch_x, touch_y):

    motor_x = motor_x + 0.5
    if motor_y == 0:
        motor_y = motor_y + 1.5
    elif motor_y == 1:
        motor_y = motor_y - 0.5
        
    global previous_x
    global previous_y
    
    #If the touch gestures is out of bounds, return amplitude of 0
    if touch_x == -1 or touch_y == -1:
        previous_x = touch_x
        previous_y = touch_y
        return 0
    if touch_x == 100:
        previous_x = touch_x
        previous_y = touch_y
        return 0
    if touch_y == 100:
        previous_x = touch_x
        previous_y = touch_y
        return 0
    x = (motor_x-touch_x)
    
    #Crossing a new gridline, set amplitude to zero
    if -0.01 < x < 0.01:
        return 100
    if x <= -1 or x >= 1:
        previous_x = touch_x
        previous_y = touch_y
        amplitude = 0
        return amplitude
    y = motor_y-touch_y

    
    #Crossing a new gridline, set amplitude to zero
    if -0.01 < y < 0.01: 
        return 100
    
    
    beta_x = abs(motor_x-touch_x)
    beta_y = abs(motor_y-touch_y)
    
    previous_x_coord_plus_1 = (previous_x // 1) + 1
    previous_x_coord_minus_1 = (previous_x // 1) - 1


    if -0.01 < x < 0.01: # on x axis
        phantom_h_x = math.sqrt(1-beta_x) * 1
        if -0.01 < y < 0.01:
            amplitude = 100
            return amplitude
        elif y <= 0:
            amplitude = math.sqrt(abs(1-beta_y)) * phantom_h_x
        elif y > 0:
            amplitude = math.sqrt(abs(1-beta_y)) * phantom_h_x 
    elif -1 < x < 0:
        phantom_h_x = math.sqrt(1-beta_x) * 1
        if y <= 0:
            amplitude = math.sqrt(abs(1-beta_y)) * phantom_h_x
        elif y > 0:
            amplitude = math.sqrt(abs(1-beta_y)) * phantom_h_x
    elif 0 < x < 1:
        phantom_h_x_plus_1 = math.sqrt(1-beta_x) * 1
        if y <= 0:
            amplitude = math.sqrt(abs(1-beta_y)) * phantom_h_x_plus_1
        elif y > 0:
            amplitude = math.sqrt(abs(1-beta_y)) * phantom_h_x_plus_1
    
    previous_x = touch_x
    previous_y = touch_y
    
    #Hexadecimal Conversion of amplitude for PCA9685
    decimal_amplitude = round(65535 * amplitude)
    hex_conversion_amp = hex(decimal_amplitude)
    new_amp = int(hex_conversion_amp,16)
    return new_amp

def get_data():
    print("entered data")
    try:
        data, addr = sock.recvfrom(1024)
        data = touchIns.decode('utf-8', 'replace')
        return data
    except sock.timeout as e:
        print(e)

previous_x = -2
previous_y = -2
counter = 0

#Array that holds the amplitude values calculates from the energy function
amplitude_array = [0,0,0,0,0,0,0,0,0]

stop_time = time.time() + 1

#main loop
while True:
    #Sets up UDP connection with Indira's applications
    sock.setblocking(0)
    ready = select.select([sock], [], [], 3)
    if ready[0]:
        touchIns, addr = sock.recvfrom(1024)
        data = touchIns.decode('utf-8', 'replace')
        counter = counter + 1
        print (data)
        #We first get messages of how many fingers are down or if a finger was released
        #We don't do anything with these messages so we just ignore them
        if data == "0,down" or data == "1,down" or data == "2,down" or data == "3,down" or data == "4,down" or data == "5,down" or data == "6,down" or data == "7,down" or data == "8,down" or data == "9,down" or data == "up":
            print ("Data Received")
            continue

        
        else:
            #Strips the touch coordinates of parenthesis, commas, spaces,
            #and assigns them to the appropriate x, y variables
            x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, x10, y10 = map(float, data.strip('()').replace('(','').replace(')','').split(','))
            
            #For every touch coordinate received from the app, we calculate the max amplitude each motor
            #contributes to simulate that touch gesture and stores them in the amplitude array
            amplitude_array[4] = max(energy_function(0, 0, x1, y1), energy_function(0, 0, x2, y2), energy_function(0, 0, x3, y3), \
                                 energy_function(0, 0, x4, y4), energy_function(0, 0, x5, y5), energy_function(0, 0, x6, y6), \
                                 energy_function(0, 0, x7, y7), energy_function(0, 0, x8, y8), energy_function(0, 0, x9, y9), \
                                 energy_function(0, 0, x10, y10))

            amplitude_array[5] = max(energy_function(1, 0, x1, y1), energy_function(1, 0, x2, y2), energy_function(1, 0, x3, y3), \
                                     energy_function(1, 0, x4, y4), energy_function(1, 0, x5, y5), energy_function(1, 0, x6, y6), \
                                     energy_function(1, 0, x7, y7), energy_function(1, 0, x8, y8), energy_function(1, 0, x9, y9), \
                                     energy_function(1, 0, x10, y10))
            amplitude_array[6] = max(energy_function(2, 0, x1, y1), energy_function(2, 0, x2, y2), energy_function(2, 0, x3, y3), \
                                     energy_function(2, 0, x4, y4), energy_function(2, 0, x5, y5), energy_function(2, 0, x6, y6), \
                                     energy_function(2, 0, x7, y7), energy_function(2, 0, x8, y8), energy_function(2, 0, x9, y9), \
                                     energy_function(2, 0, x10, y10))
            amplitude_array[7] = max(energy_function(3, 0, x1, y1), energy_function(3, 0, x2, y2), energy_function(3, 0, x3, y3), \
                                     energy_function(3, 0, x4, y4), energy_function(3, 0, x5, y5), energy_function(3, 0, x6, y6), \
                                     energy_function(3, 0, x7, y7), energy_function(3, 0, x8, y8), energy_function(3, 0, x9, y9), \
                                     energy_function(3, 0, x10, y10))
            amplitude_array[0] = max(energy_function(0, 1, x1, y1), energy_function(0, 1, x2, y2), energy_function(0, 1, x3, y3), \
                                     energy_function(0, 1, x4, y4), energy_function(0, 1, x5, y5), energy_function(0, 1, x6, y6), \
                                     energy_function(0, 1, x7, y7), energy_function(0, 1, x8, y8), energy_function(0, 1, x9, y9), \
                                     energy_function(0, 1, x10, y10))
            amplitude_array[1] = max(energy_function(1, 1, x1, y1), energy_function(1, 1, x2, y2), energy_function(1, 1, x3, y3), \
                                     energy_function(1, 1, x4, y4), energy_function(1, 1, x5, y5), energy_function(1, 1, x6, y6), \
                                     energy_function(1, 1, x7, y7), energy_function(1, 1, x8, y8), energy_function(1, 1, x9, y9), \
                                     energy_function(1, 1, x10, y10))
            amplitude_array[2] = max(energy_function(2, 1, x1, y1), energy_function(2, 1, x2, y2), energy_function(2, 1, x3, y3), \
                                     energy_function(2, 1, x4, y4), energy_function(2, 1, x5, y5), energy_function(2, 1, x6, y6), \
                                     energy_function(2, 1, x7, y7), energy_function(2, 1, x8, y8), energy_function(2, 1, x9, y9), \
                                     energy_function(2, 1, x10, y10))
            amplitude_array[3] = max(energy_function(3, 1, x1, y1), energy_function(3, 1, x2, y2), energy_function(3, 1, x3, y3), \
                                     energy_function(3, 1, x4, y4), energy_function(3, 1, x5, y5), energy_function(3, 1, x6, y6), \
                                     energy_function(3, 1, x7, y7), energy_function(3, 1, x8, y8), energy_function(3, 1, x9, y9), \
                                     energy_function(3, 1, x10, y10))

        #The follolwing code uses the hexadecimal amplitude from the energy function
        # to set the amplitude of each motor through the PCA channels
        
            #If the amplitude array had a value of 100, then we are at a gridline and
            # the motor will be off (sleeping) for 30 ms
            if amplitude_array[0] == 100:
                pca.channels[0].duty_cycle = 0x0000
                time.sleep(0.03)
            else:
                #Sets the amplitude of the motor from the amplitude array
                 pca.channels[0].duty_cycle = amplitude_array[0]
                
            if amplitude_array[1] == 100:
                pca.channels[1].duty_cycle = 0x0000
                time.sleep(0.03)
            else:
                pca.channels[1].duty_cycle = amplitude_array[1]
                
            if amplitude_array[2] == 100:
                pca.channels[2].duty_cycle = 0x0000
                time.sleep(0.03)
            else:
                pca.channels[2].duty_cycle = amplitude_array[2]
                
            if amplitude_array[3] == 100:
                pca.channels[3].duty_cycle = 0x0000
                time.sleep(0.03)
            else:
                pca.channels[3].duty_cycle = amplitude_array[3]
                
            if amplitude_array[4] == 100:
                pca.channels[4].duty_cycle = 0x0000
                time.sleep(0.03)
            else:
                pca.channels[4].duty_cycle = amplitude_array[4]
                
            if amplitude_array[5] == 100:
                pca.channels[5].duty_cycle = 0x0000
                time.sleep(0.03)
            else:
                pca.channels[5].duty_cycle = amplitude_array[5]
                
            if amplitude_array[6] == 100:
                pca.channels[6].duty_cycle = 0x0000
                time.sleep(0.03)
            else:
                pca.channels[6].duty_cycle = amplitude_array[6]
                
            if amplitude_array[7] == 100:
                pca.channels[7].duty_cycle = 0x0000
                time.sleep(0.03)
            else:
                pca.channels[7].duty_cycle = amplitude_array[7]
# 
#                   
    else:
         # exits the program
        for channel in range(8):
            pca.channels[channel].duty_cycle = 0x0000
        
