from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)

try:
  import numpy
  numpy_installed = True
except ImportError:
  numpy_installed = False

def smooth(x,window_len=7,window='flat'):

    if not numpy_installed:
      return x

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
        w = eval('numpy.'+window+'(window_len)')

    y = numpy.convolve(w/w.sum(),s,mode='valid')
    return y[(window_len/2-1):-(window_len/2)]


@app.route('/')
def root():
  return redirect("/graph")

@app.route('/update_temp', methods=['POST'])
def update_temp():
  target_temp = request.form.get("target_temp")
  open("target_temp", "w").write(target_temp)
  return redirect("/graph")

@app.route('/graph')
def graph(name=None):

  try:
    analog_data = file("/var/log/analog.log").readlines()
  except IOError:
    analog_data = []

  data = map(
    lambda x : x.strip().split(","), analog_data
  )

  temps = smooth(map(lambda x : float(x[1]) if len(x) > 0 else "", data))

  # Read target temp
  target_temp = int(open("target_temp").read())

  series = "".join(
    map(
      lambda x : ",".join(x) + "\n", 
      [(T[0],str(t),T[2]) for T,t in zip(data,temps)]
    )
  )

  return render_template('graph.html', series=series.replace("\n", "\\n"), target_temp=target_temp)

def init():
  pass
 
if __name__ == '__main__':
  init();
  app.debug = True
  app.run(host="0.0.0.0")
