import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)




pin1 = GPIO.PWM(13, 50)
x = 2
dc = x/ (20 + x)
print x
pin1.start(dc)
raw_input("Press Enter")
while False:
    dc = x/ (20 + x)
    print x
    pin1.start(dc)
    # raw_input("Press Enter")
    x -= 0.01
    time.sleep(0.1)


pin1.stop()

GPIO.cleanup()
