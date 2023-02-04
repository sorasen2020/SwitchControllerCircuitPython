import struct
from time import sleep
from adafruit_hid import find_device

BUTTON_PUSHING_SEC = 0.04

class Button:
    Y       = 0x0001
    B       = 0x0002
    A       = 0x0004
    X       = 0x0008
    L       = 0x0010
    R       = 0x0020
    ZL      = 0x0040
    ZR      = 0x0080
    MINUS   = 0x0100
    PLUS    = 0x0200
    LCLICK  = 0x0400
    RCLICK  = 0x0800
    HOME    = 0x1000
    CAPTURE = 0x2000


class Hat:
    TOP       = 0
    TOP_RIGHT = 1
    RIGHT     = 2
    BTM_RIGHT = 3
    BTM       = 4
    BTM_LEFT  = 5
    LEFT      = 6
    TOP_LEFT  = 7
    CENTER    = 8


class Direction:
    CENTER        = 0x00
    L_UP          = 0x01
    L_UP_RIGHT    = 0x02
    L_RIGHT       = 0x03
    L_DOWN_RIGHT  = 0x04
    L_DOWN        = 0x05
    L_DOWN_LEFT   = 0x06
    L_LEFT        = 0x07
    L_UP_LEFT     = 0x08
    R_UP          = 0x01
    R_UP_RIGHT    = 0x02
    R_RIGHT       = 0x03
    R_DOWN_RIGHT  = 0x04
    R_DOWN        = 0x05
    R_DOWN_LEFT   = 0x06
    R_LEFT        = 0x07
    R_UP_LEFT     = 0x08


class Stick:
    MIN      = 0
    CENTER   = 128
    MAX      = 255


class SwitchController:

    def __init__(self, devices):
        self._gamepad_device = find_device(devices, usage_page=0x1, usage=0x05)

        self._report = bytearray(8)

        self._button = 0
        self._hat    = Hat.CENTER
        self._lx     = Stick.CENTER
        self._ly     = Stick.CENTER
        self._rx     = Stick.CENTER
        self._ry     = Stick.CENTER
        self._dummy  = 0

        self._button_pushing_sec = BUTTON_PUSHING_SEC

        try:
            self.reset_all()
        except OSError:
            sleep(1)
            self.reset_all()


    def wait(self, wait):
        sleep(wait)


    def set_button_pushing_time(self, time_sec: float):
        """
        ボタンを押す時間を設定する

        Args:
        time_sec (float): 入力後の待機時間
        """
        self._button_pushing_msec = time_sec


    def press_button(self, button: Button):
        """
        ボタンを押す

        Args:
        button (Button): 押すボタン
        """
        self._button = button
        self._sendreport()


    def release_button(self, button: Button):
        """
        ボタンを離す

        Args:
        button (Button): 離すボタン
        """
        self._button &= (button ^ 0xffff)
        self._sendreport()


    def press_hatbutton(self, hat: Hat):
        """
        HAT(十字キー)を押す

        Args:
        hat (Hat): 押すHAT(十字キー)ボタン
        """
        self._hat = hat
        self._sendreport()


    def release_hatbutton(self):
        """
        HAT(十字キー)を離す
        """
        self._hat = Hat.CENTER
        self._sendreport()


    def set_sticktiltratio(self, lx_per, ly_per, rx_per, ry_per):
        """
        ジョイスティックの倒し量を設定する

        Args:
        lx_per (int)                : LスティックのX方向倒し量[%] -100~100の範囲で設定
        ly_per (int)                : LスティックのY方向倒し量[%] -100~100の範囲で設定
        rx_per (int)                : RスティックのX方向倒し量[%] -100~100の範囲で設定
        ry_per (int)                : RスティックのY方向倒し量[%] -100~100の範囲で設定
        """
        self._lx = (lx_per * 0xFF / 200 + 0x80)
        self._ly = (ly_per * 0xFF / 200 + 0x80)
        self._rx = (rx_per * 0xFF / 200 + 0x80)
        self._ry = (ry_per * 0xFF / 200 + 0x80)
        self._sendreport()


    def reset_all(self):
        """
        コントローラの入力を全てリセット
        """
        self._button = 0
        self._hat    = Hat.CENTER
        self._lx     = Stick.CENTER
        self._ly     = Stick.CENTER
        self._rx     = Stick.CENTER
        self._ry     = Stick.CENTER
        self._sendreport()


    def push_button(self, button: Button, delay_after_pushing_sec: float, loop_num: int):
        """
        ボタンを指定回数を押す

        Args:
        button (Button)                : 押すボタン
        delay_after_pushing_sec (float): ボタンを押し終えた後の待ち時間(秒)
        loop_num (int)                 : ボタンを押す回数
        """
        for _i in range(loop_num):
            self.press_button(button)
            self.wait(self._button_pushing_sec)
            self.release_button(button)
            self.wait(delay_after_pushing_sec)


    def push_button2(self, button: Button, pushing_time_sec: float, delay_after_pushing_sec: float, loop_num: int):
        """
        ボタンを指定回数を押す

        Args:
        button (Button)                : 押すボタン
        pushing_time_sec (float)       : ボタンを押す時間の長さ(秒)
        delay_after_pushing_sec (float): ボタンを押し終えた後の待ち時間(秒)
        loop_num (int)                 : ボタンを押す回数
        """
        for _i in range(loop_num):
            self.press_button(button)
            self.wait(pushing_time_sec)
            self.release_button(button)
            self.wait(delay_after_pushing_sec)


    def push_hatbutton(self, hat: Hat, delay_after_pushing_sec: float, loop_num: int):
        """
        HAT(十字キー)を指定回数を押す

        Args:
        hat (Hat)                      : 押すHAT(十字キー)
        delay_after_pushing_sec (float): ボタンを押し終えた後の待ち時間(秒)
        loop_num (int)                 : ボタンを押す回数
        """
        for i in range(loop_num):
            self.press_hatbutton(hat)
            self.wait(self._button_pushing_sec)
            self.release_hatbutton(hat)
            self.wait(delay_after_pushing_sec)


    def push_hatbutton_continuous(self, hat: Hat, pushing_time_sec: float):
        """
        HAT(十字キー)を指定時間の間押し続ける

        Args:
        hat (Hat)               : 押すHAT(十字キー)
        pushing_time_sec (float): ボタンを押す時間(秒)
        """
        self.press_hatbutton(hat)
        self.wait(pushing_time_sec)
        self.release_hatbutton(hat)
        self.wait(self._button_pushing_sec)


    def tilt_joystick(self, lx_per: int, ly_per: int, rx_per: int, ry_per: int, tilt_time_sec: float, delay_after_tilt_sec: float):
        """
        ジョイスティックの倒し量を設定する

        Args:
        lx_per (int)                : LスティックのX方向倒し量[%] -100~100の範囲で設定
        ly_per (int)                : LスティックのY方向倒し量[%] -100~100の範囲で設定
        rx_per (int)                : RスティックのX方向倒し量[%] -100~100の範囲で設定
        ry_per (int)                : RスティックのY方向倒し量[%] -100~100の範囲で設定
        tilt_time_sec (float)       : スティックを倒し続ける時間(秒)
        delay_after_tile_sec (float): スティックを倒しえた後の待ち時間(秒)
        """
        self.set_sticktiltratio(lx_per, ly_per, rx_per, ry_per)
        self.wait(tilt_time_sec)
        if (delay_after_tilt_sec > 0):
            self.set_sticktiltratio(0, 0, 0, 0)
            self.wait(delay_after_tilt_sec)


    def use_lstick(self, lstick: Direction, tilt_time_sec: float, delay_after_tilt_sec: float):
        """
        左スティックを指定時間の間倒し続ける

        Args:
        lstick (Direction)          : 傾ける方向
        tilt_time_sec (float)       : 倒し続ける時間(秒)
        delay_after_tilt_sec (float): 倒し終えた後の待ち時間(秒)
        """
        lx_per = 0
        ly_per = 0
        rx_per = 0
        ry_per = 0

        if lstick == Direction.L_DOWN:
            ly_per = 100
        elif lstick == Direction.L_UP:
            ly_per = -100
        elif lstick == Direction.L_LEFT:
            lx_per = -100
        elif lstick == Direction.L_RIGHT:
            lx_per = 100
        self.tilt_joystick(lx_per, ly_per, rx_per, ry_per, tilt_time_sec, delay_after_tilt_sec)


    def use_rstick(self, rstick: Direction, tilt_time_sec: float, delay_after_tilt_sec: float):
        """
        右スティックを指定時間の間倒し続ける

        Args:
        rstick (Direction)          : 傾ける方向
        tilt_time_sec (float)       : 倒し続ける時間(秒)
        delay_after_tilt_sec (float): 倒し終えた後の待ち時間(秒)
        """
        lx_per = 0
        ly_per = 0
        rx_per = 0
        ry_per = 0

        if rstick == Direction.R_DOWN:
            ry_per = 100
        elif rstick == Direction.R_UP:
            ry_per = -100
        elif rstick == Direction.R_LEFT:
            rx_per = -100
        elif rstick == Direction.R_RIGHT:
            rx_per = 100
        self.tilt_joystick(lx_per, ly_per, rx_per, ry_per, tilt_time_sec, delay_after_tilt_sec)


    def _sendreport(self):
        self._report = struct.pack(
            "<HBBBBBb",
            self._button,
            self._hat,
            self._lx,
            self._ly,
            self._rx,
            self._ry,
            self._dummy
        )
        self._gamepad_device.send_report(self._report)


    def sendreport(self, report):
        self._gamepad_device.send_report(report)