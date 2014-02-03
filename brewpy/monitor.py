import time
import datetime
import subprocess
import RPi.GPIO as GPIO
from operator import itemgetter

__PIN_HEATER = 23
__PIN_THERMISTOR = 23

def read_thermistor():
  curve = []
  values = open("curve.csv").readlines()
  for value in values:
    t, r = value.split(",")
    curve.append((int(r.strip()), int(t)))
  curve.sort(key = itemgetter(0))

  stdout = subprocess.check_output(
    ["/usr/local/sbin/analog", __PIN_THERMISTOR]
  ).strip()
  r = int(stdout)

  i = 0
  while i < len(curve) and r > curve[i][0]:
    i += 1

  if i == 0 or i >= len(curve):
    return None
  
  d = curve[i][0] - r
  dT = curve[i][0] - curve[i - 1][0]
  t = curve[i][1] + (1 * (d / float(dT)))
  return t

def run():
  # Setup
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(__PIN_HEATER, GPIO.OUT)

  # Read from dht-11, operate heater
  stdout = subprocess.check_output(["/usr/local/sbin/dht-11"]).strip()
  temp, rh = stdout.split(',')
  heater_on = (int(temp) < 21)
  GPIO.output(__PIN_HEATER, not heater_on)

  # Log what happened
  data = [ datetime.datetime.now().isoformat(), temp + "DegC", rh + "%", str(int(heater_on)) ]
  print ",".join(data)

if __name__ == "__main__":
  run()
