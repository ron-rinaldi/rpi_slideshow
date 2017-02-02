#!/bin/sh
#
# Setup slideshow. 
#
# This script assumes a standard Jessie distro.
#
 
# Install necessary packages
sudo apt-get -y install x11-xserver-utils

# Disable screen saver
DFILE=~/.xinitrc
echo "xset s off" > $DFILE
echo "xset -dpms" >> $DFILE
echo "xset s noblank" >> $DFILE

echo ""
echo "     N-O-T-I-C-E"
echo ""
echo "It is a good idea to add this line to /boot/config.txt:"
echo "    gpu_mem=128"
echo "Otherwise, omxplayer may run out of memory and fail."
echo ""
echo ""
