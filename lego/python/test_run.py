import time
from ev3 import EV3

# jetBrainsリモートデバッグ用モジュール
import pydevd_pycharm

pydevd_pycharm.settrace('192.168.0.20', port=60000,
                        stdoutToServer=True, stderrToServer=True)

# モーターとセンサーの通信ポートの定義.
touch_port = EV3.PORT_2
lmotor_port = EV3.PORT_B
mini_motor_port = EV3.PORT_D

# モーターとセンサーの初期設定.
ev3 = EV3()
ev3.motor_config(lmotor_port, EV3.LARGE_MOTOR)
ev3.motor_config(mini_motor_port, EV3.MEDIUM_MOTOR)
ev3.sensor_config(touch_port, EV3.TOUCH_SENSOR)

# タッチセンサーが押されたら発進.
print("Push touch sensor to run your EV3.")
while not ev3.touch_sensor_is_pressed(touch_port):
    pass
print("Go!")
ev3.motor_steer(lmotor_port, mini_motor_port, 50, 0)
time.sleep(3)

# ３秒間立ったら停止.
print("Stop.")
ev3.motor_steer(lmotor_port, mini_motor_port, 0, 0)

# 終了処理.
ev3.close()
