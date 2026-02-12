"""
The Media class provides methods to send consumer/media control keys
such as volume, play/pause, next, previous, etc., to a HID device.
"""

import time
from .media_keys import *

HID_DEVICE = "/dev/hidg3"


class Media:
    """
    A class for sending media / consumer control keys to a HID device.
    """

    @staticmethod
    def send_key(key_mask, hold=0):
        """
        Sends a media key press and then releases it.

        :param key_mask: Bit mask representing the media key(s) to press.
        :type key_mask: int
        :param hold: Time in seconds to hold the key before releasing it.
        :type hold: float, optional
        """
        Media._send_report(key_mask)
        if hold:
            time.sleep(hold)
        Media.release_keys()

    @staticmethod
    def hold_key(key_mask):
        """
        Sends a media key press without releasing it.

        :param key_mask: Bit mask representing the media key(s) to hold.
        :type key_mask: int
        """
        Media._send_report(key_mask)

    @staticmethod
    def release_keys():
        """
        Releases all currently held media keys.
        """
        Media._send_report(0x0000)

    @staticmethod
    def _send_report(key_mask):
        """
        Sends a raw HID consumer control report.

        Report length: 2 bytes (16 bits)
        Each bit represents one media key.

        :param key_mask: Bit mask of keys to send.
        :type key_mask: int
        """
        report = key_mask.to_bytes(2, byteorder="little")
        with open(HID_DEVICE, "rb+") as fd:
            fd.write(report)

