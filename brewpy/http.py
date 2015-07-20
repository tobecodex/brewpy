import time
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

  current_brew = open("current_brew", "r").read()
  if not current_brew:
    return redirect("new_brew")

  try:
    log_data = file("temp.log").readlines()
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

  return render_template('graph.html', name=current_brew, series=series.replace("\n", "\\n"), target_temp=target_temp)

@app.route('/new_brew', methods=['GET', 'POST'])
def new_brew():
  if request.method == "POST":
    name = request.form.get("name")
    og = request.form.get("og")
    notes = request.form.get("notes")
    _now = time.strftime("%d-%m-%Y@%H:%M")
    fname = "brews/%s-%s.txt" % (name, _now)
    f = open(fname, "w")
    f.write("Name: %s\n" % name)
    f.write("O.G: %s\n" % og)
    f.write("Notes:%s\n" % notes)
    f.close()
    open("current_brew", "w").write(fname)

    return redirect("/graph")
  return render_template('new_brew.html')

def init():
  pass
 
if __name__ == '__main__':
  init();
  app.debug = True
  app.run(host="0.0.0.0")
