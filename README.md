# Menu_RPI_CAR
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
