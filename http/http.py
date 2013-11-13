import RPi.GPIO as GPIO

from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)

@app.route('/')
def root():
  try:
    return redirect(url_for("static", filename="index.html"))
    return render_template(url_for("static", filename="index.html"))
  except Exception as e:
    print "Exception", e
    return e

@app.route('/graph')
def graph(name=None):
  series = ""
  lines = file("/var/log/dht11.log").readlines()
  for line in lines:
    try:
      d,tm,t,h = line.split()
    except:
      continue
    tm = d + " " + tm
    series += tm + "," + t.split(":")[1] + "," + h.split(":")[1] + "\\n"
  return render_template('graph.html', series=series)

def init():
  # use P1 header pin numbering convention
  GPIO.setmode(GPIO.BOARD)
 
if __name__ == '__main__':
  init();
  app.debug = True
  app.run(host="0.0.0.0")
