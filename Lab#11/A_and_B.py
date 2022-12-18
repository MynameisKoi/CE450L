#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from sys import version_info

if version_info.major == 3:
	raw_input = input

SDI   = 17
RCLK  = 18
SRCLK = 27

per_line = [0xfe, 0xfd, 0xfb, 0xf7, 0xef, 0xdf, 0xbf, 0x7f]

charactors = {
	"A" : [0b00111100,0b00111100,0b01100110,0b01100110,0b01111110,0b01111110,0b01100110,0b01100110],
	"B" : [0b01111000,0b01111110,0b01100110,0b01111000,0b01111000,0b01100110,0b01111110,0b01111000]}

def print_msg():
    print ("========================================")
    print ("|      Dot matrix with two 74HC595     |")
    print ("|    ------------------------------    |")
    print ("|        SDI connect to GPIO17         |")
    print ("|        RCLK connect to GPIO18        |")
    print ("|        SRCLK connect to GPIO27       |")
    print ("|                                      |")
    print ("|   Control Dot matrix with 74HC595    |")
    print ("|                                      |")
    print ("|                            SunFounder|")
    print ("========================================")
    print ("Program is running...")
    print ("Please press Ctrl+C to end the program...")
    raw_input ("Press Enter to begin\n")


def setup():
	GPIO.setmode(GPIO.BCM)    # Number GPIOs by its BCM location
	GPIO.setup(SDI, GPIO.OUT)
	GPIO.setup(RCLK, GPIO.OUT)
	GPIO.setup(SRCLK, GPIO.OUT)
	GPIO.output(SDI, GPIO.LOW)
	GPIO.output(RCLK, GPIO.LOW)
	GPIO.output(SRCLK, GPIO.LOW)

# Shift the data to 74HC595
def hc595_in(dat):
	for bit in range(0, 8):
		GPIO.output(SDI, 1 & (dat >> bit))
		GPIO.output(SRCLK, GPIO.HIGH)
		time.sleep(0.000001)
		GPIO.output(SRCLK, GPIO.LOW)

def hc595_out():
	GPIO.output(RCLK, GPIO.HIGH)
	time.sleep(0.000001)
	GPIO.output(RCLK, GPIO.LOW)

def flash(table):
	for i in range(8):
		hc595_in(per_line[i])
		hc595_in(table[i])
		hc595_out()
	# Clean up last line
	hc595_in(per_line[7])
	hc595_in(0x00)
	hc595_out()

def show(table, second):
	start = time.time()
	while True:
		flash(table)
		finish = time.time()
		if finish - start > second:
			break

def main():
	word = 'AB'
	while True:
		for table in word:
			show(charactors[table],1)
		time.sleep(1)

def destroy():
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		main()
	except KeyboardInterrupt:
		destroy()