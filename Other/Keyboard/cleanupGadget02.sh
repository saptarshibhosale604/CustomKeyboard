#!/bin/bash

set -e

GADGET_BASE="/sys/kernel/config/usb_gadget"

echo "Available USB gadgets:"
ls "$GADGET_BASE"
echo

read -rp "Enter gadget name to delete (e.g. hid_gadget): " GADGET_NAME

GADGET_PATH="$GADGET_BASE/$GADGET_NAME"

if [ ! -d "$GADGET_PATH" ]; then
    echo "❌ Gadget '$GADGET_NAME' does not exist."
    exit 1
fi

echo "⚠️  Cleaning up gadget: $GADGET_NAME"
echo

cd "$GADGET_PATH"

# --------------------------------------------------
# 1. Unbind UDC
# --------------------------------------------------
if [ -f UDC ] && [ -n "$(cat UDC)" ]; then
    echo "🔌 Unbinding from UDC: $(cat UDC)"
    echo "" > UDC
fi

# --------------------------------------------------
# 2. Remove function symlinks from configs
# --------------------------------------------------
if [ -d configs ]; then
    for cfg in configs/*; do
        [ -d "$cfg" ] || continue
        echo "🧹 Cleaning config: $cfg"

        # Remove only symlinks (functions)
        find "$cfg" -type l -exec rm -f {} +

        # Remove config strings dirs (no file deletion!)
        if [ -d "$cfg/strings" ]; then
            rmdir "$cfg/strings/"* 2>/dev/null || true
            rmdir "$cfg/strings" 2>/dev/null || true
        fi

        rmdir "$cfg" 2>/dev/null || true
    done
fi

# --------------------------------------------------
# 3. Remove functions
# --------------------------------------------------
if [ -d functions ]; then
    for fn in functions/*; do
        [ -d "$fn" ] || continue
        echo "🧹 Removing function: $fn"
        rmdir "$fn"
    done
fi

# --------------------------------------------------
# 4. Remove gadget strings
# --------------------------------------------------
if [ -d strings ]; then
    rmdir strings/* 2>/dev/null || true
    rmdir strings 2>/dev/null || true
fi

# --------------------------------------------------
# 5. Remove os_desc
# --------------------------------------------------
if [ -d os_desc ]; then
    rmdir os_desc 2>/dev/null || true
fi

# --------------------------------------------------
# 6. Remove webusb
# --------------------------------------------------
if [ -d webusb ]; then
    rmdir webusb 2>/dev/null || true
fi

# --------------------------------------------------
# 7. Final gadget removal
# --------------------------------------------------
cd "$GADGET_BASE"
rmdir "$GADGET_NAME"

echo
echo "✅ Gadget '$GADGET_NAME' fully removed."
echo "🧪 Verify:"
echo "   ls /sys/kernel/config/usb_gadget/"
echo "   ls /dev/hidg*"

