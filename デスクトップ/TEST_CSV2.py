#!/usr/bin/env pthon3
# -*- coding: utf-8 -*-
# ver2.0→2_1 csv出力に対応
import os
import socket #UDP通信
import time #待機時間用
import struct #数値→バイト列変換用
import csv #csv用
from contextlib import closing #with用
import ipaddress #入力IPアドレスの形式確認
import datetime #時刻をインポート

#ファイル名前の入力
print("input File name?")
name = input()
f = open(str(name) + '.csv', 'w', newline='')

#CSVの１行目にヘッダーを入力
writer = csv.writer(f)

ini_data = [['Time' , 'RF-A' , ' RF-B']]
writer.writerows(ini_data)  #上で入力した初期値をCSVファイルに書き込み

