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

def init():
  # use P1 header pin numbering convention
  GPIO.setmode(GPIO.BOARD)
 
if __name__ == '__main__':
  init();
  app.debug = True
  app.run(host="0.0.0.0")
