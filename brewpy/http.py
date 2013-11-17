import RPi.GPIO as GPIO

from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)

@app.route('/')
def root():
  try:
    return redirect("/graph")
  except Exception as e:
    print "Exception", e
    return e

@app.route('/graph')
def graph(name=None):
  series = file("/var/log/dht11.log").read().replace("\n", "\\n")
  return render_template('graph.html', series=series)

def init():
  # use P1 header pin numbering convention
  GPIO.setmode(GPIO.BOARD)
 
if __name__ == '__main__':
  init();
  app.debug = True
  app.run(host="0.0.0.0")
