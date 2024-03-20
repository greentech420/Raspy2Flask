# -*- coding: utf-8 -*-
import subprocess
import time
from datetime import datetime
from types import DynamicClassAttribute

def main():
    while True:
        info = cpuinfo()

        # 結果表示
        #print("{}, temp:{}, clock:{}, volts:{}, cpu_m:{}, gpu_m:{}".format(date, temp, clock, volts, memory_cpu, memory_gpu))
        print("{}, temp:{}, clock:{}MHz, volts:{}, cpu_m:{}, gpu_m:{}".format(info[0],info[1],info[2],info[3],info[4],info[5]))
        time.sleep(1) # 1秒待つ

#CPU情報の取得（取得情報をリストで戻す）
def cpuinfo():
    info=[]

    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")          # 現在時刻
    temp       = run_shell_command("vcgencmd measure_temp")      # CPU温度
    clock      = run_shell_command("vcgencmd measure_clock arm") # CPU周波数
    volts      = run_shell_command("vcgencmd measure_volts")     # CPU電圧
    memory_cpu = run_shell_command("vcgencmd get_mem arm")       # CPUのメモリ使用量
    memory_gpu = run_shell_command("vcgencmd get_mem gpu")       # GPUのメモリ使用量
    clk=int(clock)/1000000
    info.append(date)
    info.append(temp)
    info.append(str(clk))
    info.append(volts)
    info.append(memory_cpu)
    info.append(memory_gpu)


    return info

# シェルコマンドを実行する関数
def run_shell_command(command_str):
    proc = subprocess.run(command_str, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    result = proc.stdout.split("=")
    return result[1].replace('\n', '')

if __name__ == '__main__':
    main()