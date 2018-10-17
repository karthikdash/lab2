import time
import sys
import pygame
import os
import RPi.GPIO as GPIO
from pygame.locals import *

#os.system("sudo rmmod stmpe_ts")
#os.system("sudo modprobe stmpe_ts")
os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') 
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...


GPIO.setup(13, GPIO.OUT)
p1=GPIO.PWM(13,50)
dc1 = 2.2
p1.start(0)


GPIO.setup(19, GPIO.OUT)
p2=GPIO.PWM(19,50)
dc2 = 2.2
p2.start(0)


# pygame initial
pygame.init()

# Set basic parameters 
#pygame.mouse.set_visible(True)
size  = width, height = 320, 240
screen= pygame.display.set_mode((320, 240))
black = 0, 0, 0
WHITE = (255, 255, 255)
red   = 255,0,0

left_clkwise = 0
left_cc      = 0
left_stop    = 0
right_clkwise= 0
right_cc     = 0
right_stop   = 0

my_buttonfont  = pygame.font.Font(None, 30)
my_displayfont = pygame.font.Font(None, 20)
my_buttons = { 'start':(30,210), 'quit':(290, 210)}
my_display1= { 'Left History':(60,50)}
my_display2= { 'Right History':(260,50)}

flag       = False
start      = False
p1_state   = 0
p2_state   = 0
timer      = 0
clk        = time.time()
remain_t   = 0
p_remain_t = 1
stage      = 0

lflag = False
rflag = False
lresult1 = 'stop'
lresult2 = 'stop'
lresult3 = 'stop'
rresult1 = 'stop'
rresult2 = 'stop'
rresult3 = 'stop'
rstate = 'Clock'
lstate = 'Clock'
trstate = 'Clock'
tlstate = 'Clock'

while 1:
    time.sleep(0.1)
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x, y = pos
            if x >= 0 and x <= 60 and y >= 180 and y <= 240:
                time.sleep(0.2)
                left_clkwise=0
                left_cc=0
                left_stop=0
                right_clkwise=0
                right_cc=0
                right_stop=0
                flag=False
                start=True
                
            if flag == False:
                if ((x-160)*(x-160)+(y-120)*(y-120)) < 1600:
                    flag = True
                    p1.ChangeDutyCycle(0)
                    p2.ChangeDutyCycle(0)
                    p_remain_time = remain_t
            elif flag == True:
                if ((x-160)*(x-160)+(y-120)*(y-120)) < 1600:
                    flag = False
                    if p1_state==0:
                        p1.ChangeDutyCycle(0)
                    elif p1_state==1:
                        p1.ChangeDutyCycle(1.7)
                    elif p1_state==2:
                        p1.ChangeDutyCycle(2.7)
                    if p2_state==0:
                        p2.ChangeDutyCycle(0)
                    elif p2_state==1:
                        p2.ChangeDutyCycle(1.7)
                    elif p2_state==2:
                        p2.ChangeDutyCycle(2.7)
                    clk = time.time()    
            if x >= 260 and x <= 320 and y >= 180 and y <= 240:
                p1.stop
                p2.stop
                GPIO.cleanup()
                sys.exit()

    screen.fill(black)

    # motor contorl            
    if flag == False:
        remain_t = p_remain_t - (time.time()-clk)
        pygame.draw.circle(screen,red,(160,120),40)
        text_surface = my_buttonfont.render('stop', True, WHITE)
        rect = text_surface.get_rect(center=(160,120))
        screen.blit(text_surface, rect)
        if start == True:        
            # half speed
            if ( stage == 0 ) and ( remain_t <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(2.7)
                p1_state = 2
                tlstate = 'Counter'
                lstate = 'Counter'
                p2.ChangeDutyCycle(1.7)
                p2_state = 1
                trstate = 'Clock'
                rstate = 'Clock'
                time.sleep(3)
                stage = 1
                clk = time.time()
                p_remain_t = 1

            # stop
            elif ( stage == 1 ) and ( remain_t <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(0)
                p1_state = 0
                tlstate = 'Stop'
                lstate = 'Stop'
                p2.ChangeDutyCycle(0)
                p2_state = 0
                trstate = 'Stop'
                rstate = 'Stop'
                stage  = 2
                clk  = time.time()
                p_remain_t = 1
                
            # change duty cycle, half speed
            elif ( stage == 2 ) and ( remain_t <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(1.7)
                p1_state      = 1
                tlstate = 'Clock'
                lstate = 'Clock'
                p2.ChangeDutyCycle(2.7)
                p2_state      = 2
                trstate = 'Counter'
                rstate = 'Counter'
                stage         = 3
                time.sleep(3)
                clk           = time.time()
                p_remain_t    = 1
            
            #left
            elif ( stage == 3 ) and ( remain_t <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(1.7)
                p1_state      = 1
                tlstate = 'Clock'
                lstate = 'Clock'
                p2.ChangeDutyCycle(1.7)
                p2_state      = 1
                trstate = 'Clock'
                rstate = 'Clock'
                stage         = 4
                clk           = time.time()
                p_remain_t    = 1
                
            # stop
            elif ( stage == 4 ) and ( remain_t <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(0)
                p1_state      = 0
                tlstate = 'Stop'
                lstate = 'Stop'
                p2.ChangeDutyCycle(0)
                p2_state      = 0
                trstate = 'Stop'
                rstate = 'Stop'
                stage         = 5
                clk           = time.time()
                p_remain_t    = 1
                
            #right
            elif ( stage == 5 ) and ( remain_t <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(2.7)
                p1_state      = 2
                tlstate = 'Counter'
                lstate = 'Counter'
                p2.ChangeDutyCycle(2.7)
                p2_state      = 2
                trstate = 'Counter'
                rstate = 'Counter'
                stage         = 6
                clk           = time.time()
                p_remain_t    = 1
               
            # stop
            elif ( stage == 6 ) and ( remain_t <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(0)    
                p1_state      = 0
                tlstate = 'Stop'
                lstate = 'Stop'
                p2.ChangeDutyCycle(0)
                p2_state      = 0
                stage         = 0
                trstate = 'Stop'
                rstate = 'Stop'
                clk           = time.time()
                p_remain_t    = 1
  
    if lflag == True:
        lresult3 = lresult2
        lresult2 = lresult1
        lresult1 = lstate 
        lflag = False
    
    if rflag == True:
        rresult3 = rresult2
        rresult2 = rresult1
        rresult1 = rstate
        rflag = False

    for my_text, text_pos in my_buttons.items():
        text_surface = my_buttonfont.render(my_text, True, WHITE)
        rect = text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)
        
    text_surface = my_displayfont.render('Left History', True, WHITE)
    rect = text_surface.get_rect(center=(60,50))
    screen.blit(text_surface, rect)
    text_surface = my_displayfont.render('Right History', True, WHITE)
    rect = text_surface.get_rect(center=(270,50))
    screen.blit(text_surface, rect)
    
    text_surface = my_displayfont.render(lresult1, True, WHITE)
    rect = text_surface.get_rect(center=(60,90))
    screen.blit(text_surface, rect)    
    text_surface = my_displayfont.render(lresult2, True, WHITE)
    rect = text_surface.get_rect(center=(60,130))
    screen.blit(text_surface, rect)    
    text_surface = my_displayfont.render(lresult3, True, WHITE)
    rect = text_surface.get_rect(center=(60,170))
    screen.blit(text_surface, rect)    
    text_surface = my_displayfont.render(rresult1, True, WHITE)
    rect = text_surface.get_rect(center=(270,90))
    screen.blit(text_surface, rect)    
    text_surface = my_displayfont.render(rresult2, True, WHITE)
    rect = text_surface.get_rect(center=(270,130))
    screen.blit(text_surface, rect)    
    text_surface = my_displayfont.render(rresult3, True, WHITE)
    rect = text_surface.get_rect(center=(270,170))
    screen.blit(text_surface, rect)    
    
    pygame.display.flip()


    
p1.stop
p2.stop
GPIO.cleanup()
sys.exit()
