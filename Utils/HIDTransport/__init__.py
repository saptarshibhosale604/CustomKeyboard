"""
HIDTransport
============

Single place where HID reports leave the Pi.

The Keyboard, Mouse and Media writers build their raw reports exactly as
before and hand them to `send(channel, report)`. Depending on the mode chosen
at startup, the report is written to the USB gadget (/dev/hidgN) or sent over
Classic Bluetooth HID.

- set_mode("usb" | "bluetooth")  -> call once at startup, before sending
- send("keyboard" | "mouse" | "media", report_bytes)
"""

MODES = ("usb", "bluetooth")

USB_DEVICES = {
    "keyboard": "/dev/hidg0",
    "mouse": "/dev/hidg1",  # relative mouse
    "media": "/dev/hidg3",
}

_mode = "usb"
_usbMouseDev = None


def set_mode(mode):
    global _mode
    if mode not in MODES:
        raise ValueError(f"Unknown transport '{mode}', expected one of {MODES}")
    _mode = mode


def get_mode():
    return _mode


def send(channel, report):
    if _mode == "bluetooth":
        from . import bluetooth
        bluetooth.send(channel, report)
    else:
        _send_usb(channel, report)


def _send_usb(channel, report):
    global _usbMouseDev

    if channel == "mouse":
        # Keep zero-hid's write path (timeout-protected subprocess write)
        from Utils.HIDMouse.hid import write as hid_write
        if _usbMouseDev is None:
            _usbMouseDev = open(USB_DEVICES["mouse"], "ab+")
        hid_write.write_to_hid_interface(_usbMouseDev, report)
        return

    with open(USB_DEVICES[channel], "rb+") as fd:
        fd.write(report)
