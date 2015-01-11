import RPi.GPIO as GPIO

__PIN_HEATER=25

GPIO.setmode(GPIO.BCM)
GPIO.setup(__PIN_HEATER, GPIO.OUT)

# False set the heater on
GPIO.output(__PIN_HEATER, False)
