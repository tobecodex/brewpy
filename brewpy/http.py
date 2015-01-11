from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)

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
    log_data = file("/var/log/brewpy.log").readlines()
  except IOError:
    log_data = []

  data = map(
    lambda x : x.strip().split(","), log_data
  )

  # Extract temps from log lines
  temps = map(lambda x : float(x[1]) if len(x) > 0 else "", data)

  # Read target temp
  target_temp = int(open("target_temp").read())

  # Stitch time,heater,temp back together
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
