#!/usr/bin/python

# todo:最後に外す(リモートデバッグ用コード)
import pydevd_pycharm
pydevd_pycharm.settrace('192.168.0.7', port=60000, stdoutToServer=True, stderrToServer=True)


import socket
import RPi.GPIO as GPIO

PNO = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(PNO, GPIO.OUT)

def pin(message):
    if message == 'on':
        GPIO.output(PNO, GPIO.HIGH)
    elif message == 'off':
        GPIO.output(PNO, GPIO.LOW)



if __name__ == '__main__':

    M_SIZE = 1024

    host = '0.0.0.0'
    port = 10000

    locaddr = (host, port)

    # ①ソケットを作成する
    sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
    print('create socket')

    # ②自ホストで使用するIPアドレスとポート番号を指定
    sock.bind(locaddr)

    while True:
        data = sock.recv(M_SIZE)
        data = data.decode()
        print(data)
        pin(data)

