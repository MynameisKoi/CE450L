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
number = (0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90)
alphabet = (0x88, 0x83, 0xa7, 0xa1, 0x86, 0x8e, 0xc2, 0x8b,
            0xcf, 0xe1, 0x8a, 0xc7, 0xd4, 0xab, 0xa3, 0x8c, 0x98, 0xaf,
            0x92, 0x87, 0xe3, 0xd5, 0x81, 0xb6, 0x91, 0x92, 0xff)

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
    print ("|          Display 1-25 and a-z        |")
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
    timer1 = threading.Timer(0.5, timer)
    timer1.start()
    print("%d" % counter)
    if counter > 51:
        counter = 1
    else:
        counter += 1


def main():
    global counter
    print_msg()
    global timer1
    timer1 = threading.Timer(0.5, timer)
    timer1.start()
    while True:
        if counter < 26:
            clearDisplay()
            pickDigit(0)
            hc595_shift(number[counter % 10])

            clearDisplay()
            pickDigit(1)
            hc595_shift(number[counter % 100//10])
        else:
            clearDisplay()
            pickDigit(0)
            hc595_shift(alphabet[counter - 26])

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
    except IndexError:
        destroy()
    except KeyboardInterrupt:
        destroy()