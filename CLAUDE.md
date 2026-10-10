# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Firmware-in-Python for a custom 4x10 matrix keyboard wired to a Raspberry Pi 5's GPIO. `main.py` scans the matrix and sends HID reports (keyboard + relative mouse + media keys) to a host either as a composite USB HID gadget (`/dev/hidg*`) or as a Classic Bluetooth HID device, chosen at startup with `--transport`.

There is no build system, linter or test suite. Code can only be exercised on the Pi with a host attached over USB-C or paired over Bluetooth.

## Commands

```bash
# One-time: install the USB gadget (copies init_usb_gadget to /usr/bin, enables usb_gadget.service), then reboot
cd Initialization && sudo ./installer      # running it again offers to uninstall

# Tear down / rebuild the gadget by hand
sudo ./Initialization/remove_usb_gadget
sudo ./Initialization/init_usb_gadget

# Run the keyboard (must be run from repo root so `Utils.*` imports resolve)
python main.py                                   # USB (default)
sudo python3 main.py --transport bluetooth       # Bluetooth, root needed to bind L2CAP PSM 17/19

# One-time Bluetooth setup (apt deps, bluetoothd -P input, adapter class/name); run again to uninstall
sudo Initialization/bluetooth/install_bluetooth
```

`main.py` aborts with "No HID device found" if `/dev/hidg*` is missing — the gadget is not set up. The Pi also needs `dtoverlay=dwc2` in `/boot/firmware/config.txt` and `dwc2`/`libcomposite` in `/etc/modules`; the installer has those lines commented out, so they're expected to be done manually. `gpiozero` is the only third-party dependency (a local `venv/` is gitignored).

Quit the running script with the `SPECIAL_QUIT_KEYBOARD` key (see `WelcomeScript()` for its current location).

## Output transports

All writers (`Keyboard._send_report`, `Media._send_report`, zero-hid's `relative_mouse_event` when `dev is None`) call `Utils/HIDTransport.send(channel, report)` with channel `keyboard`/`mouse`/`media`. Don't write to `/dev/hidg*` directly from new code. `HIDTransport.set_mode()` is called in `main.py`'s `__main__` from `--transport`.

- **usb**: writes to the hidg devices below.
- **bluetooth** (`Utils/HIDTransport/bluetooth.py`): publishes an SDP HID record and a Just-Works pairing agent over BlueZ D-Bus, listens on its own L2CAP sockets, and sends `0xA1, reportId, <USB report bytes>` (IDs: keyboard 1, mouse 2, media 3). Reports sent while no host is connected are dropped and trigger a reconnect to a paired host. Its `REPORT_DESCRIPTOR` is a copy of the USB descriptors plus Report IDs, so change both together.

### USB HID device mapping

Defined by the configfs descriptors in `Initialization/init_usb_gadget`; the order the functions are linked determines the hidg numbers:

| Device | Function | Used by |
|---|---|---|
| `/dev/hidg0` | Keyboard (8-byte boot report) | `Utils/HIDKeyboard/keyboard.py` |
| `/dev/hidg1` | Relative mouse (buttons, X, Y, wheel, AC pan) | `Utils/HIDMouse` (vendored from zero-hid) via `Utils/mouseManager.py` |
| `/dev/hidg2` | Absolute mouse | `Utils/HIDMouse` (unused by main) |
| `/dev/hidg3` | Consumer/media (16-bit bitmask) | `Utils/HIDMedia/media.py` |

If you change a report descriptor or add a function, the matching Python writer and these device paths must change together. `Utils/HIDMedia/media_keys.py` bit positions must match the usage order in the media descriptor.

## Architecture

**Matrix scan** (`main.py`): rows `ROW_PINS_BCM` are driven high one at a time, columns `COL_PINS_BCM` read as pull-down `Button`s. `ScanMatrix()` returns a set of `(row, col)`.

**Layers** (`Utils/layers.py`): each layer is a 4x10 grid of key *name strings*, with two parallel maps — `LAYER_SHORT_MAP` (tap) and `LAYER_LONG_MAP` (hold ≥ `longPressTime`) — keyed by layer number, each entry `{"name", "description", "layout"}`. `gamingLayerNumber`, `layerChangeLayerNumber` and `maxLayer` live here too. Layer 6 (gaming) has only a short map.

**Two input modes in `MainLoop()`:**
- *Normal layers* (1..gaming-1, and the layer-change layer): tap/hold logic. `HandleLayerXPress` records press time (and starts mouse actions), `HandleLayerXHold` fires the long-press action once the threshold passes and adds the key to `longSent`, `HandleLayerXRelease` sends the short-press action unless the key is in `longSent`. So taps fire on **release**, holds fire while held.
- *Gaming layer*: `UpdateKeyboardGamingLayer()` sends true n-key (max 6) hold-down reports with no tap/hold distinction.

**Key-name dispatch:** strings in layouts are resolved by prefix in the Hold/Release handlers:
- plain name (e.g. `'A'`, `'LEFT_SHIFT'`) → looked up as `KEY_<name>` in `keyMap`, which is built from every `KEY_*` global pulled in by `from ...keyboard_keys import *` and `from ...media_keys import *`. A new plain key name needs a `KEY_` constant in one of those modules or it will `KeyError` at runtime.
- `FUNCTION_*`, `SPECIAL_*`, `PRINT_*`, `SHORTCUT_*` → tables in `Utils/combos.py`. `modifierNames` there decides what counts as a modifier.
- `LAYER_UP/DOWN`, `LAYER_CHANGE_<n|BASE|GAMING|LAYER>`, `LAYER_TEMP_LAYER_UP_01/02` (momentary layer while held; holding both jumps to the layer-change layer).
- `MOUSE_*` → `mouseManager.Main(action, pressed)` / `MouseSpeed()`; `MEDIA_*` → `Media.send_key`; `ACTION_SHUTDOWN/REBOOT` and `FUNCTION_PRINT_SSH_CMD` → `Utils/piSystemActions.py`; `ONE_SHOT_MODIFIER_*`, `ONE_HANDED_*` → modifier handling.

Modifier state is the global `activeModifiers` bitmask in `main.py`; held modifiers (home-row mods in `L1_LONG`) use `Keyboard.hold_key` and are released on key-up via `isModifierHold`.

## Repo layout notes

- `Other/` holds old experiments, backups (`*.bak`) and a full copy of the upstream `zero-hid` project — reference only, not imported by `main.py`.
- `Temp/` is gitignored scratch. `*.bak` files throughout are historical snapshots; edit the non-`.bak` file.
- `README.md` is a personal notes log (gadget setup, manual teardown steps, descriptor experiments) rather than project docs.
