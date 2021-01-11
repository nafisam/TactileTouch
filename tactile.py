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

# Prepare the UDP connection
UDP_IP = "10.0.0.99"
print "Receiver IP: ", UDP_IP
UDP_PORT = 50000
print "Port: ", UDP_PORT
sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
#sock.settimeout(1)
# 
# print("UDP target IP: %s" % UDP_IP)
#    8 print("UDP target port: %s" % UDP_PORT)
#    9 print("message: %s" % MESSAGE)
#   10 
#   11 sock = socket.socket(socket.AF_INET, # Internet
#   12                      socket.SOCK_DGRAM) # UDP
#   13 sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
coordinates = [[0,1], [0,1], [0,1], [0,1]]
motors = np.array([[27, 0, 0], [25, 0, 1], [16, 1, 0], [12, 1, 1]])
motor_GPIO = [17, 27, 12, 5, 21, 16, 22, 13]
# motor_01 = PWMLED(17)
# motor_11 = PWMLED(27)
# motor_21 = PWMLED(12)
# motor_31 = PWMLED(5)
# motor_00 = PWMLED(21)
# motor_10 = PWMLED(16)
# motor_20 = PWMLED(22)
# motor_30 = PWMLED(13)


motor_31 = PWMLED(17)
motor_21 = PWMLED(27)
motor_11 = PWMLED(13)
motor_01 = PWMLED(5)
motor_30 = PWMLED(21)
motor_20 = PWMLED(16)
motor_10 = PWMLED(12)
motor_00 = PWMLED(22)

#motor 01 is now motor 3,1
#motor 11 is now motor 2,1
#motor 2,1 is now motor 1,1
#motor 3,1 is now motor 0,1
#motor 00 is now motor motor 3,0
#motor 10 is now motor 2,0
#motor 2,0 is now motor 1,0
#motor 3,0 is now motor 00
# motor_31 = PWMLED(17) #motor31
# motor_21 = PWMLED(27) #motor21
# motor_11 = PWMLED(12) #motor11
# motor_01 = PWMLED(5)  #motor01
# motor_30 = PWMLED(21)
# motor_20 = PWMLED(16)
# motor_10 = PWMLED(22)
# motor_00 = PWMLED(13)
# intensity = [0,0,0,0]

def energy_function(motor_x, motor_y, touch_x, touch_y):

    #print("\n")
    motor_x = motor_x + 0.5
    if motor_y == 0:
        motor_y = motor_y + 1.5
    elif motor_y == 1:
        motor_y = motor_y - 0.5
        
    global previous_x
    global previous_y
    #print (previous_x)
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
    if -0.01 < x < 0.01:
        return 100
    if x <= -1 or x >= 1:
        previous_x = touch_x
        previous_y = touch_y
        amplitude = 0
        return amplitude
    y = motor_y-touch_y


    if -0.01 < y < 0.01: 
        return 100
    
    
    beta_x = abs(motor_x-touch_x)
    beta_y = abs(motor_y-touch_y)
    
    previous_x_coord_plus_1 = (previous_x // 1) + 1
    previous_x_coord_minus_1 = (previous_x // 1) - 1
#     if (touch_x // 1) == previous_x_coord_plus_1 or (touch_x // 1) == previous_x_coord_minus_1:
#         amplitude = -1
#         print("this is x+ 1 and x - 1 " + str(previous_x_coord_plus_1) + str(previous_x_coord_minus_1) + "\n")
#         print(touch_x // 1)

    if -0.01 < x < 0.01: # on x axis
        #print(y)
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
    return amplitude

def get_data():
    print("entered data")
    try:
        data, addr = sock.recvfrom(1024)
        return data
    except sock.timeout as e:
        print(e)

previous_x = -2
previous_y = -2
counter = 0
amplitude_array = [0,0,0,0,0,0,0,0,0]
naf = 0
stop_time = time.time() + 1
while True:   
#     sock.setblocking(0)
#     ready = select.select([sock], [], [], 60)
#     if ready[0]:
# #         ready[0]:
    data, addr = sock.recvfrom(1024)
    counter = counter + 1
    print (data)
    if data == "0,down" or data == "1,down" or data == "2,down" or data == "3,down" or data == "up":
        print ("i'm in the if loop")
        continue

    
    else:
        #print data
        #file1 = open("go_to_middle_then_back_to_left", "a")
        #file1.write("Test Number:" + str(1) + "\n")
        #file1.write(data)
        #file1.write("\n")
        #x, y= map(float, data.strip('()').split(','))
        
        x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, x7, y7, x8, y8, x9, y9, x10, y10 = map(float, data.strip('()').replace('(','').replace(')','').split(','))
        
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
        #amplitude_array[8]=energy_function(0,0,1.0566666,1.5033333)
        print "debug"
            
        

       
        
        
           
          #motor_00.value = amplitude[0]
               # motor_10.value = amplitude[1]
                #motor_20.value = amplitude[2]
                #motor_30.value = amplitude[3]
        #motor_01.value = amplitude_array[4]
        #sleep(4)
                #motor_11.value = amplitude[5]
                #motor_21.value = amplitude[6]
        
    #motor_31.value = amplitude[7]
        
        if amplitude_array[0] == 100:
            motor_00.value = 0
#             print("sleeping")
#             print("sleeping")
#             print("sleeping")
#             print("sleeping\n\n\n\n\n\n\n\n\n\n")
            time.sleep(0.03)
        else:
#             print("i am vibrating 00")
#             print("Amplitude 0 " + str(amplitude_array[0]) + " please fucking work\n")
            motor_00.value = amplitude_array[0]
            
        if amplitude_array[1] == 100:
            motor_10.value = 0
            time.sleep(0.03)
        else:
            motor_10.value = 0
    #         print("Amplitude 1 " + str(amplitude_array[1]) + " please fucking work\n")
    #         print("i am vibrating 10")
            motor_10.value = amplitude_array[1]
            
        if amplitude_array[2] == 100:
            motor_20.value = 0
            time.sleep(0.03)
        else:
            motor_20.value = 0
    #         print("Amplitude 2 " + str(amplitude_array[2]) + " please fucking work\n")
    #         print("i am vibrating 20")
            motor_20.value = amplitude_array[2]
            
        if amplitude_array[3] == 100:
            motor_30.value = 0
            time.sleep(0.03)
        else:
            motor_30.value = 0
    #         print("Amplitude 3 " + str(amplitude_array[3]) + " please fucking work\n")
    #         print("i am vibrating 30")
            motor_30.value = amplitude_array[3]
            
        if amplitude_array[4] == 100:
            motor_01.value = 0
#             print("sleeping")
#             print("sleeping")
#             print("sleeping")
#             print("sleeping\n\n\n\n\n\n\n\n\n\n")
            time.sleep(0.03)
        else:
            motor_01.value = 0
    #         print("Amplitude 4 " + str(amplitude_array[4]) + " please fucking work\n")
    #         print("i am vibrating 01")
            motor_01.value = amplitude_array[4]
            
        if amplitude_array[5] == 100:
            motor_11.value = 0
            time.sleep(0.03)
        else:
            motor_11.value = 0
    #         print("Amplitude 5 " + str(amplitude_array[5]) + " please fucking work\n")
    #         print("i am vibrating 11")
            motor_11.value = amplitude_array[5]
            
        if amplitude_array[6] == 100:
            motor_21.value = 0
            time.sleep(0.03)
        else:
            motor_21.value = 0
    #         print("Amplitude 6 " + str(amplitude_array[6]) + " please fucking work\n")
    #         print("i am vibrating 21")
            motor_21.value = amplitude_array[6]
            
        if amplitude_array[7] == 100:
            motor_31.value = 0
            time.sleep(0.03)
        else:
            motor_31.value = 0
    #         print("Amplitude 7 " + str(amplitude_array[7]) + " please fucking work\n")
    #         print("i am vibrating 31")
            motor_31.value = amplitude_array[7]
        #ile1.close()
# 
#                   
#     else:
#          # exits the program 
#         sys.exit("Frames " + str(counter))  
#         print counter
#         x1 = 100
#         y1 = 100
#         x2 = 100
#         y2 = 100
#         x3 = 100
#         y3 = 100
#         x4 = 100
#         y4 = 100
#         x5 = 100
#         y5 = 100
#         x6 = 100
#         y6 = 100
#         x7 = 100
#         y7 = 100
#         x8 = 100
#         y8 = 100
#         x9 = 100
#         y9 = 100
#         x10 = 100
#         y10 = 100
#     
#    