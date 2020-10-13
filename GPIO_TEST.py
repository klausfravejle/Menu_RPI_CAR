def setwarnings(warnings):
    if warnings == True:
        debug == True
        print("Debug True")


BCM = "BCM"
def setmode (BCM):
    #if BCM == BCM:
    print("BCM")
    pass


IN = " - IN"
OUT = " - OUT"
def setup (pin, inout):
    # print("GPIO Setup" + str(pin) + inout + str(inout))
    # print(str(pin) + inout)
    pass


def output(mpin, onoff):
    # print ("mpin out is " + str(mpin) + "and is " + str(onoff))
    pass


def input(mpin):
    # print ("mpin in is " + str(mpin))
    pass

def cleanup():
    pass

RPI_REVISION = 3

I2C=""
SPI=""
HARD_PWM=""
SERIAL=""
UNKNOWN=""
gpio_function=""