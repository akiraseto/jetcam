import serial
from datetime import datetime


class RealCommunicator():
    def __init__(self, portname):
        self.ser = serial.Serial(portname, 115200, timeout=None)
        self.ser.reset_input_buffer()
        self.last_written_time = datetime.now().timestamp()

    def _encode_byte(self, item):
        assert (0 <= item and item < 256)
        q1, mod1 = divmod(item, 16)
        q2, mod2 = divmod(q1, 16)
        assert (q2 == 0)
        return (mod2, mod1)

    def write(self, items):
        for item in items:
            for b in self._encode_byte(item):
                # Wait for transmission interval
                current_time = datetime.now().timestamp()
                while (current_time - self.last_written_time) < 0.003:
                    current_time = datetime.now().timestamp()
                self.ser.write(bytes([b]))
                self.last_written_time = datetime.now().timestamp()

    def read(self):
        # Clear input buffer until receive b'\xfe'
        while True:
            r = self.ser.read(1)
            if r == b'\xfe':
                break
        r = self.ser.read(1)
        return int(r[0])

    def close(self):
        self.ser.close()


class EV3():
    # sensor_port_t
    PORT_1 = 0
    PORT_2 = 1
    PORT_3 = 2
    PORT_4 = 3

    # sensor_type_t
    NONE_SENSOR = 0
    ULTRASONIC_SENSOR = 1
    GYRO_SENSOR = 2
    TOUCH_SENSOR = 3
    COLOR_SENSOR = 4
    INFRARED_SENSOR = 5
    HT_NXT_ACCEL_SENSOR = 6
    NXT_TEMP_SENSOR = 7
    TNUM_SENSOR_TYPE = 8

    # colorid_t
    COLOR_NONE = 0
    COLOR_BLACK = 1
    COLOR_BLUE = 2
    COLOR_GREEN = 3
    COLOR_YELLOW = 4
    COLOR_RED = 5
    COLOR_WHITE = 6
    COLOR_BROWN = 7
    TNUM_COLOR = 8

    # motor_port_t
    PORT_A = 0
    PORT_B = 1
    PORT_C = 2
    PORT_D = 3
    TNUM_MOTOR_PORT = 4

    # motor_type_t
    NONE_MOTOR = 0
    MEDIUM_MOTOR = 1
    LARGE_MOTOR = 2
    UNREGULATED_MOTOR = 3
    TNUM_MOTOR_TYPE = 4

    # button_t
    LEFT_BUTTON = 0
    RIGHT_BUTTON = 1
    UP_BUTTON = 2
    DOWN_BUTTON = 3
    ENTER_BUTTON = 4
    BACK_BUTTON = 5
    TNUM_BUTTON = 6

    def __init__(self):
        portname = '/dev/ttyUSB0'
        self.com = RealCommunicator(portname)
        for i in range(7):
            self.lcd_clear_line(i)

    def __del__(self):
        self.close()

    def close(self):
        self.com.close()

    def _write(self, items):
        self.com.write(items)

    def _read(self):
        return self.com.read()

    def _send_header(self, cmd_id):
        self._write([255, cmd_id])

    def motor_config(self, motor_port, motor_type):
        self._send_header(0)
        self._write([motor_port, motor_type])

    def enable_watchdog_task(self):
        self._send_header(1)

    def motor_steer(self, left_motor_port, right_motor_port, drive, steer):
        self._send_header(10)
        drive = int(drive) + 100
        steer = int(steer) + 100
        drive = min(max(drive, 0), 200)
        steer = min(max(steer, 0), 200)
        self._write([left_motor_port, right_motor_port, drive, steer])

    def motor_set_power(self, motor_port, power):
        self._send_header(20)
        power = int(power) + 100
        power = min(max(power, 0), 200)
        self._write([motor_port, power])

    def motor_stop(self, motor_port):
        self._send_header(30)
        self._write([motor_port])

    def motor_rotate(self, motor_port, degrees, speed):
        self._send_header(50)
        speed = min(max(speed, 0), 100)
        self._write([motor_port, degrees, speed])

    def sensor_config(self, sensor_port, sensor_type):
        self._send_header(100)
        self._write([sensor_port, sensor_type])

    def touch_sensor_is_pressed(self, touch_sensor_port):
        self._send_header(110)
        self._write([touch_sensor_port])
        touch = self._read()
        assert (touch == 1 or touch == 0)
        return True if touch == 1 else False

    def color_sensor_get_reflect(self, color_sensor_port):
        self._send_header(120)
        self._write([color_sensor_port])
        color = self._read()
        assert (color <= 100)
        return color

    def lcd_draw_string(self, string, line):
        self._send_header(200)
        self._write([line])
        if len(string) < 20:
            string = string + ' ' * (20 - len(string))
        items = [ord(x) for x in string]
        items.append(0)
        self._write(items)

    def lcd_clear_line(self, line):
        self.lcd_draw_string(' ' * 20, line)

    def button_is_pressed(self, button):
        self._send_header(210)
        self._write([button])
        state = self._read()
        assert (state == 1 or state == 0)
        return True if state == 1 else False
