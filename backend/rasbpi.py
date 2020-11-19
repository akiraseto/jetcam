#!/usr/bin/python

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

    loc_addr = (host, port)

    # ソケット作成
    sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
    print('create socket')

    # 自ホストで使用するIPアドレスとポート番号を指定
    sock.bind(loc_addr)

    while True:
        data = sock.recv(M_SIZE)
        data = data.decode(encoding="utf8", errors='ignore')
        print(data)
        pin(data)
