#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from sys import version_info

if version_info.major == 3:
    raw_input = input

# Set up pins
MotorPin1   = 17
MotorPin2   = 18
MotorEnable = 27
YellowLED = 24
RedLED = 23

def print_message():
    print ("========================================")
    print ("|                Motor                 |")
    print ("|    ------------------------------    |")
    print ("|     Motor pin 1 connect to GPIO17    |")
    print ("|     Motor pin 2 connect to GPIO18    |")
    print ("|     Motor enable connect to GPIO27   |")
    print ("|     YellowLED connect to GPIO24      |")
    print ("|     RedLED connect to GPIO23         |")
    print ("|                                      |")
    print ("|         Controlling a motor          |")
    print ("|                                      |")
    print ("|                            Khoi Duong|")
    print ("======================================\n")
    print ("Program is running...")
    print ("Please press Ctrl+C to end the program...")
    raw_input ("Press Enter to begin\n")

def setup():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set pins to output
    GPIO.setup(MotorPin1, GPIO.OUT)
    GPIO.setup(MotorPin2, GPIO.OUT)
    GPIO.setup(MotorEnable, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(YellowLED, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RedLED, GPIO.OUT, initial=GPIO.LOW)

# Define a motor function to spin the motor
# direction should be
# 1(clockwise), 0(stop), -1(counterclockwise)
def motor(direction):
    # Clockwise
    if direction == 1:
        # Set direction
        GPIO.output(MotorPin1, GPIO.HIGH)
        GPIO.output(MotorPin2, GPIO.LOW)
        # Enable the motor
        GPIO.output(MotorEnable, GPIO.HIGH)
        print ("Clockwise - Yellow")
    # Counterclockwise
    if direction == -1:
        # Set direction
        GPIO.output(MotorPin1, GPIO.LOW)
        GPIO.output(MotorPin2, GPIO.HIGH)
        # Enable the motor
        GPIO.output(MotorEnable, GPIO.HIGH)
        print ("Counterclockwise - Red")
    # Stop
    if direction == 0:
        # Disable the motor
        GPIO.output(MotorEnable, GPIO.LOW)
        print ("Stop")

def main():
    print_message()
    # Define a dictionary to make the script more readable
    # CW as clockwise, CCW as counterclockwise, STOP as stop
    directions = {'CW': 1, 'CCW': -1, 'STOP': 0}
    while True:
        # Clockwise
        motor(directions['CW'])
        GPIO.output(YellowLED, GPIO.HIGH)
        GPIO.output(RedLED, GPIO.LOW)
        time.sleep(5)
        # Stop
        motor(directions['STOP'])
        GPIO.output(YellowLED, GPIO.LOW)
        GPIO.output(RedLED, GPIO.LOW)
        time.sleep(2)
        # Anticlockwise
        motor(directions['CCW'])
        GPIO.output(RedLED, GPIO.HIGH)
        GPIO.output(YellowLED, GPIO.LOW)
        time.sleep(5)
        # Stop
        motor(directions['STOP'])
        GPIO.output(YellowLED, GPIO.LOW)
        GPIO.output(RedLED, GPIO.LOW)
        time.sleep(2)

def destroy():
    # Stop the motor
    GPIO.output(MotorEnable, GPIO.LOW)
    GPIO.output(RedLED, GPIO.LOW)
    GPIO.output(YellowLED, GPIO.LOW)
    # Release resource
    GPIO.cleanup()

# If run this script directly, do:
if __name__ == '__main__':
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the child program
    # destroy() will be executed.
    except KeyboardInterrupt:
        destroy()

