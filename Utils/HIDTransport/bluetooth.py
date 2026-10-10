"""
bluetooth.py

Classic Bluetooth HID (BR/EDR) device for the custom keyboard.

- Publishes an SDP HID record through BlueZ (org.bluez.ProfileManager1)
- Registers a "Just Works" pairing agent (NoInputNoOutput)
- Listens on L2CAP PSM 17 (control) and 19 (interrupt) itself
- Reconnects to an already paired host when a key is pressed while disconnected
- Sends reports as: 0xA1, reportId, <same bytes as the USB report>

Requirements (see Initialization/bluetooth/install_bluetooth):
- python3-dbus, python3-gi
- bluetoothd started with "-P input" so it does not own PSM 17/19
- run as root (binding PSM < 0x1001)
"""

import os
import select
import socket
import struct
import threading
import time

# --------------------------------------------------
# Config
# --------------------------------------------------

DEVICE_NAME = "CustomKeyboard"
PSM_CONTROL = 0x11
PSM_INTERRUPT = 0x13
BDADDR_ANY = "00:00:00:00:00:00"

# Discoverable forever when nothing is paired yet, otherwise only this long after start
PAIRING_WINDOW_SECONDS = 120
RECONNECT_RETRY_SECONDS = 5
SEND_TIMEOUT_SECONDS = 1.0

HID_UUID = "00001124-0000-1000-8000-00805f9b34fb"
PROFILE_PATH = "/customkeyboard/hid_profile"
AGENT_PATH = "/customkeyboard/agent"

# Linux socket options for L2CAP link security (require pairing + encryption)
SOL_BLUETOOTH = 274
BT_SECURITY = 4
BT_SECURITY_MEDIUM = 2

# channel -> (report id, report length)
REPORTS = {
    "keyboard": (1, 8),
    "mouse": (2, 5),
    "media": (3, 2),
}

# --------------------------------------------------
# Report descriptor
# Same layouts as Initialization/init_usb_gadget, plus a Report ID per collection.
# Keep these in sync when a USB descriptor changes.
# --------------------------------------------------

REPORT_DESCRIPTOR = bytes([
    # Keyboard, Report ID 1, 8 bytes: [modifiers][reserved][6 keys]
    0x05, 0x01,        # Usage Page (Generic Desktop)
    0x09, 0x06,        # Usage (Keyboard)
    0xA1, 0x01,        # Collection (Application)
    0x85, 0x01,        #   Report ID (1)
    0x05, 0x08,        #   Usage Page (LEDs)
    0x19, 0x01,        #   Usage Minimum (Num Lock)
    0x29, 0x03,        #   Usage Maximum (Scroll Lock)
    0x15, 0x00,        #   Logical Minimum (0)
    0x25, 0x01,        #   Logical Maximum (1)
    0x75, 0x01,        #   Report Size (1)
    0x95, 0x03,        #   Report Count (3)
    0x91, 0x02,        #   Output (Data,Var,Abs)
    0x09, 0x4B,        #   Usage (Generic Indicator)
    0x95, 0x01,        #   Report Count (1)
    0x91, 0x02,        #   Output (Data,Var,Abs)
    0x95, 0x04,        #   Report Count (4)
    0x91, 0x01,        #   Output (Const)
    0x05, 0x07,        #   Usage Page (Keyboard/Keypad)
    0x19, 0xE0,        #   Usage Minimum (0xE0)
    0x29, 0xE7,        #   Usage Maximum (0xE7)
    0x95, 0x08,        #   Report Count (8)
    0x81, 0x02,        #   Input (Data,Var,Abs)  modifiers
    0x75, 0x08,        #   Report Size (8)
    0x95, 0x01,        #   Report Count (1)
    0x81, 0x01,        #   Input (Const)  reserved
    0x19, 0x00,        #   Usage Minimum (0x00)
    0x29, 0x91,        #   Usage Maximum (0x91)
    0x26, 0xFF, 0x00,  #   Logical Maximum (255)
    0x95, 0x06,        #   Report Count (6)
    0x81, 0x00,        #   Input (Data,Array,Abs)  keys
    0xC0,              # End Collection

    # Relative mouse, Report ID 2, 5 bytes: [buttons][x][y][wheel][pan]
    0x05, 0x01,        # Usage Page (Generic Desktop)
    0x09, 0x02,        # Usage (Mouse)
    0xA1, 0x01,        # Collection (Application)
    0x85, 0x02,        #   Report ID (2)
    0x05, 0x09,        #   Usage Page (Button)
    0x19, 0x01,        #   Usage Minimum (Button 1)
    0x29, 0x08,        #   Usage Maximum (Button 8)
    0x15, 0x00,        #   Logical Minimum (0)
    0x25, 0x01,        #   Logical Maximum (1)
    0x95, 0x08,        #   Report Count (8)
    0x75, 0x01,        #   Report Size (1)
    0x81, 0x02,        #   Input (Data,Var,Abs)
    0x05, 0x01,        #   Usage Page (Generic Desktop)
    0x09, 0x30,        #   Usage (X)
    0x09, 0x31,        #   Usage (Y)
    0x15, 0x81,        #   Logical Minimum (-127)
    0x25, 0x7F,        #   Logical Maximum (127)
    0x75, 0x08,        #   Report Size (8)
    0x95, 0x02,        #   Report Count (2)
    0x81, 0x06,        #   Input (Data,Var,Rel)
    0x09, 0x38,        #   Usage (Wheel)
    0x15, 0x81,        #   Logical Minimum (-127)
    0x25, 0x7F,        #   Logical Maximum (127)
    0x75, 0x08,        #   Report Size (8)
    0x95, 0x01,        #   Report Count (1)
    0x81, 0x06,        #   Input (Data,Var,Rel)
    0x05, 0x0C,        #   Usage Page (Consumer)
    0x0A, 0x38, 0x02,  #   Usage (AC Pan)
    0x15, 0x81,        #   Logical Minimum (-127)
    0x25, 0x7F,        #   Logical Maximum (127)
    0x75, 0x08,        #   Report Size (8)
    0x95, 0x01,        #   Report Count (1)
    0x81, 0x06,        #   Input (Data,Var,Rel)
    0xC0,              # End Collection

    # Media / consumer control, Report ID 3, 2 bytes: bit mask (see media_keys.py) + padding
    0x05, 0x0C,        # Usage Page (Consumer)
    0x09, 0x01,        # Usage (Consumer Control)
    0xA1, 0x01,        # Collection (Application)
    0x85, 0x03,        #   Report ID (3)
    0x15, 0x00,        #   Logical Minimum (0)
    0x25, 0x01,        #   Logical Maximum (1)
    0x75, 0x01,        #   Report Size (1)
    0x95, 0x08,        #   Report Count (8)
    0x09, 0xE9,        #   Usage (Volume Up)        bit 0
    0x09, 0xEA,        #   Usage (Volume Down)      bit 1
    0x09, 0xE2,        #   Usage (Mute)             bit 2
    0x09, 0xB0,        #   Usage (Play)             bit 3
    0x09, 0xB1,        #   Usage (Pause)            bit 4
    0x09, 0xB5,        #   Usage (Next Track)       bit 5
    0x09, 0xB6,        #   Usage (Previous Track)   bit 6
    0x09, 0xB7,        #   Usage (Stop)             bit 7
    0x81, 0x02,        #   Input (Data,Var,Abs)
    0x95, 0x08,        #   Report Count (8)
    0x81, 0x01,        #   Input (Const)  padding byte
    0xC0,              # End Collection
])


def BuildSdpRecord():
    descriptorHex = REPORT_DESCRIPTOR.hex()
    return f"""<?xml version="1.0" encoding="UTF-8" ?>
<record>
  <attribute id="0x0001"><sequence><uuid value="0x1124" /></sequence></attribute>
  <attribute id="0x0004">
    <sequence>
      <sequence><uuid value="0x0100" /><uint16 value="0x{PSM_CONTROL:04x}" /></sequence>
      <sequence><uuid value="0x0011" /></sequence>
    </sequence>
  </attribute>
  <attribute id="0x0005"><sequence><uuid value="0x1002" /></sequence></attribute>
  <attribute id="0x0006">
    <sequence><uint16 value="0x656e" /><uint16 value="0x006a" /><uint16 value="0x0100" /></sequence>
  </attribute>
  <attribute id="0x0009">
    <sequence><sequence><uuid value="0x1124" /><uint16 value="0x0101" /></sequence></sequence>
  </attribute>
  <attribute id="0x000d">
    <sequence>
      <sequence>
        <sequence><uuid value="0x0100" /><uint16 value="0x{PSM_INTERRUPT:04x}" /></sequence>
        <sequence><uuid value="0x0011" /></sequence>
      </sequence>
    </sequence>
  </attribute>
  <attribute id="0x0100"><text value="{DEVICE_NAME}" /></attribute>
  <attribute id="0x0101"><text value="Raspberry Pi keyboard, mouse and media keys" /></attribute>
  <attribute id="0x0102"><text value="CustomKeyboard" /></attribute>
  <attribute id="0x0200"><uint16 value="0x0100" /></attribute>
  <attribute id="0x0201"><uint16 value="0x0111" /></attribute>
  <attribute id="0x0202"><uint8 value="0xc0" /></attribute>
  <attribute id="0x0203"><uint8 value="0x00" /></attribute>
  <attribute id="0x0204"><boolean value="true" /></attribute>
  <attribute id="0x0205"><boolean value="true" /></attribute>
  <attribute id="0x0206">
    <sequence><sequence><uint8 value="0x22" /><text encoding="hex" value="{descriptorHex}" /></sequence></sequence>
  </attribute>
  <attribute id="0x0207">
    <sequence><sequence><uint16 value="0x0409" /><uint16 value="0x0100" /></sequence></sequence>
  </attribute>
  <attribute id="0x020b"><uint16 value="0x0100" /></attribute>
  <attribute id="0x020c"><uint16 value="0x0c80" /></attribute>
  <attribute id="0x020d"><boolean value="true" /></attribute>
  <attribute id="0x020e"><boolean value="false" /></attribute>
  <attribute id="0x020f"><uint16 value="0x0640" /></attribute>
  <attribute id="0x0210"><uint16 value="0x0320" /></attribute>
</record>
"""


# --------------------------------------------------
# BlueZ D-Bus objects
# --------------------------------------------------

def _MakeDbusObjects(dbus, dbusService):

    class HidProfile(dbusService.Object):
        """Only publishes the SDP record; connections are accepted on our own sockets."""

        @dbusService.method("org.bluez.Profile1", in_signature="", out_signature="")
        def Release(self):
            pass

        @dbusService.method("org.bluez.Profile1", in_signature="oha{sv}", out_signature="")
        def NewConnection(self, device, fd, properties):
            os.close(fd.take())

        @dbusService.method("org.bluez.Profile1", in_signature="o", out_signature="")
        def RequestDisconnection(self, device):
            pass

    class JustWorksAgent(dbusService.Object):
        """Accepts every pairing request and marks the host as trusted."""

        def __init__(self, bus, path):
            super().__init__(bus, path)
            self.bus = bus

        def _Trust(self, devicePath):
            try:
                props = dbus.Interface(self.bus.get_object("org.bluez", devicePath),
                                       "org.freedesktop.DBus.Properties")
                props.Set("org.bluez.Device1", "Trusted", dbus.Boolean(True))
                print(f"[BT] Paired and trusted {devicePath}")
            except dbus.DBusException as error:
                print(f"[BT] Could not trust {devicePath}: {error}")

        @dbusService.method("org.bluez.Agent1", in_signature="", out_signature="")
        def Release(self):
            pass

        @dbusService.method("org.bluez.Agent1", in_signature="o", out_signature="s")
        def RequestPinCode(self, device):
            self._Trust(device)
            return "0000"

        @dbusService.method("org.bluez.Agent1", in_signature="o", out_signature="u")
        def RequestPasskey(self, device):
            self._Trust(device)
            return dbus.UInt32(0)

        @dbusService.method("org.bluez.Agent1", in_signature="ouq", out_signature="")
        def DisplayPasskey(self, device, passkey, entered):
            print(f"[BT] Passkey for {device}: {passkey:06d}")

        @dbusService.method("org.bluez.Agent1", in_signature="os", out_signature="")
        def DisplayPinCode(self, device, pincode):
            print(f"[BT] PIN for {device}: {pincode}")

        @dbusService.method("org.bluez.Agent1", in_signature="ou", out_signature="")
        def RequestConfirmation(self, device, passkey):
            self._Trust(device)

        @dbusService.method("org.bluez.Agent1", in_signature="o", out_signature="")
        def RequestAuthorization(self, device):
            self._Trust(device)

        @dbusService.method("org.bluez.Agent1", in_signature="os", out_signature="")
        def AuthorizeService(self, device, uuid):
            pass

        @dbusService.method("org.bluez.Agent1", in_signature="", out_signature="")
        def Cancel(self):
            pass

    return HidProfile, JustWorksAgent


# --------------------------------------------------
# Bluetooth HID device
# --------------------------------------------------

class BluetoothHid:

    def __init__(self):
        self.lock = threading.Lock()
        self.ctrl = None
        self.intr = None
        self.hostAddress = None
        self.wantReconnect = threading.Event()
        self.lastReconnectTry = 0.0
        self.warnedNoHost = False
        self.started = False
        self.adapterAddress = None
        self.bus = None

    # ---------------- Setup ----------------

    def Start(self):
        if self.started:
            return
        if os.geteuid() != 0:
            raise RuntimeError("Bluetooth mode must run as root: sudo python3 main.py --transport bluetooth")

        try:
            import dbus
            import dbus.service
            import dbus.mainloop.glib
            from gi.repository import GLib
        except ImportError as error:
            raise RuntimeError(
                f"Missing Bluetooth dependency ({error}). "
                "Run: sudo Initialization/bluetooth/install_bluetooth"
            ) from error

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.dbus = dbus

        adapterPath, adapterProps, pairedHosts = self._FindAdapter()
        self.adapterAddress = str(adapterProps["Address"])
        self.pairedHosts = pairedHosts

        # Listen before publishing the record so an incoming host always finds us
        self.ctrlListen = self._Listen(PSM_CONTROL)
        self.intrListen = self._Listen(PSM_INTERRUPT)

        HidProfile, JustWorksAgent = _MakeDbusObjects(dbus, dbus.service)
        self.profile = HidProfile(self.bus, PROFILE_PATH)
        self.agent = JustWorksAgent(self.bus, AGENT_PATH)

        bluez = self.bus.get_object("org.bluez", "/org/bluez")
        dbus.Interface(bluez, "org.bluez.ProfileManager1").RegisterProfile(
            PROFILE_PATH, HID_UUID, {
                "ServiceRecord": BuildSdpRecord(),
                "Role": "server",
                "RequireAuthentication": False,
                "RequireAuthorization": False,
            })
        agentManager = dbus.Interface(bluez, "org.bluez.AgentManager1")
        agentManager.RegisterAgent(AGENT_PATH, "NoInputNoOutput")
        agentManager.RequestDefaultAgent(AGENT_PATH)

        self._SetupAdapter(adapterPath, adapterProps)

        threading.Thread(target=GLib.MainLoop().run, daemon=True).start()
        threading.Thread(target=self._ConnectionLoop, daemon=True).start()

        if pairedHosts:
            self.wantReconnect.set()
        self.started = True

    def _FindAdapter(self):
        dbus = self.dbus
        manager = dbus.Interface(self.bus.get_object("org.bluez", "/"),
                                 "org.freedesktop.DBus.ObjectManager")
        objects = manager.GetManagedObjects()

        adapters = sorted(path for path, ifaces in objects.items() if "org.bluez.Adapter1" in ifaces)
        if not adapters:
            raise RuntimeError("No Bluetooth adapter found (is bluetooth.service running?)")
        adapterPath = adapters[0]

        pairedHosts = [
            str(ifaces["org.bluez.Device1"]["Address"])
            for path, ifaces in objects.items()
            if "org.bluez.Device1" in ifaces
            and ifaces["org.bluez.Device1"].get("Adapter") == adapterPath
            and ifaces["org.bluez.Device1"].get("Paired")
        ]
        return adapterPath, objects[adapterPath]["org.bluez.Adapter1"], pairedHosts

    def _SetupAdapter(self, adapterPath, adapterProps):
        dbus = self.dbus
        props = dbus.Interface(self.bus.get_object("org.bluez", adapterPath),
                               "org.freedesktop.DBus.Properties")
        window = 0 if not self.pairedHosts else PAIRING_WINDOW_SECONDS

        props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(True))
        props.Set("org.bluez.Adapter1", "Alias", dbus.String(DEVICE_NAME))
        props.Set("org.bluez.Adapter1", "PairableTimeout", dbus.UInt32(window))
        props.Set("org.bluez.Adapter1", "Pairable", dbus.Boolean(True))
        props.Set("org.bluez.Adapter1", "DiscoverableTimeout", dbus.UInt32(window))
        props.Set("org.bluez.Adapter1", "Discoverable", dbus.Boolean(True))

        deviceClass = int(adapterProps.get("Class", 0))
        if deviceClass & 0x1FFC != 0x0540:
            print(f"[BT] WARNING: adapter class is 0x{deviceClass:06x}, not a keyboard (0x002540). "
                  "Run Initialization/bluetooth/install_bluetooth so hosts show it as a keyboard.")

        if window:
            print(f"[BT] Discoverable/pairable for {window}s (already paired: {', '.join(self.pairedHosts)})")
        else:
            print("[BT] Discoverable/pairable until a host pairs")

    def _Listen(self, psm):
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(SOL_BLUETOOTH, BT_SECURITY, struct.pack("BB", BT_SECURITY_MEDIUM, 0))
        try:
            sock.bind((BDADDR_ANY, psm))
        except OSError as error:
            sock.close()
            raise RuntimeError(
                f"Cannot bind L2CAP PSM {psm} ({error}). bluetoothd's input plugin probably owns it; "
                "run: sudo Initialization/bluetooth/install_bluetooth"
            ) from error
        sock.listen(1)
        return sock

    # ---------------- Connection handling ----------------

    def _ConnectionLoop(self):
        while True:
            if self.intr is not None:
                self._ServeConnection()
                continue

            readable, _, _ = select.select([self.ctrlListen], [], [], 1.0)
            if readable:
                self._AcceptHost()
            elif self.wantReconnect.is_set() and \
                    time.time() - self.lastReconnectTry >= RECONNECT_RETRY_SECONDS:
                self._ReconnectToPairedHost()

    def _AcceptHost(self):
        ctrl, (address, _) = self.ctrlListen.accept()
        self.intrListen.settimeout(10)
        try:
            intr, _ = self.intrListen.accept()
        except OSError:
            print(f"[BT] {address} opened control channel but not interrupt channel")
            ctrl.close()
            return
        self._SetConnection(ctrl, intr, address)

    def _ReconnectToPairedHost(self):
        self.lastReconnectTry = time.time()
        self.wantReconnect.clear()
        hosts = ([self.hostAddress] if self.hostAddress else []) + \
            [h for h in self._PairedHosts() if h != self.hostAddress]

        for address in hosts:
            print(f"[BT] Reconnecting to {address}...")
            ctrl = intr = None
            try:
                ctrl = self._Connect(address, PSM_CONTROL)
                intr = self._Connect(address, PSM_INTERRUPT)
            except OSError as error:
                print(f"[BT] {address} not reachable ({error})")
                for sock in (ctrl, intr):
                    if sock:
                        sock.close()
                continue
            self._SetConnection(ctrl, intr, address)
            return

    def _PairedHosts(self):
        try:
            return self._FindAdapter()[2]
        except Exception:
            return self.pairedHosts

    def _Connect(self, address, psm):
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
        sock.setsockopt(SOL_BLUETOOTH, BT_SECURITY, struct.pack("BB", BT_SECURITY_MEDIUM, 0))
        sock.settimeout(5)
        sock.connect((address, psm))
        return sock

    def _SetConnection(self, ctrl, intr, address):
        ctrl.settimeout(None)
        intr.settimeout(SEND_TIMEOUT_SECONDS)
        with self.lock:
            self.ctrl, self.intr = ctrl, intr
            self.hostAddress = address
            self.warnedNoHost = False
        print(f"[BT] Connected to host {address}")

    def _Disconnect(self, reason):
        with self.lock:
            if self.intr is None:
                return
            for sock in (self.ctrl, self.intr):
                try:
                    sock.close()
                except OSError:
                    pass
            self.ctrl = self.intr = None
        print(f"[BT] Host disconnected ({reason})")

    def _ServeConnection(self):
        """Answer HIDP control requests until the host goes away."""
        ctrl, intr = self.ctrl, self.intr
        if ctrl is None or intr is None:
            return
        try:
            readable, _, _ = select.select([ctrl, intr], [], [], 1.0)
            for sock in readable:
                data = sock.recv(64)
                if not data:
                    self._Disconnect("link closed")
                    return
                if sock is ctrl:
                    self._HandleControl(data)
                # Interrupt-channel data from the host is LED output reports; ignored
        except (OSError, ValueError) as error:
            self._Disconnect(error)

    def _HandleControl(self, data):
        msgType, param = data[0] >> 4, data[0] & 0x0F
        reply = b"\x03"  # HANDSHAKE: unsupported request

        if msgType == 0x1:  # HID_CONTROL
            if param == 0x5:  # VIRTUAL_CABLE_UNPLUG
                self._Disconnect("virtual cable unplug")
            return
        elif msgType == 0x4:  # GET_REPORT
            reportType = param & 0x3
            reportId = data[1] if len(data) > 1 else 0
            size = next((size for rid, size in REPORTS.values() if rid == reportId), None)
            if reportType == 0x1 and size:
                reply = bytes([0xA1, reportId]) + bytes(size)
            else:
                reply = b"\x02"  # HANDSHAKE: invalid report id
        elif msgType in (0x5, 0x7, 0x9):  # SET_REPORT, SET_PROTOCOL, SET_IDLE
            reply = b"\x00"  # HANDSHAKE: successful
        elif msgType == 0x6:  # GET_PROTOCOL
            reply = b"\xA0\x01"  # report protocol
        elif msgType == 0x8:  # GET_IDLE
            reply = b"\xA0\x00"

        with self.lock:
            if self.ctrl is not None:
                self.ctrl.send(reply)

    # ---------------- Sending ----------------

    def Send(self, channel, report):
        reportId, size = REPORTS[channel]
        with self.lock:
            intr = self.intr
            if intr is None:
                if not self.warnedNoHost:
                    print("[BT] No host connected, dropping key presses (trying to reconnect)")
                    self.warnedNoHost = True
                self.wantReconnect.set()
                return
            try:
                intr.sendall(bytes([0xA1, reportId]) + bytes(report[:size]))
                return
            except TimeoutError:
                print(f"[BT] Send timed out, dropped {channel} report")
                return
            except OSError as error:
                failure = error
        self._Disconnect(failure)
        self.wantReconnect.set()

    def Status(self):
        return {
            "adapter": self.adapterAddress,
            "name": DEVICE_NAME,
            "host": self.hostAddress if self.intr is not None else None,
        }


_device = BluetoothHid()


def start():
    _device.Start()
    return _device.Status()


def send(channel, report):
    _device.Send(channel, report)
