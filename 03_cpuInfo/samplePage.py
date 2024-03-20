import cpuInfo
from flask import Flask,render_template,request

app = Flask(__name__)
@app.route('/')
def samplePage():
	info=cpuInfo.cpuinfo()
	return render_template('index.html',				#呼び出すHTML
							title='RaspberryPi CPU情報', #ページタイトル
							date=info[0],   #日付/時刻
							temp=info[1],   #温度
							clock=info[2],  #クロック周波数
							volts=info[3],  #CPU電圧
							cpu_m=info[4],  #メモリ使用量(CPU)
							gpu_m=info[5] ) #メモリ使用量(GPU)


if __name__=='__main__':
	app.run("10.0.3.32",debug=True,port=8000)
	

