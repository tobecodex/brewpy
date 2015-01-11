import RPi.GPIO as GPIO

__PIN_HEATER=23

GPIO.setmode(GPIO.BCM)
GPIO.setup(__PIN_HEATER, GPIO.OUT)

# True sets the heater off
GPIO.output(__PIN_HEATER, True)
