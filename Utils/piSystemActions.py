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



import socket

def get_hostname():
    return socket.gethostname()

def get_ip():
    try:
        # Gets the primary IP used for internet connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "IP_NOT_FOUND"

def GetSSHCmd():
    print('inside GetSSHCmd')
    hostname = get_hostname()
    ip = get_ip()
    sshCmd = f"ssh {hostname}@{ip}"
    # print(f"ssh {hostname}@{ip}")
    
    print(f"GetSSHCmd sshCmd: {sshCmd}")
    return sshCmd

# if __name__ == "__main__":
#     main()

