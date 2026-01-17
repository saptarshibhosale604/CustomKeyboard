"""
piLevelFunctions.py

Contains low-level Raspberry Pi power control functions.
"""

import os


def PiShutdown():
    """
    Safely shut down the Raspberry Pi.
    """
    try:
        print("Shutting down Raspberry Pi...")
        os.system("sudo shutdown now")
    except Exception as error:
        print(f"Error during shutdown: {error}")


def PiReboot():
    """
    Safely restart the Raspberry Pi.
    """
    try:
        print("Restarting Raspberry Pi...")
        os.system("sudo reboot now")
    except Exception as error:
        print(f"Error during restart: {error}")

