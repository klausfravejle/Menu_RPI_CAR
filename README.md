# The setup
- 2 X HC-SR04 Ultrasonic Sensor on Raspberry Pi

- 1 X Raspberry PI 3B

- 1 X USB webcam

- 1 X Double BTS7960 43A High power motor driver module.

- 1 X L298 DC motor driver module
. Upgrades
To come:
 - 1 X Webcam Wide angle 5 MP

# Install dependencies
Instructions assume that you are using Raspbian Linux.

Python3 Install

sudo apt-get install python3-pip
sudo apt-get install python-pip

# Description
Controlling RC car using Raspberry PI, and 2 HC-SR04 Ultrasonic Sound Sensor. 

Returns an distance by using the median reading of 5 readings, if the distance is smaller that 15 cm, it stops and goes back, selecting a new route (left / right)

Uses BCM pin values by default. BOARD pin values are supported, by changing GPIO.setmode(GPIO.BCM) to GPIO.setmode(GPIO.BOARD), remember to setup the new PINS.


# Contributing
Contributions to hcsr04sensor are welcome. 


# Setup
import RPi.GPIO as GPIO - You need to uncomment this line, as i was writing the program on a windows machine.


You need to install the following modules.
opencv 2 (cv2)

pillow (PIL)


import GPIO_TEST as GPIO - Comment out this on Raspberry


# GPIO PINS

TRIG + TRIG1 = Goes to the HC-SR04 Trigger.

TRIG = 4  # pin 7

TRIG1 = 27  # pin 13

ECHO + ECHO1 = Goes to the Echo pins on the HC-SR04.

ECHO = 17  # pin 11

ECHO1 = 22  # pin 15 


led = Goes to lights for the RC car.

led = 18  # pin 12


The rest goes to the motor controller, selfexplained.

gpio_right = 5  # pin 29

gpio_back = 6  # pin 31

gpio_left = 13  # pin 33

gpio_forward = 26  # pin 37


Enjoy :-)
