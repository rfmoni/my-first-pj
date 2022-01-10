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


#IPアドレスの入力関係
print("Destination IP address:")
while True:
    try:
        print(">",end="") #>を改行なしで表示
        inputip = input() #入力させる
        ipaddress.ip_address(inputip) #入力が誤った形式だとエラーを吐く
    except KeybordInterrupt:
        exit() #Ctrl+Cが入力されたらプログラムを抜ける
    except:
        print("Incorrect IP address. input IP address again.(xxx.xxx.xxx.x)")
    else:
        break #正しいIPアドレスだったらwhileを抜ける
#送信の設定
host = inputip #送信先（相手）IPアドレス
send_port = 60000 #送信ポート番号
#受信の設定
recv_ip = "" #このままでいい
recv_port = 60000 #ポート番号
#2つのsocketを設定
socksend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #送信ソケット
sockrecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #受信ソケット
sockrecv.bind((recv_ip, recv_port)) #ソケットを登録する

#送受信
#プログラム終了時にソケットを自動的に閉じ、CSVファイルも閉じる
with closing(socksend), closing(sockrecv):
# , open(str(name) + '.csv') as f:
    try:
        while True: #無限ループ
            
            #受信
            print("Waiting for receive...") #受信待機中であることを示す

            #受信を待機する
            srt, addr = sockrecv.recvfrom(1024) #受信する
            srrfa, addr = sockrecv.recvfrom(1024) #受信する
            srrfb, addr = sockrecv.recvfrom(1024) #受信する

            #--受信していない間はここで止まる--
            rnow = srt.decode()
            print ("receive_time: " , rnow ) #数値に変換して表示
            rrfa = struct.unpack('>d' , srrfa)[0] #受信したバイト列を数値に変換
            rrfb = struct.unpack('>d' , srrfb)[0] #受信したバイト列を数値に変換       print ("receive_time: " , rnow ) #数値に変換して表示
            print ("receive_RF_A_DATA: " , str( rrfa )) #数値に変換して表示
            print ("receive_RF_B_DATA: " , str( rrfb )) #数値に変換して表示
      
            #時刻と受信データをCSVファイルに入力
            rfdata = [[str(rnow) ,str(rrfa) ,str(rrfb)]]
            writer.writerows(rfdata)
        
    #処理を止める
    except KeyboardInterrupt: #Ctrl-Cを捕まえた
        print('処理を止めました')
        f.close()