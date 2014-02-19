import RPi.GPIO as GPIO

from flask import Flask, render_template, url_for, redirect
app = Flask(__name__)

import numpy
def smooth(x,window_len=7,window='flat'):
    x = numpy.array(x)

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len<3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s = numpy.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    if window == 'flat': #moving average
        w = numpy.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y = numpy.convolve(w/w.sum(),s,mode='valid')
    return y[(window_len/2-1):-(window_len/2)]


@app.route('/')
def root():
  try:
    return redirect("/graph")
  except Exception as e:
    print "Exception", e
    return e

@app.route('/graph')
def graph(name=None):

  data = map(
    lambda x : x.strip().split(","), 
    file("/var/log/analog.log").readlines()
  )
  temps = smooth(map(lambda x : float(x[1]) if len(x) > 0 else "", data))
  series = "".join(
    map(
      lambda x : ",".join(x) + "\n", 
      [(T[0],str(t),T[2]) for T,t in zip(data,temps)]
    )
  )

  return render_template('graph.html', series=series.replace("\n", "\\n"))

def init():
  # use P1 header pin numbering convention
  GPIO.setmode(GPIO.BOARD)
 
if __name__ == '__main__':
  init();
  app.debug = True
  app.run(host="0.0.0.0")
