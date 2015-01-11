#!/usr/bin/env python

import time
import datetime
import subprocess
import RPi.GPIO as GPIO
from operator import itemgetter

__PIN_HEATER = 25
__DEVICE_ID = "000004f926e7"

def read_resistance():
  # Read the resistance on thermistor via C program
  stdout = subprocess.check_output(["/usr/local/sbin/analog"]).strip()
  return int(stdout)

def read_thermistor():

  # Do some maths to figure out what the temp
  # is for a given resistance for our thermistor

  R = read_resistance()

  curve = []
  # curve.csv contains values for our current 100k 
  # thermistor
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

def read_ds18b20():
  stdout = subprocess.check_output(["cat", "/sys/bus/w1/devices/28-"  + __DEVICE_ID + "/w1_slave"]).strip()
  temp = stdout.split("t=")[1]
  temp = temp[0:2] + "." + temp[2:]
  return float(temp)

def run():

  # Setup
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(__PIN_HEATER, GPIO.OUT)

  # Read target temp
  target_temp = int(open("target_temp").read())

  temp = read_ds18b20()

  _now = datetime.datetime.now().isoformat()
  # heater_on = int(_now[len(_now) - 11]) % 2 == 0
  heater_on = (int(temp) < target_temp)
  GPIO.output(__PIN_HEATER, not heater_on)

  # Log what happened
  data = [
    _now,
    str(temp), 
    str(int(heater_on)) 
  ]
  print ",".join(data)

if __name__ == "__main__":
  run()
