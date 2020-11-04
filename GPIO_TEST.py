IN = " - IN"
OUT = " - OUT"
BCM = "BCM"


def setwarnings(A):
    pass


def setup(pin, inout):
    pass


def setmode(BCM):
    print("bcm on")


def output(pin, onoff):
    pin = str(pin)
    onoff = str(onoff)
    # config_object = ConfigParser()
    # config_object.read("config.ini")
    # pinonoff = config_object["PINON_OFF"]

    # pinonoff[pin] = onoff

    # with open('config.ini', 'w') as conf:
    #    config_object.write(conf)


def input(mpin):
    pass


def PWM(pin, dc):
    # print ("pin = " + str(pin) + " - dutycycle = " + str(dc))
    pass


def cleanup():
    pass


def pwm(gpio, pwm):
    # print ("GPIO PIN = " + str(gpio) + " AND pwm = " + str(pwm))
    pass
