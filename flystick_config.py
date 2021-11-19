"""
This "demo" configuration is for the most spartanly-named
"Thrustmaster USB Joystick" (http://www.thrustmaster.com/products/usb-joystick).
It was the cheapest joystick in my local electronics shop, and - as an added
bonus - it had just the throttle lever I wanted.
"""
from flystick_conf_models import *

stick = Joystick(0)

# Raspberry Pi GPIO pin where to output the PPM signal.
# Pin map: http://wiki.mchobby.be/images/3/31/RASP-PIZERO-Correspondance-GPIO.jpg
# (Connect this pin to the RC transmitter trainer port.)
PPM_OUTPUT_PIN = 18

# Output (PPM) channels.
CHANNELS = (
    # channel 1: aileron
    stick.axis(0),
    # channel 2: elevator (reversed)
    -stick.axis(1),
    # channel 3: throttle (reversed)
    -stick.axis(3),
    # channel 4: rudder (reversed)
    stick.axis(2),
    # channel 5: flight mode
    stick.hat_switch(hat=0, axis=1, positions=5),
    # channels 6-8: buttons demo
    stick.button(0),
    stick.button(1),
    stick.button(2),
)

