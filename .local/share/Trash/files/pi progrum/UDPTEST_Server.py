#UDPTEST_Serverをベースに
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket #UDP送信
import time #待機時間用
import struct #数値→バイト列変換用
from contextlib import closing #with用
import ipaddress #入力IPアドレスの形式確認用
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
    r = struct.unpack('>i' , sr)[0] #受信したバイト列を数値に変換
    print ( "receive: " , str( r )) #数値に変換して表示
    
    #処理
    s = 1.0 / ( 2.0 * r - 1.0 )
    if r % 2 == 0 :
      s = -s
    #送信
    # 受信があったときのみ送信する
    print("send: ", str( s )) #送信するバイト列を自分側に表示
    ss = struct.pack('>d', s ) #計算結果をバイト列に変換
    socksend.sendto(ss, (host, send_port)) #ソケットにUDP送信