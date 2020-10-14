#! /usr/bin/env python
import platform
import time
import tkinter as tk
from threading import Thread

# import RPi.GPIO as GPIO
import cv2
from PIL import Image, ImageTk

import GPIO_TEST as GPIO

global PwmValue
import random

PwmValue = 50
sleeprun = 0.2
# pwncmd="GPIO.PWM"
pwncmd = "GPIO.OUTPUT"
# ------------------------GPIO Mode ----------------------------
# setmode = BCM or BOARD
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# ------------------------GPIO PINS ----------------------------
# BCM / BOARD Setup pins
# https://www.google.com/url?sa=i&url=https%3A%2F%2Fdocs.microsoft.com%2Fen-us%2Fwindows%2Fiot-core%2Flearn-about-hardware%2Fpinmappings%2Fpinmappingsrpi&psig=AOvVaw1jc-PY9cHE5bM75SeY_a4N&ust=1602577275042000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCOjYitzPruwCFQAAAAAdAAAAABAJ
TRIG = 4  # pin 7
ECHO = 17  # pin 11
TRIG1 = 27  # pin 13
ECHO1 = 22  # pin 15
led = 18  # pin 12
gpio_right = 5  # pin 29
gpio_back = 6  # pin 31
gpio_left = 13  # pin 33
gpio_forward = int(26)  # pin 37
pwmled = 21
# Check if running on windows system.
if platform.system() == 'Windows':
    oswin = True
else:
    oswin = False

# Start ------------------------cv2 webcam settings ----------------------------
width, height = 600, 450
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# End --------------------------cv2 webcam settings ----------------------------
def vp_start_gui():

    global val, w, root
    root = tk.Tk()
    global top
    top = Toplvl1(root)
    init(root, top)
    root.mainloop()
    w = None


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def create_toplevel1(rt, *args, **kwargs):
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Toplvl1(w)
    init(w, top, *args, **kwargs)
    return (w, top)


def destroy_toplevel1():
    global w
    w.destroy()
    w = None



class Toplvl1:
    def __init__(self, top=None):
        top.title("Raspberry RC auto car")


        def webset():
            global lmain
            lmain = tk.Label(top)
            lmain.pack()
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

        def setPwm(newvalue):
            global pwmValue
            newValue = int(newvalue)
            pwmValue = (newvalue)
            var.set("Speed  = " + newvalue)

        root.iconbitmap('icon.ico')
        global var
        var = tk.StringVar()
        webset()
        # ----------------------LABEL-------------------------------

        global label
        self.label = tk.Label(root)
        # self.label.pack()
        self.label.place(relx=0, rely=0.12, height=25, width=642)
        self.label.configure(textvariable=var)

        # ----------------------Forward button-----------------------
        self.forward_button = tk.Button(top)
        self.forward_button.place(relx=0.423, rely=0.667, height=42, width=80)
        self.forward_button.configure(background="#d9d9d9")
        self.forward_button.configure(command=forward)
        self.forward_button.configure(text='''Forward''')
        root.bind('w', forward)

        # ----------------------Right button-----------------------
        self.right_button = tk.Button(top)
        self.right_button.place(relx=0.567, rely=0.778, height=42, width=80)
        self.right_button.configure(command=right)
        self.right_button.configure(text='''Right''')
        root.bind('d', right)

        # ----------------------Scale slider-----------------------
        self.scale_speed = tk.Scale(top)
        self.scale_speed.set(80)
        self.scale_speed.place(relx=0, rely=0, height=58, width=645)
        self.scale_speed.configure(command=setPwm, orient=tk.HORIZONTAL, label="Speed control")

        # ----------------------Left button-----------------------
        self.left_button = tk.Button(top)
        self.left_button.place(relx=0.283, rely=0.778, height=42, width=80)
        self.left_button.configure(command=left)
        self.left_button.configure(text='''Left''')
        root.bind('a', left)

        # ----------------------Back button-----------------------
        self.back_button = tk.Button(top)
        self.back_button.place(relx=0.423, rely=0.889, height=42, width=80)
        self.back_button.configure(command=back)
        self.back_button.configure(text='''Back''')
        root.bind('s', back)

        # ----------------------Auto button-----------------------
        global text_for_auto_button
        text_for_auto_button = "Auto"
        global auto_button


        def auto_button():
            if suitauto is True:
                text_for_auto_button = "Auto ON"
                top.title = "Auto mode on!!!"
            else:
                text_for_auto_button = "Auto OFF"

            self.auto_button = tk.Button(top)
            self.auto_button.place(relx=0.067, rely=0.8, height=42, width=74)
            self.auto_button.configure(command=automode)
            self.auto_button.configure(text=text_for_auto_button)

        auto_button()


global pwmValue
pwmValue = ""

# ----------------------Init GPIO-----------------------
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(gpio_right, GPIO.OUT)
GPIO.setup(gpio_back, GPIO.OUT)
GPIO.setup(gpio_left, GPIO.OUT)
GPIO.setup(gpio_forward, GPIO.OUT)


def forward(_event=None):
    GPIO.output(gpio_right, 0)
    GPIO.output(gpio_back, 0)
    GPIO.output(gpio_left, 0)
    time.sleep(sleeprun)
    GPIO.PWM(gpio_back, 0)
    global pwmvalue
    var.set("Forward")


def back(_event=None):
    GPIO.output(gpio_right, 0)
    GPIO.PWM(gpio_back, pwmValue)
    GPIO.output(gpio_left, 0)
    GPIO.output(gpio_forward, 0)
    time.sleep(sleeprun)
    GPIO.PWM(gpio_back, 0)
    var.set("Back")


def right(_event=None):
    GPIO.output(gpio_right, 1)
    GPIO.output(gpio_back, 0)
    GPIO.output(gpio_left, 0)
    GPIO.output(gpio_forward, 1)
    time.sleep(sleeprun)
    GPIO.output(gpio_forward, 0)
    GPIO.output(gpio_right, 0)
    var.set("Right")

def left(_event=None):
    GPIO.output(gpio_right, 0)
    GPIO.output(gpio_back, 0)
    GPIO.output(gpio_left, 1)
    GPIO.output(gpio_forward, 1)
    time.sleep(sleeprun)
    GPIO.output(gpio_forward, 0)
    GPIO.output(gpio_left, 0)
    var.set("Left")

def stop():
    GPIO.output(gpio_right, 0)
    GPIO.output(gpio_back, 0)
    GPIO.output(gpio_left, 0)
    GPIO.output(gpio_forward, 0)
    var.set("Stop")

# START ------------automodeon -  starts automodeon using Thread ------
def automode():
    if __name__ == '__main__':
        firstrun=False
        auto_button()

        t1 = Thread(target=automodeon)
        t1.setDaemon(True)
        t1.start()


# ----------------------START show webcam function--------------------
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


# ----------------------flips True = False -------------------------
def flip(suitauto):
    return not suitauto


# START ------------Automodeon -  defines how the car drives on auto------
suitauto = True
def automodeon():
    global suitauto
    suitauto = flip(suitauto)
    if suitauto is True:
        var.set("Automode disabled!")

    else:
        var.set("Automode enabled!")
        while suitauto is False:
            avgdistance = 0
            for i in range(5):
                GPIO.output(TRIG, False)  # Set TRIG as LOW
                time.sleep(0.1)  # Delay

                GPIO.output(TRIG, True)  # Set TRIG as HIGH
                time.sleep(0.00001)  # Delay of 0.00001 seconds
                GPIO.output(TRIG, False)  # Set TRIG as LOW

                pulse_start = time.time()
                pulse_end = time.time()
                while oswin is True and GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW and os is win
                    GPIO.output(led, False)
                    pulse_start = time.time()

                while oswin is True and GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH and os is win
                    GPIO.output(led, False)
                    pulse_end = time.time()
                pulse_duration = pulse_end - pulse_start  # time to get back the pulse to sensor
                distance = pulse_duration * 17150  # Multiply pulse duration by 17150 (34300/2) to get distance
                avgdistance = avgdistance + distance
            avgdistance = avgdistance / 5

            flag = 0

            if oswin is True:
                avgdistance = (random.randint(13, 17))
            if avgdistance < 15:  # Check whether the distance is within 15 cm range
                stop()
                time.sleep(1)
                back()
                time.sleep(1.5)
                try:
                    count = count + 1
                except NameError:
                    count = 0

                if (count % 3 == 1) & (flag == 0):
                    right()
                    flag = 1

                else:
                    left()

                    flag = 0
                    time.sleep(1.5)
                    count = count + 1
                    stop()
                    time.sleep(1)
            else:
                forward()
                flag = 0
# END ------------Automodeon -  defines how the car drives on auto------

vp_start_gui()
GPIO.cleanup()
