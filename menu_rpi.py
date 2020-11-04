#! /usr/bin/env python
# https://www.bluetin.io/sensors/python-library-ultrasonic-hc-sr04/
#  ------------------------Imports ----------------------------
import platform
import random
import time
import tkinter as tk
from configparser import ConfigParser
from threading import Thread

import cv2
from PIL import Image, ImageTk

# ------------------------Set ----------------------------
pwmvalue = 40
webcam_exists = True
is_on_auto = True
dist = 50
debug = False
spnum = int(0)


# ------------------------Simple print ------------------------
def sp(pp):
    if debug is True:
        global spnum
        spnum = int(spnum) + 1
        print(pp)
        print(". . . . . . . . . . . . .")
    else:
        pass


# ------------------------Read config.ini file ----------------------------
config_object = ConfigParser()
config_object.read("config.ini")
PINS = config_object["PINS"]
GPIO_SETTINGS = config_object["GPIO_SETTINGS"]
OPENCV = config_object["OPENCV"]
MISC = config_object["MISC"]
PINON_OFF = config_object["PINON_OFF"]
DUTY = config_object["DUTY"]

trig = (format(PINS["trig"]))
trig1 = (format(PINS["trig1"]))
echo = (format(PINS["echo"]))
echo1 = (format(PINS["echo1"]))
led = (format(PINS["led"]))
gpio_side = (format(PINS["gpio_side"]))
gpio_forward = (format(PINS["gpio_forward"]))
gpio_back = (format(PINS["gpio_back"]))
setm = (format(GPIO_SETTINGS["setm"]))

width = int(format(OPENCV["width"]))
height = int(format(OPENCV["height"]))
sleeprun = float(format(MISC["sleep"]))
duty_cycle_right = float(format(DUTY["duty_cycle_right"]))
duty_cycle_left = float(format(DUTY["duty_cycle_left"]))
duty_cycle_center = float(duty_cycle_left) + (float(duty_cycle_right) - float(duty_cycle_left)) / 2

# ------------------------GPIO Mode/warnings ----------------------------
if platform.system() == 'Windows':
    oswin = True
else:
    oswin = False

if oswin is True:
    sp("Windows system")
    import GPIO_TEST as GPIO
else:
    # setmode = BCM or BOARD
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    import RPi.GPIO as GPIO

    sp("Linux system")

# ------------------------cv2 webcam settings ----------------------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def randint1_10():
    return random.randint(1, 10)


def strtofloat(value):
    try:
        float(value)
        return float(value)
    except ValueError:
        return "Could not convert to float!!"


# --------------------------tkinter - Make GUI  ----------------------------


def vp_start_gui():
    global w, root
    root = tk.Tk()
    global top
    top = Toplvl1(root)
    init(root, top)
    root.mainloop()
    w = None


def init(top, gui):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def create_toplevel1(rt, *args, **kwargs):
    global w, w_win, root
    rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Toplvl1(w)
    # init(w, top, *args, **kwargs)
    init(w, top)
    return w, top


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

        def set_pwm(newvalue):
            global pwmvalue
            pwmvalue = newvalue
            var.set("Speed  = " + str(newvalue))

            sp("Speed  = " + str(newvalue))

        def leftKey(left):
            global pwmvalue
            if int(pwmvalue) > 20:
                pwmvalue = int(pwmvalue) - 10
                self.scale_speed.set(pwmvalue)
                var.set("Speed  = " + str(pwmvalue))

        def rightKey(right):
            global pwmvalue
            if int(pwmvalue) < 100:
                pwmvalue = int(pwmvalue) + 10
                self.scale_speed.set(pwmvalue)
                var.set("Speed  = " + str(pwmvalue))

        def stopKey(stopKey):
            stop()
            sp("STOP - User input!")

        if oswin is True:
            root.iconbitmap('icon.ico')
            pass
        else:
            pass
        global var
        var = tk.StringVar()
        if webcam_exists is False:
            pass
        else:
            webset()

        global label
        self.label = tk.Label(root)
        # IF SCALING IS ENABLED USE THIS = rely=0.12
        self.label.place(relx=0, rely=0.12, height=25, width=642)
        self.label.configure(textvariable=var)
        var.set("Raspberry PI - Self driving - Car")

        # ----------------------Scale slider-----------------------
        self.scale_speed = tk.Scale(top)
        self.scale_speed.set(30)
        self.scale_speed.place(relx=0, rely=0, height=58, width=645)
        self.scale_speed.configure(command=set_pwm, orient=tk.HORIZONTAL, label="Speed control", from_=20, to=100)
        self.scale_speed.configure(resolution=10)
        top.bind('<Left>', leftKey)
        top.bind('<Right>', rightKey)
        top.bind('<Return>', stopKey)

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
            if is_on_auto is True:
                text_for_auto_button = "Auto ON"
                top.title = "Auto mode on!!!"
            else:
                text_for_auto_button = "Auto OFF"

            self.auto_button = tk.Button(top)
            self.auto_button.place(relx=0.067, rely=0.8, height=42, width=74)
            self.auto_button.configure(command=automode)
            self.auto_button.configure(text=text_for_auto_button)

        auto_button()


# ----------------------Init GPIO-----------------------
sp("Init GPIO")
GPIO.setup(int(trig), GPIO.OUT)
GPIO.setup(int(echo), GPIO.IN)
GPIO.setup(int(trig1), GPIO.OUT)
GPIO.setup(int(echo1), GPIO.IN)
GPIO.setup(int(led), GPIO.OUT)
GPIO.setup(int(gpio_side), GPIO.OUT)
GPIO.setup(int(gpio_back), GPIO.OUT)

GPIO.setup(int(gpio_forward), GPIO.OUT)
forward_pwm = GPIO.PWM(int(gpio_forward), 50)
back_pwm = GPIO.PWM(int(gpio_back), 50)
turn_pwm = GPIO.PWM(int(gpio_side), 50)


def forward(_event=None):
    global pwmvalue
    if oswin is True:
        pass
    else:
        turn_pwm.start(7.5)
        time.sleep(0.2)
        turn_pwm.start(0)
        back_pwm.start(0)
        forward_pwm.start(int(pwmvalue))
    var.set("Forward - Distance is = " + str(get_distance()) + " cm")
    sp("Forward")


def back(_event=None):
    if oswin is True:
        pass
    else:
        turn_pwm.start(7.5)
        time.sleep(0.2)
        forward_pwm.start(0)
        back_pwm.start(int(pwmvalue))
    var.set("Back - Distance is = " + str(get_distance()) + " cm")
    sp("Back")


def right(_event=None):
    if oswin is True:
        pass
    else:
        # duty cycle
        turn_pwm.start(10)
        time.sleep(0.2)
        turn_pwm.start(0)

    var.set("Right - Distance is = " + str(get_distance()) + " cm")
    sp("Right")


def left(_event=None):
    if oswin is True:
        pass
    else:

        turn_pwm.start(5)
        time.sleep(0.2)
        turn_pwm.start(0)

    var.set("Left - Distance is = " + str(get_distance()) + " cm")
    sp("Left")


def stop():
    if oswin is True:
        pass

    else:
        forward_pwm.start(0)
        back_pwm.start(0)
        turn_pwm.start(0)
    var.set("Stop")
    sp("Stop")


# START ------------automodeon -  starts automodeon using Thread ------
def automode():
    if __name__ == '__main__':
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
    lmain.after(100, show_frame)


# ----------------------flips True = False -------------------------
def flip(is_on_auto):
    return not is_on_auto


# START ------------Automodeon -  defines how the car drives on auto------
def get_distance():
    GPIO.output(int(trig), False)
    time.sleep(0.2)
    GPIO.output(int(trig), True)
    time.sleep(0.00001)
    GPIO.output(int(trig), False)
    start = time.time()

    pulse_start = 0
    while time.time() - start < 0.1:
        if GPIO.input(int(echo)) == True:
            pulse_start = time.time()
            break
        time.sleep(0.0001)

    pulse_end = 0
    while time.time() - start < 0.1:
        if GPIO.input(int(echo)) == False:
            pulse_end = time.time()
            break
        time.sleep(0.0001)

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = (random.randint(1, 100))

    sp(round(distance, 2))
    return round(distance, 2)


def automodeon():
    global is_on_auto
    is_on_auto = flip(is_on_auto)
    if is_on_auto is True:
        var.set("Automode disabled!")
        sp("Automode disabled!")
    else:
        var.set("Automode enabled!")
        sp("Automode enabled!")
        while is_on_auto is False:
            avgdistance = 0

            avgdistance = get_distance()

            if avgdistance > (dist):
                sp("more than " + str(dist) + "cm")
                forward()


            elif avgdistance < (dist):

                sp("less than " + str(dist) + "cm")

                forward_pwm.start(20)
                back()
                time.sleep(1.5)
                last_left = random.choice([True, False])

                if last_left is True:
                    back_pwm.start(20)
                    right()
                    last_left = False
                    sp("Right")

                else:
                    left()
                    last_left = True
                    sp("Left")


vp_start_gui()
sp("GPIO Cleanup!!")
GPIO.cleanup()
