import time
import datetime
import subprocess
import RPi.GPIO as GPIO
from operator import itemgetter

__PIN_HEATER = 23
__PIN_THERMISTOR = 24

def read_resistance():
  stdout = subprocess.check_output(["/usr/local/sbin/analog"]).strip()
  return int(stdout)

def read_thermistor():

  R = read_resistance()

  curve = []
  values = open("curve.csv").readlines()
  for value in values:
    f, c, r = value.split()
    curve.append((int(r.strip()), float(c)))
  curve.sort(key = itemgetter(0))

  # Now use the thermistor curve
  # to work out temp.

  i = 0
  for point in curve:
    if R < point[0]:
      break
    i += 1

  # lerp is good enough
 
  r0 = curve[i - 1][0]
  r1 = curve[i][0]
  mu = (R - r0) / float(r1 - r0)
  
  t0 = curve[i - 1][1]
  t1 = curve[i][1]
  
  t = round(t0 + (mu * (t1 - t0)), 2)
  return t

def run():
  # Setup
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(__PIN_HEATER, GPIO.OUT)

  temp = read_thermistor()
  # print str(temp) + " degC"

  heater_on = (int(temp) > 21)
  GPIO.output(__PIN_HEATER, not heater_on)

  # Log what happened
  data = [ 
    datetime.datetime.now().isoformat(), 
    str(temp), 
    str(int(heater_on)) 
  ]
  print ",".join(data)

if __name__ == "__main__":
  run()
