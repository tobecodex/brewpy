import time
import datetime
import subprocess
import RPi.GPIO as GPIO

__PIN_HEATER = 23

def run():
  # Setup
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(__PIN_HEATER, GPIO.OUT)

  # Read from dht-11, operate heater
  stdout = subprocess.check_output(["dht-11"]).strip()
  temp = int(stdout.split()[0].split(":")[1])
  heater_on = (temp <= 15)
  GPIO.output(__PIN_HEATER, not heater_on)

  # Log what happened
  print datetime.datetime.now().isoformat(), stdout, heater_on

if __name__ == "__main__":
  run()
