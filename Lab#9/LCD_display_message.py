#!/usr/bin/env python3

from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from sys import version_info
import time

if version_info.major == 3:
    raw_input = input
def print_msg():
    print ("========================================")
    print ("|                LCD1602               |")
    print ("|    ------------------------------    |")
    print ("|         GND connect to PIN 6         |")
    print ("|         VCC connect to PIN 2         |")
    print ("|         SDA connect to PIN 3         |")
    print ("|         SCL connect to PIN 5         |")
    print ("|                                      |")
    print ("|           Control LCD1602            |")
    print ("|                                      |")
    print ("|                            Khoi Duong|")
    print ("========================================\n")
    print ("Program is running...")
    print ("Please press Ctrl+C to end the program...")
    raw_input ("Press Enter to begin\n")

lcd = LCD()
def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

def main():
    print_msg()
    txt = "you did good job"
    txt2 = "--Khoi D 19610--"
    a = 0
    while True:
        lcd.text(txt2, 2)
        if a + 16 < len(txt):
            lcd.text(txt[a:a+16],1)
        if a + 16 >= len(txt):
            b = txt[a:len(txt)]
            c = 16 - len(b)
            lcd.text(b + '   ' + txt[0:c], 1)
        if a == len(txt):
            a = -1
        a += 1
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        lcd.clear()