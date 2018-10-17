import time
import sys
import pygame
import os
import RPi.GPIO as GPIO
from pygame.locals import *

os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') 
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

GPIO.setmode(GPIO.BCM)   


GPIO.setup(19, GPIO.OUT)
p1=GPIO.PWM(19,50)
dc1 = 2.2
p1.start(0)


GPIO.setup(13, GPIO.OUT)
p2=GPIO.PWM(13,50)
dc2 = 2.2
p2.start(0)



pygame.init()
pygame.mouse.set_visible(True)
size  = width, height = 320, 240
screen= pygame.display.set_mode((320, 240))
black = 0, 0, 0
WHITE = (255, 255, 255)
red   = 255,0,0
green = 0,255,0

l_clockwise = 0
l_counterclockwise = 0
l_stop    = 0
r_clockwise= 0
r_counterclockwise = 0
r_stop = 0

my_buttonfont  = pygame.font.Font(None, 30)
my_displayfont = pygame.font.Font(None, 20)
my_buttons = { 'start':(30,210),'quit':(290, 210)}
my_display1= { 'Left History':(60,50)}
my_display2= { 'Right History':(260,50)}

flag = False
start  = False
p1_state = 0
p2_state = 0
timer  = 0
clk = time.time()
time_remaining  = 0
p_time_remaining = 1
current_status  = 0

lflag = False
rflag = False
leftresult1 = 'stop'
leftresult2 = 'stop'
leftresult3 = 'stop'
rresult1 = 'stop'
rightresult2 = 'stop'
rightresult3 = 'stop'
right_state = 'clockwise'
left_state = 'clockwise'
tright_state = 'clockwise'
tleft_state = 'clockwise'

while 1:
    time.sleep(0.1)
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x, y = pos
            if x >= 0 and x <= 60 and y >= 180 and y <= 240:
                time.sleep(0.2)
                l_clockwise=0
                l_counterclockwise=0
                l_stop=0
                r_clockwise=0
                r_counterclockwise=0
                r_stop=0
                flag=False
                start=True
                
            if flag == False:
                if ((x-160)*(x-160)+(y-120)*(y-120)) < 1600:
                    flag = True
                    p1.ChangeDutyCycle(0)
                    p2.ChangeDutyCycle(0)
                    p_time_remaining = time_remaining
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

        
    if flag == False:
        time_remaining = p_time_remaining - (time.time()-clk)
        pygame.draw.circle(screen,red,(160,120),40)
        text_surface = my_buttonfont.render('stop', True, WHITE)
        rect = text_surface.get_rect(center=(160,120))
        screen.blit(text_surface, rect)
        if start == True:        
            # half speed
            if ( current_status == 0 ) and ( time_remaining <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(2.7)
                p1_state = 2
                tleft_state = 'counterclockwise'
                left_state = 'counterclockwise'
                p2.ChangeDutyCycle(1.7)
                p2_state = 1
                tright_state = 'clockwise'
                right_state = 'clockwise'
                current_status = 1
                clk = time.time()
                p_time_remaining = 1


            elif ( current_status == 1 ) and ( time_remaining <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(0)
                p1_state  = 0
                tleft_state = 'Stop'
                left_state = 'Stop'
                p2.ChangeDutyCycle(0)
                p2_state    = 0
                tright_state = 'Stop'
                right_state = 'Stop'
                current_status         = 2
                clk  = time.time()
                p_time_remaining    = 1
                

            elif ( current_status == 2 ) and ( time_remaining <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(1.7)
                p1_state  = 1
                tleft_state = 'clockwise'
                left_state = 'clockwise'
                p2.ChangeDutyCycle(2.7)
                p2_state   = 2
                tright_state = 'counterclockwise'
                right_state = 'counterclockwise'
                current_status   = 3
                clk = time.time()
                p_time_remaining    = 1
            

            elif ( current_status == 3 ) and ( time_remaining <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(1.7)
                p1_state  = 1
                tleft_state = 'clockwise'
                left_state = 'clockwise'
                p2.ChangeDutyCycle(1.7)
                p2_state  = 1
                tright_state = 'clockwise'
                right_state = 'clockwise'
                current_status = 4
                clk = time.time()
                p_time_remaining = 1
                

            elif ( current_status == 4 ) and ( time_remaining <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(0)
                p1_state = 0
                tleft_state = 'Stop'
                left_state = 'Stop'
                p2.ChangeDutyCycle(0)
                p2_state = 0
                tright_state = 'Stop'
                right_state = 'Stop'
                current_status         = 5
                clk = time.time()
                p_time_remaining    = 1
                

            elif ( current_status == 5 ) and ( time_remaining <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(2.7)
                p1_state   = 2
                tleft_state = 'counterclockwise'
                left_state = 'counterclockwise'
                p2.ChangeDutyCycle(2.7)
                p2_state   = 2
                tright_state = 'counterclockwise'
                right_state = 'counterclockwise'
                current_status = 6
                clk = time.time()
                p_time_remaining = 1
               

            elif ( current_status == 6 ) and ( time_remaining <= 0 ):
                rflag = True
                lflag = True
                p1.ChangeDutyCycle(0)    
                p1_state = 0
                tleft_state = 'Stop'
                left_state = 'Stop'
                p2.ChangeDutyCycle(0)
                p2_state  = 0
                current_status = 0
                tright_state = 'Stop'
                right_state = 'Stop'
                clk = time.time()
                p_time_remaining = 1

    else:
        pygame.draw.circle(screen,green,(160,120),40)
        text_surface = my_buttonfont.render('resume', True, WHITE)
        rect = text_surface.get_rect(center=(160,120))
        screen.blit(text_surface, rect)
      
    if lflag == True:
        leftresult3 = leftresult2
        leftresult2 = leftresult1
        leftresult1 = left_state 
        lflag = False
    
    if rflag == True:
        rightresult3 = rightresult2
        rightresult2 = rresult1
        rresult1 = right_state
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
    
    text_surface = my_displayfont.render(leftresult1, True, WHITE)
    rect = text_surface.get_rect(center=(60,90))
    screen.blit(text_surface, rect)    
    text_surface = my_displayfont.render(leftresult2, True, WHITE)
    rect = text_surface.get_rect(center=(60,130))
    screen.blit(text_surface, rect)    
    text_surface = my_displayfont.render(leftresult3, True, WHITE)
    rect = text_surface.get_rect(center=(60,170))
    screen.blit(text_surface, rect)    
    text_surface = my_displayfont.render(rresult1, True, WHITE)
    rect = text_surface.get_rect(center=(270,90))
    screen.blit(text_surface, rect)    
    text_surface = my_displayfont.render(rightresult2, True, WHITE)
    rect = text_surface.get_rect(center=(270,130))
    screen.blit(text_surface, rect)    
    text_surface = my_displayfont.render(rightresult3, True, WHITE)
    rect = text_surface.get_rect(center=(270,170))
    screen.blit(text_surface, rect)    
    
    pygame.display.flip()


    
p1.stop
p2.stop
GPIO.cleanup()
sys.exit()