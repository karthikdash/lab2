import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

pin1 = GPIO.PWM(13,50)
dc = 2.2
pin1.start(dc)
# time.sleep(3)
print('Clockwise \n')
while dc > 0.5:
    print('Clockwise: Current dc value is: %f'%(dc))
    dc = dc - 0.2
    pin1.ChangeDutyCycle(dc)
    time.sleep(0.5)

dc = 2.2
pin1.start(dc)
# time.sleep(3)
while dc < 3.5:
    print('Anticlockwise: Current dc value is: %f'%(dc))
    dc = dc + 0.2
    pin1.ChangeDutyCycle(dc)
    time.sleep(0.5)

pin1.stop()
GPIO.cleanup()
