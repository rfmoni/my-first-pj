#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket #UDP送信
import time #待機時間用
import datetime
import struct #数値→バイト列変換用
from contextlib import closing #with用
import ipaddress #入力IPアドレスの形式確認用

import serial
ser = serial.Serial('/dev/ttyACM0', 115200)


#IPアドレスの入力関係
print("Destination IP address:")
while True:
  try:
    print(">",end="") #>を改行無しで表示
    inputip = input() #入力させる
    ipaddress.ip_address(inputip) #入力が誤った形式だとエラーを吐く
  except KeyboardInterrupt:
    exit() #Ctrl+Cが入力されたらプログラムを抜ける
  except:
    print("Incorrect IP address. input IP address again.(xxx.xxx.xxx.xxx)")
  else:
    break #正しいIPアドレスだったらwhileを抜ける
#送信の設定
host = inputip # 送信先（相手）IPアドレス
send_port = 60000 # 送信ポート番号
#受信の設定
recv_ip = "" #このままでいい
recv_port = 60000 #ポート番号
#2つのsocketを設定
socksend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #送信ソケットの設定
sockrecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #受信ソケットの生成
sockrecv.bind((recv_ip, recv_port)) #ソケットを登録する
#送受信
with closing(socksend), closing(sockrecv): #プログラム終了時にソケットを自動的に閉じる
  while True: #無限ループ
  
    #受信
    print("Waiting for receive...") #受信待機中であることを示す
    
   
    # 受信を待機する
    sr, addr = sockrecv.recvfrom(1024) #受信する
    #--受信していない間はここで止まる--
    r = struct.unpack('>d' , sr)[0] #受信したバイト列を数値に変換
    t = datetime.datetime.fromtimestamp(r)  #文字列から時刻へ変換
    print ( "receive: " , t) #数値に変換して表示
    
    # Picoの電圧を取得する
    s=""
    s=ser.readline()
    while ser.in_waiting:       # 受信があったときのみ送信する
        s= s + ser.readline()
    s2= s.split(b'\r')
    sf= (float(s2[0]))
    
    
    #送信
    print("send: ", str( sf )) #送信するバイト列を自分側に表示
    ss = struct.pack('>d', sf ) #計算結果をバイト列に変換
    socksend.sendto(ss, (host, send_port)) #ソケットにUDP送信