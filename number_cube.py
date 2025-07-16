#!/usr/bin/env python3

import time, RPi.GPIO as GPIO
from gpiozero import Button
from luma.core.interface.serial import i2c
from luma.oled.device           import sh1106
from luma.core.render           import canvas
from mfrc522                    import SimpleMFRC522
from PIL import ImageFont

GPIO.setwarnings(False)

#OLED
oled = sh1106(i2c(port=1, address=0x3C))
#großer ziffer (Standard-Pi-Font 64 px)
big_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)

def show(d):
    with canvas(oled) as draw:
        #center die ziffer mittig
        draw.text((40, 0), str(d), font=big_font, fill="white")

digit = 0
dirty = True
show(digit)

#Buttons
btn_up   = Button(17, pull_up=True, bounce_time=0.05)
btn_down = Button(27, pull_up=True, bounce_time=0.05)

def inc():
    global digit, dirty
    digit = (digit + 1) % 10
    dirty = True
    show(digit)

def dec():
    global digit, dirty
    digit = (digit - 1) % 10
    dirty = True
    show(digit)

btn_up.when_pressed   = inc
btn_down.when_pressed = dec

#RC522 Reader
writer = SimpleMFRC522()           

#print("Tag dauerhaft auflegen: Zahl mit Buttons ändern")

try:
    while True:
        if dirty:
            try:
                writer.write(str(digit))
                print(f"Geschrieben: {digit}")
                dirty = False
            except IndexError:     # Tag verrutscht
                time.sleep(0.1)
                continue
        time.sleep(0.05)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

