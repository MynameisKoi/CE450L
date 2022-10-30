import RPi.GPIO as GPIO
import time
import threading

from sys import version_info

if version_info.major == 3:
    raw_input = input

SDI = 24
RCLK = 23
SRCLK = 18

placePin = (10, 22, 27, 17)
text = (0x8b, 0xcf, 0xff, 0x91, 0xa3, 0xe3, 0xff, 0xa1, 0xcf, 0xa1,
        0xff, 0xc2, 0xa3, 0xa3, 0xa1, 0xff, 0xe1, 0xa3, 0x83, 0xff)

counter = 0
timer1 = 0

def clearDisplay():
    for i in range(8):
        GPIO.output(SDI, 1)
        GPIO.output(SRCLK, GPIO.HIGH)
        GPIO.output(SRCLK, GPIO.LOW)
    GPIO.output(RCLK, GPIO.HIGH)
    GPIO.output(RCLK, GPIO.LOW)

def hc595_shift(data):
    for i in range(8):
        GPIO.output(SDI, 0x80 & (data << i))
        GPIO.output(SRCLK, GPIO.HIGH)
        GPIO.output(SRCLK, GPIO.LOW)
    GPIO.output(RCLK, GPIO.HIGH)
    GPIO.output(RCLK, GPIO.LOW)

def print_msg():
    print ("========================================")
    print ("|     Display 'hi you did good job'    |")
    print ("|    ------------------------------    |")
    print ("|        SDI connect to GPIO24         |")
    print ("|        RCLK connect to GPIO23        |")
    print ("|        SRCLK connect to GPIO18       |")
    print ("|                                      |")
    print ("|  Control 7-seg display with 74HC595  |")
    print ("|                                      |")
    print ("|                            SunFounder|")
    print ("========================================")
    print ("Program is running...")
    print ("Please press Ctrl+C to end the program...")
    raw_input ("Press Enter to begin\n")


def pickDigit(digit):
    for i in placePin:
        GPIO.output(i,GPIO.LOW)
    GPIO.output(placePin[digit], GPIO.HIGH)

def timer():
    global counter
    global timer1
    timer1 = threading.Timer(0.2, timer)
    timer1.start()
    print("%d" % counter)
    if counter > 22:
        counter = 1
    else:
        counter += 1


def main():
    global counter
    print_msg()
    global timer1
    timer1 = threading.Timer(0.2, timer)
    timer1.start()
    while True:
        if counter < 19:
            clearDisplay()
            pickDigit(0)
            hc595_shift(text[counter])
        if counter > 0 and counter < 20:
            clearDisplay()
            pickDigit(1)
            hc595_shift(text[counter-1])
        if counter > 1 and counter < 21:
            clearDisplay()
            pickDigit(2)
            hc595_shift(text[counter-2])
        if counter > 2 and counter < 22:
            clearDisplay()
            pickDigit(3)
            hc595_shift(text[counter-3])

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    for i in placePin:
        GPIO.setup(i, GPIO.OUT)

def destroy():   # When "Ctrl+C" is pressed, the function is executed.
    global timer1
    GPIO.cleanup()
    timer1.cancel()  # cancel the timer

if __name__ == '__main__':
    setup()
    try:
        main()
    #except IndexError:
     #   destroy()
    except KeyboardInterrupt:
        destroy()