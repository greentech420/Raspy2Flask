from flask import Flask
app=Flask(__name__)

@app.route('/')
def samplePage1():
	name="Hello Flask"
	return name

@app.route('/good/')
def samplePage2():
	name="Good Flask"
	return name


if __name__=='__main__':
	app.run("10.0.3.32",debug=True,port=8000)