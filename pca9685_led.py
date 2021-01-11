# This simple test outputs a 50% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.

from board import SCL, SDA
import busio
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

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 80

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.

pca.channels[1].duty_cycle = 0xFFFF
time.sleep(2)
pca.channels[1].duty_cycle = 0x3FFF
time.sleep(2)
pca.channels[1].duty_cycle = 0x0000
time.sleep(2)
pca.channels[1].duty_cycle = 0xFFFF
time.sleep(2)
pca.channels[1].duty_cycle = 0x3FFF
time.sleep(2)
pca.channels[1].duty_cycle = 0x0000
