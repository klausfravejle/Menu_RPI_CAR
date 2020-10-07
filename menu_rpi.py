#! /usr/bin/env python
import GPIO_TEST as GPIO
import time
import random
from threading import Thread
from PIL import Image, ImageTk
import cv2

# ------------------------GPIO Mode ----------------------------
# choose BCM or BOARD
GPIO.setmode(GPIO.BCM)
# ------------------------GPIO PINS ----------------------------

TRIG = 17
ECHO = 27
TRIG1 = 18
ECHO1 = 28
led = 22
m11 = 16
m12 = 12
m21 = 21
m22 = 20

# Start ------------------------cv2 webcam settings ----------------------------
width, height = 600, 450
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
# End --------------------------cv2 webcam settings ----------------------------

suitauto = False
stopauto = 1
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import menu_rpi_support


def vp_start_gui():
    # '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root)
    menu_rpi_support.init(root, top)
    root.mainloop()

    w = None


def create_Toplevel1(rt, *args, **kwargs):
    # Starting point when module is imported by another module.
    # Correct form of call: 'create_Toplevel1(root, *args, **kwargs)'
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    menu_rpi_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
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
        # ----------------------Webcam-START -----------------------

        webset()
        # ----------------------Webcam - END -----------------------

        # ----------------------Forward button-----------------------
        self.forwardbutton = tk.Button(top)
        self.forwardbutton.place(relx=0.423, rely=0.667, height=42, width=80)
        self.forwardbutton.configure(activebackground="#ececec")
        self.forwardbutton.configure(activeforeground="#000000")
        self.forwardbutton.configure(background="#d9d9d9")
        self.forwardbutton.configure(command=forward)
        self.forwardbutton.configure(disabledforeground="#a3a3a3")
        self.forwardbutton.configure(foreground="#000000")
        self.forwardbutton.configure(highlightbackground="#d9d9d9")
        self.forwardbutton.configure(highlightcolor="black")
        self.forwardbutton.configure(pady="0")
        self.forwardbutton.configure(text='''Forward''')
        root.bind('w', forward)

        # ----------------------Right button-----------------------
        self.rightbutton = tk.Button(top)
        self.rightbutton.place(relx=0.567, rely=0.778, height=42, width=80)
        self.rightbutton.configure(activebackground="#ececec")
        self.rightbutton.configure(activeforeground="#000000")
        self.rightbutton.configure(background="#d9d9d9")
        self.rightbutton.configure(command=right)
        self.rightbutton.configure(disabledforeground="#a3a3a3")
        self.rightbutton.configure(foreground="#000000")
        self.rightbutton.configure(highlightbackground="#d9d9d9")
        self.rightbutton.configure(highlightcolor="black")
        self.rightbutton.configure(pady="0")
        self.rightbutton.configure(text='''Right''')
        root.bind('d', right)

        # ----------------------Left button-----------------------
        self.leftbutton = tk.Button(top)
        self.leftbutton.place(relx=0.283, rely=0.778, height=42, width=80)
        self.leftbutton.configure(activebackground="#ececec")
        self.leftbutton.configure(activeforeground="#000000")
        self.leftbutton.configure(background="#d9d9d9")
        self.leftbutton.configure(command=left)
        self.leftbutton.configure(disabledforeground="#a3a3a3")
        self.leftbutton.configure(foreground="#000000")
        self.leftbutton.configure(highlightbackground="#d9d9d9")
        self.leftbutton.configure(highlightcolor="black")
        self.leftbutton.configure(pady="0")
        self.leftbutton.configure(text='''Left''')
        root.bind('a', left)

        # ----------------------Back button-----------------------
        self.backbutton = tk.Button(top)
        self.backbutton.place(relx=0.423, rely=0.889, height=42, width=80)
        self.backbutton.configure(activebackground="#ececec")
        self.backbutton.configure(activeforeground="#000000")
        self.backbutton.configure(background="#d9d9d9")
        self.backbutton.configure(command=back)
        self.backbutton.configure(disabledforeground="#a3a3a3")
        self.backbutton.configure(foreground="#000000")
        self.backbutton.configure(highlightbackground="#d9d9d9")
        self.backbutton.configure(highlightcolor="black")
        self.backbutton.configure(pady="0")
        self.backbutton.configure(text='''Back''')
        root.bind('s', back)

        # ----------------------Auto button-----------------------
        self.autobutton = tk.Button(top)
        self.autobutton.place(relx=0.067, rely=0.667, height=42, width=54)
        self.autobutton.configure(activebackground="#ececec")
        self.autobutton.configure(activeforeground="#000000")
        self.autobutton.configure(background="#d9d9d9")
        self.autobutton.configure(command=automode)
        self.autobutton.configure(disabledforeground="#a3a3a3")
        self.autobutton.configure(foreground="#000000")
        self.autobutton.configure(highlightbackground="#d9d9d9")
        self.autobutton.configure(highlightcolor="black")
        self.autobutton.configure(pady="0")
        self.autobutton.configure(text='''Auto''')

# ----------------------Init GPIO-----------------------
def GPIO_init():
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(TRIG1, GPIO.OUT)
    GPIO.setup(ECHO1, GPIO.IN)
    GPIO.setup(led, GPIO.OUT)
    GPIO.setup(m11, GPIO.OUT)
    GPIO.setup(m12, GPIO.OUT)
    GPIO.setup(m21, GPIO.OUT)
    GPIO.setup(m22, GPIO.OUT)
GPIO_init()

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
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print("Car forward")


def back(_event=None):
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print("Car back")


def right(_event=None):
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print("Car right")


def left(_event=None):
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print("Car left")


def stop():
    print("Car stop")
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)


def automode():
    if __name__ == '__main__':
            t1 = Thread(target=automodeon)
            t1.setDaemon(True)
            t1.start()



def automodeon():
    if suitauto is True:
        print("Autostop")
    else:
        leftt = 0
        rightt = 0
        while True:
            # count = 0
            # i = 0
            avgDistance = 0
            for i in range(5):
                GPIO.output(TRIG, False)  # Set TRIG as LOW
                time.sleep(0.1)  # Delay

                GPIO.output(TRIG, True)  # Set TRIG as HIGH
                time.sleep(0.00001)  # Delay of 0.00001 seconds
                GPIO.output(TRIG, False)  # Set TRIG as LOW

                while GPIO.input(ECHO) == 0:  # Check whether the ECHO is LOW
                    GPIO.output(led, False)
                pulse_start = time.time()

                while GPIO.input(ECHO) == 1:  # Check whether the ECHO is HIGH
                    GPIO.output(led, False)
                pulse_end = time.time()
                pulse_duration = pulse_end - pulse_start  # time to get back the pulse to sensor

                distance = pulse_duration * 17150  # Multiply pulse duration by 17150 (34300/2) to get distance


                # ----------------------------- For testing on windows Start ---------------------------
                distance = random.randint(1, 32)
                distance = round(distance, 2)  # Round to two decimal points
                # ----------------------------- For testing on windows End  ---------------------------


                avgDistance = avgDistance + distance
                # print("Average distance cm =" + str(avgDistance))
            avgDistance = avgDistance / 5

            flag = 0

            if avgDistance < 15:  # Check whether the distance is within 15 cm range
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
                    rightt = rightt + 1
                    flag = 1

                else:
                    left()
                    leftt = leftt + 1
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


if __name__ == '__main__':
    vp_start_gui()
GPIO.cleanup()
