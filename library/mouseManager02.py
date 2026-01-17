"""
main.py

Terminal-based mouse controller using keyboard input.
No external libraries required.

Key mappings:
- Hold 'h' -> move right
- Hold 'l' -> move left
- Hold 'j' -> move down
- Hold 'd' -> move up
- Press 'u' -> left click
- Press 'i' -> right click
- Press 'p' -> quit program
"""

import sys
import termios
import tty
import select
from time import sleep
from zero_hid import Mouse

# =========================
# Configuration
# =========================

# moveStep = 8
moveStep = 2
loopDelay = 0.01
maxDelta = 127


# =========================
# Terminal Helpers
# =========================

# def SetRawMode():
#     """
#     Set terminal to raw mode for instant key reading.
#     """
#     fd = sys.stdin.fileno()
#     oldSettings = termios.tcgetattr(fd)
#     tty.setraw(fd)
#     return oldSettings
#

# def RestoreTerminal(oldSettings):
#     """
#     Restore terminal to original settings.
#     """
#     termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, oldSettings)


def ReadKey():
    """
    Read one key if available (non-blocking).
    """
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None


# =========================
# Mouse Helpers
# =========================

def MoveRelative(mouse, dx, dy):
    """
    Move mouse using HID-safe deltas.
    """
    try:
        while dx != 0 or dy != 0:
            stepX = max(-maxDelta, min(maxDelta, dx))
            stepY = max(-maxDelta, min(maxDelta, dy))

            mouse.move(stepX, stepY)

            dx -= stepX
            dy -= stepY
    except Exception as exc:
        print(f"\n⚠️ Mouse movement error: {exc}")


# =========================
# Info Helpers
# =========================

def PrintStartupInfo():
    """
    Print control instructions.
    """
    print("\n================ Mouse Controller Started ================\n")
    print("\nControls:")
    print("\n  h  -> move right (hold)")
    print("\n  l  -> move left  (hold)")
    print("\n  j  -> move down  (hold)")
    print("\n  d  -> move up    (hold)")
    print("\n  u  -> left click")
    print("\n  i  -> right click")
    print("\n  p  -> quit")
    print("\n==========================================================\n")


# =========================
# Main Logic
# =========================

def MouseMovementLoop():
    """
    Program entry point.
    """
    global movement_up
    global movement_down
    global movement_left
    global movement_right
    global isMouseMovementLoopOn

    # oldTerminalSettings = None
    isMouseMovementLoopOn = True

    try:
        # oldTerminalSettings = SetRawMode()
        PrintStartupInfo()

        with Mouse(absolute=False) as mouse:
            while True:
                # key = ReadKey()

                if movement_left:
                    print("\r➡️  Moving Left   ")
                    MoveRelative(mouse, -moveStep, 0)

                if movement_right:
                    print("\r⬅️  Moving Right    ")
                    MoveRelative(mouse, moveStep, 0)

                if movement_down:
                    print("\r⬇️  Moving Down    ")
                    MoveRelative(mouse, 0, moveStep)

                if movement_up:
                    print("\r⬆️  Moving Up      ")
                    MoveRelative(mouse, 0, -moveStep)

                # elif key == 'u':
                #     print("\r🖱️  Left Click     ")
                #     mouse.left_click()
                #
                # elif key == 'i':
                #     print("\r🖱️  Right Click    ")
                #     mouse.right_click()
                #
                # elif key == 'p':
                #     print("\nQuit key pressed. Exiting...")
                #     break
                #
                sleep(loopDelay)

    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")

    except Exception as exc:
        print(f"\n❌ Fatal error: {exc}")

    finally:
        # if oldTerminalSettings:
            # RestoreTerminal(oldTerminalSettings)
        print("\nMouse Control Stopped")

import threading
import time

# Movement state variables
movement_up = False
movement_down = False
movement_left = False
movement_right = False

isMouseMovementLoopOn = False

def Main():
    global movement_up
    global movement_down
    global movement_left
    global movement_right
    global isMouseMovementLoopOn

    print("Enter movement command: up, down, left, right, stop")
    print("Type 'exit' to quit\n")

    
    print(f"isMouseMovementLoopOn: {isMouseMovementLoopOn}")

    if not isMouseMovementLoopOn:
        # Start independent loop in another thread
        threadMouseMovementLoop = threading.Thread(
            target=MouseMovementLoop,
            daemon=True  # exits automatically when main thread exits
        )
        threadMouseMovementLoop.start()


    while True:
        command = input("Command: ").strip().lower()

        # Reset all movements first
        # movement_up = False
        # movement_down = False
        # movement_left = False
        # movement_right = False

        if command == "k":
            movement_up = True
        elif command == "j":
            movement_down = True
        elif command == "l":
            movement_right = True
        elif command == "h":
             movement_left = True
        elif command == "s":
            movement_up = False
            movement_down = False
            movement_left = False
            movement_right = False
        elif command == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid command")
            continue

        # Debug / status output
        print(
            f"UP={movement_up}, "
            f"DOWN={movement_down}, "
            f"LEFT={movement_left}, "
            f"RIGHT={movement_right}"
        )


if __name__ == "__main__":
    Main()

