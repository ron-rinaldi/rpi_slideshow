# rpi_slideshow
Auto-booting slideshow for Raspberry Pi showing both still images and videos.

- Finds all images and videos, recursive within a specified directory tree.
- Image and video file extensions are configurable. (e.g. find mp4, but not m4v)
- Uses omxplayer for videos, pygame for still images.
- Repeats continuously.  Can be stopped by keypress if keyboard is plugged in.
- Uses systemd to auto-start at boot.
- Can be shutdown using a switch connected to GPIO pins (see watchdog.py)
- Can be shutdown remotely using ssh, then "sudo systemctl stop slideshow"

