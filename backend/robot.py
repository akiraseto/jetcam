import socket
import json

import RPi.GPIO as GPIO


class Robot:
    """物理的動作させる

    DataConnectionからの内容により、GPIOに信号を渡す
    """

    def __init__(self):
        self.PNO = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PNO, GPIO.OUT)

        self.M_SIZE = 1024
        self.host = '0.0.0.0'
        self.port = 10000
        self.sock = None

    def pin(self, data):
        """GPIOピンに伝達
        """

        if data == 'on':
            GPIO.output(self.PNO, GPIO.HIGH)
        elif data == 'off':
            GPIO.output(self.PNO, GPIO.LOW)

    def make_socket(self):
        """socketの準備
        """

        print('create socket')
        loc_addr = (self.host, self.port)

        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind(loc_addr)

    def recv_data(self):
        """データを受け取る
        """

        try:
            data = self.sock.recv(self.M_SIZE)
            return data
        except Exception as e:
            print('socket error:', e)
            self.make_socket()

    def socket_loop(self, queue, lego):
        """ソケット通信を待ち受ける
        """

        self.make_socket()
        while True:
            data = self.recv_data()
            data = data.decode(encoding="utf8", errors='ignore')
            data = data[2:]
            json_data = json.loads(data)

            if 'message' in json_data.keys():
                queue.put(json_data)
                self.pin(json_data['message'])

            elif 'lego' in json_data.keys():
                print(json_data)
                lego.move_motor(json_data['lego'])

    @staticmethod
    def close():
        GPIO.cleanup()
        print('GPIO clean up')
