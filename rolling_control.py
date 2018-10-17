import pygame
from  pygame.locals import*
import os
from pygame import*
import RPi.GPIO as GPIO
import time
import signal
import sys



os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
pygame.init()
pygame.mouse.set_visible(False)

# Color Definitions
RED = (255, 0, 0)
GREEN = (0, 255, 0)

GPIO.setmode(GPIO.BCM)   

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)   
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)   

# Set GPIO 12 & 18 as output
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

stop1 = True
stop2 = True
# Set duty cycle
dc1 = 2.2
dc2 = 2.2
# Set channel & frequency
p1 = GPIO.PWM(19,50)
p2 = GPIO.PWM(13,50)

rStop = 0
rClk = 0
rCClk = 0

lStop = 0
lClk = 0
lCClk = 0

def handler(signum, frame):
    print "exit"
    pygame.quit()
    sys.exit(0)

signal.signal(signal.SIGTSTP, handler)
# PyGame
WHITE = 255, 255, 255
BLACK = 0,0,0
screen = pygame.display.set_mode((320, 240))
my_font = pygame.font.Font(None, 15)

my_buttons = { 'Left History': [(40,60), 0], 
			   'L_Stop': [(40, 70), lStop],
			   'L_Clockwise': [(40, 80), lClk],
			   'L_CClockwise': [(40, 90), lCClk],
			   'Right History': [(280,60), 0], 
			   'R_Stop': [(280, 70), rStop],
			   'R_Clockwise': [(280, 80), rClk],
			   'R_CClockwise': [(280, 90), rCClk],
			   'Panic': [(160, 120), 0],
                           'Exit' : [(160, 220), 0]}
print len(my_buttons)

pause = False

while True:
	
	screen.fill(BLACK) # Erase the Work space
	for my_text, text_pos in my_buttons.items():
		if my_text == "Panic":
			if not pause:
				text_surface = my_font.render("Panic", True, WHITE)
				pygame.draw.circle(screen, RED, text_pos[0], 30)
			else:
				text_surface = my_font.render("Resume", True, WHITE)
				pygame.draw.circle(screen, GREEN, text_pos[0], 30)
		else:
			text_surface = my_font.render(my_text + " " + str(text_pos[1]), True, WHITE)
		rect = text_surface.get_rect(center=text_pos[0])
		screen.blit(text_surface, rect)
	pygame.display.flip()
	
	for event in pygame.event.get():
		if(event.type is MOUSEBUTTONDOWN):
			pos = pygame.mouse.get_pos()
		elif(event.type is MOUSEBUTTONUP):
			pos = pygame.mouse.get_pos()
			x,y = pos
			if y > 100 and y < 140:
				if x > 140 and x < 180:
					if pause == False:
						stop2 = False
						stop1 = False
						pause = True
					else:
						pause = False
						stop2 = True
						stop1 = True
                        else:
                                if x > 140 and x < 180:
                                    pygame.quit()
                                    sys.exit(0)
                                    GPIO.cleanup()

	
	
	
	if stop1:
		p1.start(dc1)
	else:
		p1.ChangeDutyCycle(0)
	if stop2:
		p2.start(dc2)
	else:
		p2.ChangeDutyCycle(0)
	time.sleep(0.1)
	if(not GPIO.input(17)):
		time.sleep(0.2)
		if dc1>2.2:
			dc1 = 1.2
			p1.ChangeDutyCycle(dc1)
			my_buttons['R_Clockwise'][1] += 1
		else:
			dc1 = 3
			p1.ChangeDutyCycle(dc1)
			my_buttons['R_CClockwise'][1] += 1

	if(not GPIO.input(22)):
		time.sleep(0.2)
		if dc2>2.2:
			dc2 = 1.2
			p2.ChangeDutyCycle(dc2)
			my_buttons['L_Clockwise'][1] += 1
		else:
			dc2 = 3
			p2.ChangeDutyCycle(dc2)
			my_buttons['L_CClockwise'][1] += 1


	if(not GPIO.input(23)):
		time.sleep(0.2)
		if(stop1 == True):
			stop1 = False
			my_buttons['R_Stop'][1] += 1
		else:
			stop1 = True

	if(not GPIO.input(27)):
		time.sleep(0.2)
		if(stop2 == True):
			stop2 = False
			my_buttons['L_Stop'][1] += 1
		else:
			stop2 = True
pygame.quit()





