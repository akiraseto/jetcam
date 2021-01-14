import time
from ev3 import EV3

# jetBrainsリモートデバッグ用モジュール
# import pydevd_pycharm
#
# pydevd_pycharm.settrace('192.168.0.20', port=60000,
#                         stdoutToServer=True, stderrToServer=True)

# モーターとセンサーの通信ポートの定義.
sensor_pan = EV3.PORT_2
sensor_pedestal = EV3.PORT_3
start_switch = EV3.PORT_4

# 回転: pan +時計回り
pan = EV3.PORT_A
# 上下移動: pedestal +下がる
pedestal = EV3.PORT_B
# 上下角: tilt -上がる
tilt = EV3.PORT_C

# モーターとセンサーの初期設定.
ev3 = EV3()
ev3.sensor_config(sensor_pan, EV3.TOUCH_SENSOR)
ev3.sensor_config(sensor_pedestal, EV3.TOUCH_SENSOR)
ev3.sensor_config(start_switch, EV3.TOUCH_SENSOR)
ev3.motor_config(pan, EV3.LARGE_MOTOR)
ev3.motor_config(pedestal, EV3.LARGE_MOTOR)
ev3.motor_config(tilt, EV3.MEDIUM_MOTOR)

# タッチセンサーが押されたら発進
print("スタートスイッチを押してください。")
while not ev3.touch_sensor_is_pressed(start_switch):
    pass
print("Start!")

ev3.motor_set_power(pan, 0)
print('pan', ev3.touch_sensor_is_pressed(sensor_pan))

ev3.motor_set_power(pedestal, 5)
print('pedestal', ev3.touch_sensor_is_pressed(sensor_pedestal))
ev3.motor_set_power(tilt, 0)
time.sleep(1)

ev3.motor_stop(pan, False)
ev3.motor_stop(pedestal, True)
ev3.motor_stop(tilt, False)

# 終了処理.
ev3.close()
print("Stop!")
