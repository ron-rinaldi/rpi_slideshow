#!/usr/bin/python  
# Simple script for shutting down the raspberry Pi at the press of a button.  
# by Inderpreet Singh  
#
# Script copied from:
# https://www.element14.com/community/docs/DOC-78055/l/adding-a-shutdown-button-to-the-raspberry-pi-b

#
# Connect a normally open switch to GPIO18 and Ground of the pi.
# Note that GPIO18 corresponds to header pin number 12 on 
# the header pin arrangement shown below:
# 
#   2  4  6  8  10  12  14  16  18  20  22  24  26  28 ...
#   1  3  5  7   9  11  13  15  17  19  21  23  25  27 ...
#
# Header pin 14 is a ground pin. 
# Therefore, to activate this script, you must short the 
# header pins number 12 and 14 above.
#  
import RPi.GPIO as GPIO  
import time  
import os  
 
# Use the Broadcom SOC Pin numbers  
# Setup the Pin with Internal pullups enabled and PIN in reading mode.  
GPIO.setmode(GPIO.BCM)  
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)  
 
# Our function on what to do when the button is pressed  
def shutdown(channel):  
    os.system("sudo shutdown -h now")  
 
# Add our function to execute when the button pressed event happens  
GPIO.add_event_detect(18, GPIO.FALLING, 
                      callback = shutdown, bouncetime = 2000)  
 
# Now wait!  
while 1:  
    time.sleep(1) 
 
