from bme280 import BME280
import datetime
from flask import Flask,render_template,request

app = Flask(__name__)

bme = BME280()

@app.route('/')
def samplePage():
	py_temp,py_humi,py_press = bme.readData()
	py_date = datetime.datetime.now().strftime('%Y/%M/%d %H:%M')

	return render_template('index.html',
							title='環境情報ページ',	#ページタイトル
							date=py_date,	#日付/時刻情報
							temp=py_temp,	#気温情報
							humi=py_humi,	#湿度情報
							press=py_press	#気圧情報

	)


if __name__=='__main__':
	app.run("10.0.3.32",debug=True,port=8000)
	

