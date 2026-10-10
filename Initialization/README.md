# usb gadget module configuration for [zero-hid](https://github.com/thewh1teagle/zero-hid)

To be able to use `zero-hid` package
it's necessary to change some configuration on the kernel.

### Install / remove the module
clone the repo if you haven't yet
```bash
git clone https://github.com/thewh1teagle/zero-hid
```

get into usb_gadget folder
```bash
cd zero-hid/usb_gadget
```
Execute `installer`
```bash
sudo ./installer
```

# Bluetooth mode (CustomKeyboard)

The keyboard can also run as a Classic Bluetooth HID device instead of over USB:

```bash
sudo ./bluetooth/install_bluetooth                 # once: deps, bluetoothd -P input, keyboard class/name
sudo python3 main.py --transport bluetooth         # from the repo root
```

Then pair "CustomKeyboard" from the host. Running `install_bluetooth` again uninstalls it.
