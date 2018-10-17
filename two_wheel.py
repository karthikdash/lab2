
import RPi.GPIO as GPIO
import time

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


while True:
    if stop1:
        p1.start(dc1)
    else:
        p1.ChangeDutyCycle(0)
    if stop2:
        p2.start(dc2)
    else:
        p2.ChangeDutyCycle(0)
        
    if(not GPIO.input(17)):
        time.sleep(0.2)
        if dc1>2.2:
            dc1 = 1.2
            p1.ChangeDutyCycle(dc1)
        else:
            dc1 = 3
            p1.ChangeDutyCycle(dc1)
    
    if(not GPIO.input(22)):
        time.sleep(0.2)
        if dc2>2.2:
            dc2 = 1.2
            p2.ChangeDutyCycle(dc2)
        else:
            dc2 = 3
            p2.ChangeDutyCycle(dc2)
    
    if(not GPIO.input(23)):
        time.sleep(0.2)
        if(stop1 == True):
            stop1 = False
        else:
            stop1 = True

    if(not GPIO.input(27)):
        time.sleep(0.2)
        if(stop2 == True):
            stop2 = False
        else:
            stop2 = True





