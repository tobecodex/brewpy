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
  temp, rh = stdout.split(',')
  heater_on = (int(temp) <= 15)
  GPIO.output(__PIN_HEATER, not heater_on)
  print heater_on

  # Log what happened
  data = [ datetime.datetime.now().isoformat(), temp, rh, str(int(heater_on)) ]
  print ",".join(data)

if __name__ == "__main__":
  run()
