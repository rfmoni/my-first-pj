#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import itertools
import math
import numpy as np
 
import serial
ser = serial.Serial('/dev/ttyACM0', 115200)
 
from matplotlib import pyplot as plt
from matplotlib import animation
 
from subprocess import getoutput
 
 
def _update(frame, x, y):
    """グラフを更新するための関数"""
    # 現在のグラフを消去する
    plt.cla()
    # データを更新 (追加) する
    x.append(frame)
    
    # Picoの電圧を取得する
    a=""
    a=ser.readline()
    while ser.in_waiting:
        a= a + ser.readline()
    a2= a.split(b'\r')
    y.append(float(a2[0]))
 
    # 折れ線グラフを再描画する
    plt.plot(x, y)
    
    # グラフのタイトルに電圧を表示する
    plt.title("CH* = "+ str(y[-1]) +" V")
       
    # グラフの縦軸_電圧の範囲を指定する
    plt.ylim(0,3.5)
 
def main():
    # 描画領域
    fig = plt.figure(figsize=(10, 6))
    # 描画するデータ
    x = []
    y = []
    
    params = {
        'fig': fig,
        'func': _update,  # グラフを更新する関数
        'fargs': (x, y),  # 関数の引数 (フレーム番号を除く)
        'interval': 1000,  # 更新間隔 (ミリ秒)
        'frames': itertools.count(0, 1),  # フレーム番号を無限に生成するイテレータ
    }
    anime = animation.FuncAnimation(**params)
 
    # グラフを表示する
    plt.show()
 
if __name__ == '__main__':
    main()