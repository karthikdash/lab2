import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
pin = GPIO.PWM(26, 50)
pin.start(7.5)
time.sleep(2)
pin.stop()
GPIO.cleanup()
