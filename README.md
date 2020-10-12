# Menu_RPI_CAR
You need to uncomment this line, as i was writing the program on a windows machine.
# import RPi.GPIO as GPIO

You need to install the following modules.
opencv 2 (cv2)
pillow (PIL)
Comment this line out, because of windows programming
# Disable this on Raspberry
import GPIO_TEST as GPIO


https://www.google.com/url?sa=i&url=https%3A%2F%2Fdocs.microsoft.com%2Fen-us%2Fwindows%2Fiot-core%2Flearn-about-hardware%2Fpinmappings%2Fpinmappingsrpi&psig=AOvVaw1jc-PY9cHE5bM75SeY_a4N&ust=1602577275042000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCOjYitzPruwCFQAAAAAdAAAAABAJ
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
