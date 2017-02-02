#!/bin/bash
#
# Slideshow.
#
# Time so that xterm is up and flash 
# drives are mounted
sleep 8

# Make sure screensaver is off
xset s off
xset -dpms
xset s noblank

# Activate the slideshow
cd /home/pi/rpi_slideshow/
python slideshow.py ./slideshow.ini
