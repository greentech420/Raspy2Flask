from flask import Flask, render_template
app=Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html',title="最初のページ")

@app.route('/next')
def next():
	return render_template('next.html',title="次のページ")




if __name__=='__main__':
	app.run("10.0.3.32",debug=True,port=8000)