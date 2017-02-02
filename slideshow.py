#!/usr/bin/python
# Notes:
# Difficult to get interruptible sleep during pygame.
# So, we use the pygame event queue to test for keyboard
# action.  This is useful to stop slideshow for debug.
# In production, there will not be a keyboard, only a
# watchdog switch.
#
#
import os
import time
import sys
import subprocess

import ConfigParser
import pygame

def isnumber( value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def sleep( delay):
    time.sleep(delay)
    # Interrupt sleep by any key press.
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            close_down()


def readconfig( config_path):
    # Load the configuration.
    parser = ConfigParser.SafeConfigParser()
    if len( parser.read( config_path)) == 0:
        raise RuntimeError('Cant open config file: {0}'.format( config_path))
    
    # Create config object to return
    config = {}
    config['filepath'] = parser.get('slideshow','filepath')
    delay    = parser.get('slideshow','delay')
    if isnumber(delay): config['delay'] = float(delay)
    else:               config['delay'] = 5.0

    all_extensions = []

    # OMXPlayer extensions
    omx_extensions = []
    extensions = parser.get('slideshow','omx_extensions')
    extensions = extensions.split(',')
    for ext in extensions:
       omx_extensions.append( ext.strip()) 
       all_extensions.append( ext.strip())
    config['omx_extensions'] = omx_extensions

    # Image extensions
    img_extensions = []
    extensions = parser.get('slideshow','img_extensions')
    extensions = extensions.split(',')
    for ext in extensions:
       img_extensions.append( ext.strip()) 
       all_extensions.append( ext.strip())
    config['img_extensions'] = img_extensions

    config['all_extensions'] = all_extensions

    return config


#def printfiles( dirlist):
#    for filename in dirlist:
#        print filename


def getfilesindir( directory, extensions, filelist):
    dir = directory[0]
    filenames = directory[2]
    for filename in filenames:
        for extension in extensions:
            if filename.endswith( extension):
                filelist.append( dir + '/' + filename)


def getfiles( config):
    filelist = []
    extensions = config['all_extensions']
    tree = os.walk( config['filepath'])
    for directory in tree:
        getfilesindir( directory, extensions, filelist)
    return filelist


def play_omx( filename, screen):
    # Play a movie using oxmplayer.  
    #print "OMX: ", filename
    args = ['omxplayer']
    args.append( '--blank')
    args.append( filename)

    #print args
    # Use .call, as it will wait for process to finish
    subprocess.call( args, stdin=None, stdout=None, stderr=None, shell=False)
    blankscreen( screen)
    # Sleep here is to catch key press.
    sleep(0.05)


def play_pygame( filename, config, screen):
    # Display an image file using pygame. 
    print "PYGAME: ", filename
    info = pygame.display.Info()
    displaysize = (info.current_w, info.current_h) 
    img = pygame.image.load( filename)
    imgsize = img.get_size()
    xscale = float(displaysize[0]) / float(imgsize[0])
    yscale = float(displaysize[1]) / float(imgsize[1])
    scale = xscale
    if yscale < xscale: scale = yscale
    newsize = ( int(float(imgsize[0]*scale)), 
                int(float(imgsize[1]*scale)))
    xoffset = 0
    yoffset = 0
    if newsize[0] < displaysize[0]:
        xoffset = (displaysize[0] - newsize[0]) / 2
    if newsize[1] < displaysize[1]:
        yoffset = (displaysize[1] - newsize[1]) / 2

    img = pygame.transform.smoothscale( img, newsize)
    screen.blit( img, (xoffset, yoffset))
    pygame.display.flip()

    sleep( config['delay'])
    blankscreen( screen)


def play( filename, config, screen):
    # Play any type of file (image or movie)
    # Determine program to use
    for ext in config['omx_extensions']:
        if filename.endswith( ext):
            play_omx( filename, screen)
            return

    for ext in config['img_extensions']:
        if filename.endswith( ext):
            play_pygame( filename, config, screen)
            return
    

def pygameinit():
    pygame.display.init()
    info = pygame.display.Info()
    size = (info.current_w, info.current_h) 
    screen = pygame.display.set_mode( size, pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)
    return screen


def blankscreen( screen):
    screen.fill( (0,0,0)) 
    pygame.display.update()


def close_down():
    #print 'close_down'
    sys.exit(0)

# ----------------------------------------------------------------------------
# Begin main program

if len(sys.argv) <= 1:
    print "No config file specified"
    close_down()

else:
    config_path = sys.argv[1]
    config = readconfig( config_path)
    #print config

    filelist = getfiles( config)
    filelist.sort()

    if len(filelist) == 0:
        print 'No files found at:', config['filepath']
        close_down()

    screen = pygameinit()

    while True:
        for filename in filelist:
            play( filename, config, screen)

