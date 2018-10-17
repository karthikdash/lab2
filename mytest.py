import RPi.GPIO as GPIO
import time
import pygame # Import Library and initialize pygame
import math
from pygame.locals import *
import os
import sys

GPIO.setmode(GPIO.BCM)   

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # set up broadcom number 17 as input GPIO pin, as pull up network)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # set up broadcom number 22 as input GPIO pin, as pull up network)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # set up broadcom number 23 as input GPIO pin, as pull up network)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # set up broadcom number 27 as input GPIO pin, as pull up network)

# Set GPIO 12 & 18 as output
GPIO.setup(19, GPIO.OUT) 
GPIO.setup(13, GPIO.OUT)

pygame.init()

pygame.mouse.set_visible(True)
size = width, height = 320, 240


