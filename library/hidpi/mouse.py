# hidpi/mouse.py
import time

MOUSE_DEVICE = "/dev/hidg1"

class Mouse:
    _fd = None

    @staticmethod
    def _open():
        if Mouse._fd is None:
            Mouse._fd = open(MOUSE_DEVICE, "rb+", buffering=0)

    @staticmethod
    def move(x, y, wheel=0):
        Mouse._open()
        report = bytes([
            0,
            x & 0xFF,
            y & 0xFF,
            wheel & 0xFF
        ])
        Mouse._fd.write(report)

    @staticmethod
    def click(button, hold=0):
        Mouse._open()
        Mouse._fd.write(bytes([button, 0, 0, 0]))
        if hold:
            time.sleep(hold)
        Mouse._fd.write(bytes([0, 0, 0, 0]))

