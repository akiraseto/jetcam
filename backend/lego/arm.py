import time
from lego.ev3 import EV3


class Lego_arm:
    """レゴアームを制御

    モジュールの指定と、スピード、起動時間をLego EV3に渡す
    """

    def __init__(self):
        # モーターとセンサーの通信ポートの定義.
        self.sensor_pan = EV3.PORT_2
        self.sensor_pedestal = EV3.PORT_3
        self.stop_switch = EV3.PORT_4

        # 回転: pan +時計回り
        self.pan = EV3.PORT_A
        # 上下移動: pedestal +下がる
        self.pedestal = EV3.PORT_B
        # 上下角: tilt -上がる
        self.tilt = EV3.PORT_C

        # モーターとセンサーの初期設定.
        self.ev3 = EV3()
        self.ev3.sensor_config(self.sensor_pan, EV3.TOUCH_SENSOR)
        self.ev3.sensor_config(self.sensor_pedestal, EV3.TOUCH_SENSOR)
        self.ev3.sensor_config(self.stop_switch, EV3.TOUCH_SENSOR)
        self.ev3.motor_config(self.pan, EV3.LARGE_MOTOR)
        self.ev3.motor_config(self.pedestal, EV3.LARGE_MOTOR)
        self.ev3.motor_config(self.tilt, EV3.MEDIUM_MOTOR)

        # 緊急停止の調整値
        self.stop_adjust = {
            'pan': {
                'power': -50,
                'time': 0.1
            },
            'pedestal': {
                'power': 90,
                'time': 0.12
            }
        }

    def move_motor(self, data):
        """lego motorを動かす 調整値
        """

        module = None
        power = int(data['power'])
        interval = float(data['time'])
        if interval < 0.1:
            interval = 0.1
        elif interval > 10:
            interval = 10
        breaking = False

        if data['move'] == 'pan':
            module = self.pan
        elif data['move'] == 'pedestal':
            module = self.pedestal
            breaking = True
        elif data['move'] == 'tilt':
            module = self.tilt

        self.ev3.motor_set_power(module, power)

        # 安全装置
        t_end = time.time() + interval
        while time.time() < t_end:
            if self.ev3.touch_sensor_is_pressed(self.stop_switch):
                print('stop arm')
                break

            if self.ev3.touch_sensor_is_pressed(self.sensor_pan):
                self.ev3.motor_stop(self.pan, False)
                self.ev3.motor_set_power(self.pan,
                                         self.stop_adjust['pan']['power'])
                time.sleep(self.stop_adjust['pan']['time'])
                print('stop pan')
                break

            if self.ev3.touch_sensor_is_pressed(self.sensor_pedestal):
                self.ev3.motor_stop(self.pedestal, False)
                self.ev3.motor_set_power(self.pedestal,
                                         self.stop_adjust['pedestal']['power'])
                time.sleep(self.stop_adjust['pedestal']['time'])
                print('stop pedestal')
                break

        self.ev3.motor_stop(module, breaking)

    def close(self):
        self.ev3.close()
        print("LEGO Close!")
