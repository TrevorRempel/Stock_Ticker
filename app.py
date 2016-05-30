from flask import Flask, render_template, request, redirect
from process import make_html
from plot import produce_plot
from bokeh.embed import components
from bokeh.plotting import figure
import json


app = Flask(__name__)
app.OPTIONS = [r"Open", r"Adj_Open", r"Close", r"Adj_Close"]
app.NAMES = [s.replace("_",". ") for s in app.OPTIONS]
app.div = []
app.script = ""


@app.route('/')
def main():
  return redirect('/index')

@app.route('/clear', methods = ['GET'])
def clear():
	return redirect('/index')
	#return render_template('index.html',op = app.OPTIONS, names = app.NAMES)

@app.route('/index', methods = ['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html', op = app.OPTIONS, names = app.NAMES)
	if request.method == 'POST':
		options = [val.replace("_",". ") for val in app.OPTIONS if request.form.get(val) is not None]
		ticker = request.form.get("ticker")
		
		notValid, fig = make_html(ticker, options)
		app.script, app.div = components(fig)
		#output_file("test.html")

		
		'''
		TOOLS = "resize,crosshair,box_zoom,reset,box_select,save"
		output_file("test.html")
		fig=figure(title="Sensor data", tools = TOOLS)
		fig.line([1,2,3,4],[2,4,6,8])
		#global script
		#global div
		script, div=components(fig)
		'''

		if len(notValid) > 0:
			notValidstr = 'These are not valid tickers: ' + ', '.join(notValid)
		else:
			notValidstr = ""

		return render_template('plot.html', op = app.OPTIONS, names = app.NAMES,\
			script = app.script, div = json.dumps(app.div), notValid = notValidstr)



if __name__ == '__main__':
  #app.run(debug = True, port = 33507)
  app.run(port=33507)
