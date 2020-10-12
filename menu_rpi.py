#! /usr/bin/env python
# Enable this on Raspberry
# import RPi.GPIO as GPIO

import random
import time
import tkinter as tk
from threading import Thread

import cv2
from PIL import Image, ImageTk

# Disable this on Raspberry
import GPIO_TEST as GPIO


# ------------------------GPIO Mode ----------------------------
# choose BCM or BOARD
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
gpio_forward = 26  # pin 37

# Start ------------------------cv2 webcam settings ----------------------------
width, height = 600, 450
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


# End --------------------------cv2 webcam settings ----------------------------


def vp_start_gui():
    # '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root)
    init(root, top)
    root.mainloop()
    w = None


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def create_toplevel1(rt, *args, **kwargs):
    # Starting point when module is imported by another module.
    # Correct form of call: 'create_toplevel1(root, *args, **kwargs)'
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    init(w, top, *args, **kwargs)
    return (w, top)


def destroy_toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        # This class configures and populates the toplevel window.
        #   top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.geometry("600x450+650+150")
        top.minsize(176, 1)
        top.maxsize(1924, 1050)
        top.resizable(1, 1)
        top.title("Raspberry RC auto car")
        top.configure(background="#d9d9d9")

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

        self.Frame1 = tk.Frame(top)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")
        webset()

        # ----------------------Forward button-----------------------
        self.forward_button = tk.Button(top)
        self.forward_button.place(relx=0.423, rely=0.667, height=42, width=80)
        self.forward_button.configure(activebackground="#ececec")
        self.forward_button.configure(activeforeground="#000000")
        self.forward_button.configure(background="#d9d9d9")
        self.forward_button.configure(command=forward)
        self.forward_button.configure(disabledforeground="#a3a3a3")
        self.forward_button.configure(foreground="#000000")
        self.forward_button.configure(highlightbackground="#d9d9d9")
        self.forward_button.configure(highlightcolor="black")
        self.forward_button.configure(pady="0")
        self.forward_button.configure(text='''Forward''')
        root.bind('w', forward)

        # ----------------------Right button-----------------------
        self.right_button = tk.Button(top)
        self.right_button.place(relx=0.567, rely=0.778, height=42, width=80)
        self.right_button.configure(activebackground="#ececec")
        self.right_button.configure(activeforeground="#000000")
        self.right_button.configure(background="#d9d9d9")
        self.right_button.configure(command=right)
        self.right_button.configure(disabledforeground="#a3a3a3")
        self.right_button.configure(foreground="#000000")
        self.right_button.configure(highlightbackground="#d9d9d9")
        self.right_button.configure(highlightcolor="black")
        self.right_button.configure(pady="0")
        self.right_button.configure(text='''Right''')
        root.bind('d', right)

        # ----------------------Left button-----------------------
        self.left_button = tk.Button(top)
        self.left_button.place(relx=0.283, rely=0.778, height=42, width=80)
        self.left_button.configure(activebackground="#ececec")
        self.left_button.configure(activeforeground="#000000")
        self.left_button.configure(background="#d9d9d9")
        self.left_button.configure(command=left)
        self.left_button.configure(disabledforeground="#a3a3a3")
        self.left_button.configure(foreground="#000000")
        self.left_button.configure(highlightbackground="#d9d9d9")
        self.left_button.configure(highlightcolor="black")
        self.left_button.configure(pady="0")
        self.left_button.configure(text='''Left''')
        root.bind('a', left)

        # ----------------------Back button-----------------------
        self.back_button = tk.Button(top)
        self.back_button.place(relx=0.423, rely=0.889, height=42, width=80)
        self.back_button.configure(activebackground="#ececec")
        self.back_button.configure(activeforeground="#000000")
        self.back_button.configure(background="#d9d9d9")
        self.back_button.configure(command=back)
        self.back_button.configure(disabledforeground="#a3a3a3")
        self.back_button.configure(foreground="#000000")
        self.back_button.configure(highlightbackground="#d9d9d9")
        self.back_button.configure(highlightcolor="black")
        self.back_button.configure(pady="0")
        self.back_button.configure(text='''Back''')
        root.bind('s', back)

        # ----------------------Auto button-----------------------
        self.auto_button = tk.Button(top)
        self.auto_button.place(relx=0.067, rely=0.667, height=42, width=54)
        self.auto_button.configure(activebackground="#ececec")
        self.auto_button.configure(activeforeground="#000000")
        self.auto_button.configure(background="#d9d9d9")
        self.auto_button.configure(command=automode)
        self.auto_button.configure(disabledforeground="#a3a3a3")
        self.auto_button.configure(foreground="#000000")
        self.auto_button.configure(highlightbackground="#d9d9d9")
        self.auto_button.configure(highlightcolor="black")
        self.auto_button.configure(pady="0")
        self.auto_button.configure(text="Auto")


# ----------------------Init GPIO-----------------------


def gpio_init():
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(TRIG1, GPIO.OUT)
    GPIO.setup(ECHO1, GPIO.IN)
    GPIO.setup(led, GPIO.OUT)
    GPIO.setup(gpio_right, GPIO.OUT)
    GPIO.setup(gpio_back, GPIO.OUT)
    GPIO.setup(gpio_left, GPIO.OUT)
    GPIO.setup(gpio_forward, GPIO.OUT)


gpio_init()


def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


# ----------------------END show webcam function--------------------

def forward(_event=None):
    GPIO.output(gpio_right, 0)
    GPIO.output(gpio_back, 0)
    GPIO.output(gpio_left, 0)
    GPIO.output(gpio_forward, 1)
    print("Car forward")


def back(_event=None):
    GPIO.output(gpio_right, 0)
    GPIO.output(gpio_back, 1)
    GPIO.output(gpio_left, 0)
    GPIO.output(gpio_forward, 0)
    print("Car back")


def right(_event=None):
    GPIO.output(gpio_right, 1)
    GPIO.output(gpio_back, 0)
    GPIO.output(gpio_left, 0)
    GPIO.output(gpio_forward, 1)
    print("Car right")


def left(_event=None):
    GPIO.output(gpio_right, 0)
    GPIO.output(gpio_back, 0)
    GPIO.output(gpio_left, 1)
    GPIO.output(gpio_forward, 0)
    print("Car left")


def stop():
    print("Car stop")
    GPIO.output(gpio_right, 0)
    GPIO.output(gpio_back, 0)
    GPIO.output(gpio_left, 0)
    GPIO.output(gpio_forward, 0)


def automode():
    if __name__ == '__main__':
        t1 = Thread(target=automodeon)
        t1.setDaemon(True)
        t1.start()


# ----------------------flips True / False -----------------------
def flip(suitauto):
    return not suitauto


# ------Automodeon -  defines how the car drives on auto-----------------------
suitauto = True


def automodeon():
    global suitauto
    suitauto = flip(suitauto)

    if suitauto is True:
        print("Automode disabled!")
    else:
        print("Automode enabled!")
        while suitauto is False:
            avgdistance = 0
            for i in range(5):
                GPIO.output(TRIG, False)  # Set TRIG as LOW
                time.sleep(0.1)  # Delay

                GPIO.output(TRIG, True)  # Set TRIG as HIGH
                time.sleep(0.00001)  # Delay of 0.00001 seconds
                GPIO.output(TRIG, False)  # Set TRIG as LOW

                # while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
                #    GPIO.output(led, False)
                pulse_start = time.time()

                # while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
                #    GPIO.output(led, False)
                pulse_end = time.time()
                pulse_duration = pulse_end - pulse_start  # time to get back the pulse to sensor

                distance = pulse_duration * 17150  # Multiply pulse duration by 17150 (34300/2) to get distance

                # ----------------------------- For testing on windows Start ---------------------------
                distance = random.randint(1, 32)
                distance = round(distance, 2)  # Round to two decimal points
                # ----------------------------- For testing on windows End  ---------------------------

                avgdistance = avgdistance + distance
                # print("Average distance cm =" + str(avgdistance))
            avgdistance = avgdistance / 5

            flag = 0

            if avgdistance < 15:  # Check whether the distance is within 15 cm range
                stop()
                # time.sleep(1)
                time.sleep(0.5)
                back()
                # time.sleep(1.5)
                time.sleep(0.5)
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
                    # time.sleep(1.5)
                    time.sleep(0.5)
                    count = count + 1
                    stop()
                    # time.sleep(1)
                    time.sleep(0.5)
            else:
                forward()
                flag = 0


vp_start_gui()
GPIO.cleanup()
