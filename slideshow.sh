#!/bin/bash
#
# Slideshow.
#
# Time so that xterm is up and flash 
# drives are mounted
# Successful values: 
#    sleep 8   on a Pi-3
#    sleep 32  on a Pi-zero
#sleep 32

# Make sure screensaver is off
xset s off
xset -dpms
xset s noblank

# Activate the slideshow
cd /home/pi/rpi_slideshow/
python slideshow.py ./slideshow.ini
