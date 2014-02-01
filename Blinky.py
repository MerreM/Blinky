import serial
import random
import signal
import sys
from time import sleep

stare  = [
[' ',' ',' ',' ',' ',' ',' ',' ',' ','#','#','#',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ','#',' '],
[' ','#','#',' ',' ',' ',' ',' ','#',' ',' ',' ','#',' '],
['#',' ',' ','#',' ',' ',' ',' ','#',' ',' ',' ','#',' '],
['#',' ',' ','#',' ',' ',' ',' ','#',' ',' ',' ','#',' '],
['#',' ',' ','#',' ',' ',' ',' ','#',' ',' ',' ','#',' '],
[' ','#','#',' ','#','#','#','#',' ','#','#','#',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
]
blink  = [
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
['#','#','#','#',' ',' ',' ',' ',' ','#','#','#','#',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ','#','#','#','#',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
]
suspicious1  = [
[' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ','#',' ',' '],
[' ',' ','#',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' '],
[' ','#',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' '],
['#',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' '],
[' ','#',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' '],
[' ',' ','#',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' '],
[' ',' ',' ',' ','#','#','#','#',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],

]
suspicious2  = [
[' ','#',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' '],
[' ',' ','#',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' '],
[' ',' ',' ','#',' ',' ',' ',' ',' ',' ','#',' ',' ',' '],
[' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ','#',' ',' '],
[' ',' ',' ','#',' ',' ',' ',' ',' ',' ','#',' ',' ',' '],
[' ',' ','#',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' '],
[' ',' ',' ',' ','#','#','#','#',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],

]


def faces_to_binary(face):
    output = "$$$F"
    for x in range(14):
        for y in range(9):
            output+='1' if (face[y][x]=='#') else '0'
    return output+"\r"


class PiLiteBoard(object):
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
        self.ser.write("$$$SPEED50\r")
        self.ser.write("$$$ALL,OFF\r")
        self.state = "OFF"
    def write(self, text):
        text = text.encode('utf-8')
        while text:
            self.ser.write(text[:14])
            text = text[14:]
            sleep(3)
    def stare(self):
        if not self.state == "stare":
            self.ser.write("$$$ALL,OFF\r")
            self.ser.write(faces_to_binary(stare))
        self.state = "stare"
	sleep(random.randint(1,5))
    def blink(self):
        self.ser.write("$$$ALL,OFF\r")
        self.ser.write(faces_to_binary(blink))
        sleep(0.5)
        self.ser.write("$$$ALL,OFF\r")
        self.ser.write(faces_to_binary(stare))
    def suspicious(self):
        self.ser.write("$$$ALL,OFF\r")
        self.ser.write(faces_to_binary(suspicious1))
        sleep(1)
        self.ser.write("$$$ALL,OFF\r")
        self.ser.write(faces_to_binary(suspicious2))
	sleep(1)
    def blinky(self):
        while True:
            choice = random.randint(0,100)
            if choice > 75:
                self.suspicious()
		self.blink()
            elif 50 < choice < 75:
                self.blink()
            else:
                self.stare()
	    sleep(1)

def main():
    pi = PiLiteBoard()
    pi.blinky()

if __name__ == "__main__":
    main()
