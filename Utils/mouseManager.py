"""
mouseManager.py

Terminal-based mouse controller using keyboard input.
No external libraries required.

- mouse movement
- mouse click long pressed done
- movement + mouse click long pressed, not working

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
import time
# from time import sleep
# from time import sleep, time
from Utils.HIDMouse import Mouse

mouseRelativeClick = Mouse(absolute=False)
# mouseRelativeMove = Mouse(absolute=False)
mouseRelativeMove = mouseRelativeClick

# =========================
# Configuration
# =========================
moveStepDefault = 10
moveStep = moveStepDefault # Default mouse speed
# mouseSpeedMultiplier = 0 # Default mouse speed
# moveStep = 2
# moveStep = 20
# loopDelay = 0.1
mouseLoopDelay = 0.01
maxDelta = 127
breakMouseLoopTime = 0.2 # Break the mouse loop after this time

scrollStepDefault = 2
scrollStep = scrollStepDefault # Default mouse speed
maxScrollDelta = 100
mouseScrollDelay = 0.2


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
            # stepX = max(0, min(maxDelta, dx))
            # stepY = max(0, min(maxDelta, dy))

            # print(f"MoveRelative::")
            # print(f"stepX: {stepX}")
            # print(f"stepY: {stepY}")
            # time.sleep(3)

            mouse.move(stepX, stepY)

            dx -= stepX
            dy -= stepY
    except Exception as exc:
        print(f"\n⚠️ Mouse movement error: {exc}")


def ScrollRelative(mouse, dx, dy):
    """
    Move mouse using HID-safe deltas.
    """
    try:
        if (dy != 0):
            print("scrolling up/down")
            # mouse.scroll_y(100)
            # while dx != 0 or dy != 0:
            while dy != 0:
                # stepX = max(-maxDelta, min(maxDelta, dx))
                stepY = max(-maxScrollDelta, min(maxScrollDelta, dy))
                # stepX = max(0, min(maxDelta, dx))
                # stepY = max(0, min(maxDelta, dy))

                print(f"ScrollRelative::")
                # print(f"stepX: {stepX}")
                print(f"stepY: {stepY}")
                # time.sleep(3)

                # mouse.move(stepX, stepY)

                mouse.scroll_y(stepY)
                # dx -= stepX
                dy -= stepY

        elif (dx != 0):
            print("scrolling left/right")
            while dx != 0:
                stepX = max(-maxScrollDelta, min(maxScrollDelta, dx))

                print(f"ScrollRelative::")
                print(f"stepX: {stepX}")
                # time.sleep(3)

                mouse.scroll_x(stepX)
                dx -= stepX
        else:
            print("scrolling nowhere")

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

# from time import sleep, time

def MouseMovementLoop():
    """
    Program entry point.
    """
    global movement_up
    global movement_down
    global movement_left
    global movement_right
    global scroll_up
    global scroll_down
    global scroll_left
    global scroll_right
    global isMouseMovementLoopOn

    isMouseMovementLoopOn = True
    lastMouseActionTime = time.time()   # Track last movement timestamp

    try:
        # with Mouse(absolute=False) as mouse_relative:
        if True: # mouseRelativeMove
        # with Mouse(absolute=True) as mouse_relative:
            while True:
                mouseAction = False  # Flag to detect movement in this iteration

                # # Debug / status output
                # print(
                #     f"UP={movement_up}, "
                #     f"DOWN={movement_down}, "
                #     f"LEFT={movement_left}, "
                #     f"RIGHT={movement_right}"
                # )

                # if click_left
                #     # def left_click(self, release=True):
                #     mouse.left_click()
                #     mouseAction = True

                if movement_left:
                    # MoveRelative(mouse_relative, -moveStep, 0)
                    # MoveRelative(mouse_relative, -moveStep, 0)
                    MoveRelative(mouseRelativeMove, -moveStep, 0)
                    mouseAction = True

                if movement_right:
                    # MoveRelative(mouse_relative, moveStep, 0)
                    MoveRelative(mouseRelativeMove, moveStep, 0)
                    mouseAction = True

                if movement_down:
                    # MoveRelative(mouse_relative, 0, moveStep)
                    MoveRelative(mouseRelativeMove, 0, moveStep)
                    mouseAction = True
                    # print("mouse movement down")
                    # ScrollRelative(mouse_relative, 0, moveStep)
                    # mouseAction = True
                    # time.sleep(5)

                if movement_up:
                    # MoveRelative(mouse_relative, 0, -moveStep)
                    MoveRelative(mouseRelativeMove, 0, -moveStep)
                    mouseAction = True


                if scroll_down:
                    # print("mouse movement down")
                    ScrollRelative(mouseRelativeMove, 0, -scrollStep)
                    mouseAction = True
                    time.sleep(mouseScrollDelay)

                if scroll_up:
                    ScrollRelative(mouseRelativeMove, 0, scrollStep)
                    mouseAction = True
                    time.sleep(mouseScrollDelay)

                if scroll_left:
                    # print("mouse movement down")
                    ScrollRelative(mouseRelativeMove, -scrollStep, 0)
                    mouseAction = True
                    time.sleep(mouseScrollDelay)

                if scroll_right:
                    ScrollRelative(mouseRelativeMove, scrollStep, 0)
                    mouseAction = True
                    time.sleep(mouseScrollDelay)

                # Update last movement time if movement occurred
                if mouseAction:
                    lastMouseActionTime = time.time()
                else:
                    # Break if no movement for 2 seconds
                    if time.time() - lastMouseActionTime >= breakMouseLoopTime:
                        if click_left or click_right:
                            print(f"No movement for {breakMouseLoopTime} Seconds. But click is pressed. \n")
                        else:
                            # print(f"\n⏹️ No movement for {breakMouseLoopTime} Seconds. Stopping mouse loop thread.")
                            print(f"No movement for {breakMouseLoopTime} Seconds. Stopping mouse loop thread.\n")
                            break

                time.sleep(mouseLoopDelay)

    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")

    except Exception as exc:
        print(f"\n❌ Fatal error: {exc}")

    finally:
        isMouseMovementLoopOn = False
        # print("\nMouse Control Stopped")

import threading
# import time

# Click state variables
click_left = False
click_right = False

# Movement state variables
movement_up = False
movement_down = False
movement_left = False
movement_right = False

scroll_up = False
scroll_down = False
scroll_left = False
scroll_right = False

isMouseMovementLoopOn = False

def MouseSpeed(mouseSpeed):
    # global mouseSpeedMultiplier
    global moveStep
    global moveStepDefault
    # print(f"mouseSpeed: {mouseSpeed}")

    # Default mouse speed
    if mouseSpeed == 0:
        # mouseSpeedMuliplier = 0
        moveStep = moveStepDefault

    # Available mouse speed
    elif mouseSpeed == 1:
        moveStep = 2
    elif mouseSpeed == 2:
        moveStep = 10
    elif mouseSpeed == 3:
        moveStep = 30
    elif mouseSpeed == 4:
        moveStep = 50

    print(f"moveStep: {moveStep}")

def Main(cmdInput, cmdStatus):

    global click_left
    global click_right

    global movement_up
    global movement_down
    global movement_left
    global movement_right
    
    global scroll_up
    global scroll_down
    global scroll_left
    global scroll_right

    global isMouseMovementLoopOn
    global mouseRelativeClick

    # print("Enter movement command: up, down, left, right, stop")
    # print("Type 'exit' to quit\n")

    
    # print(f"isMouseMovementLoopOn: {isMouseMovementLoopOn}")
    print(f"mouseManager Main:: cmdInput: {cmdInput}:: cmdStatus: {cmdStatus}")

    if not isMouseMovementLoopOn:
        # Start independent loop in another thread
        threadMouseMovementLoop = threading.Thread(
            target=MouseMovementLoop,
            daemon=True  # exits automatically when main thread exits
        )
        threadMouseMovementLoop.start()


    # while True:
    # command = input("command: ").strip().lower()
    if cmdInput.startswith('click'):
        print("inside mouse click")
        if cmdInput == "click_left":
            # print("inside mouse click_left")
            click_left = cmdStatus
            # movement_up = cmdStatus
            # if click_left:
            #     # print("inside mouse click_left true")
            #     mouseAction = True
            #     with Mouse(absolute=False) as mouse_relative:
            # cmdInput#         mouse_relative.left_click()
            print(f"inside mouse click_left: {click_left}, cmdInput: {cmdInput}")
            if click_left:
                # print("inside mouse click_left true")
                mouseAction = True
                
                # with Mouse(absolute=False) as mouse_relative:
                    # mouse_relative.left_click()
                mouseRelativeClick.left_click(release=False)
                print('------ mouse left click starts')
                # time.sleep(5)
                # print('------ mouse click starts after time.sleep')
            else:
                # with Mouse(absolute=False) as mouse_relative:
                    # mouse_relative.left_click()
                mouseRelativeClick.release()
                print('------ mouse left click ends')


        elif cmdInput == "click_right":
            # print("inside mouse click_right")
            click_right = cmdStatus
            # # movement_up = cmdStatus

            if click_right:
                # print("inside mouse click_left true")
                mouseAction = True
                mouseRelativeClick.right_click(release=False)
                print('------ mouse right click starts')
            else:
                mouseRelativeClick.release()
                print('------ mouse right click ends')

            #     # print("inside mouse click_right true")
            #     mouseAction = True
            #     with Mouse(absolute=False) as mouse_relative:
            #         mouse_relative.right_click()

    if cmdInput.startswith('move'):
        if cmdInput == "move_up":
            movement_up = cmdStatus
        elif cmdInput == "move_down":
            movement_down = cmdStatus
        elif cmdInput == "move_left":
             movement_left = cmdStatus
        elif cmdInput == "move_right":
            movement_right = cmdStatus

    if cmdInput.startswith('scroll'):
        if cmdInput == "scroll_up":
            scroll_up = cmdStatus
        elif cmdInput == "scroll_down":
            scroll_down = cmdStatus
        elif cmdInput == "scroll_left":
            scroll_left = cmdStatus
        elif cmdInput == "scroll_right":
            scroll_right = cmdStatus

    if cmdInput == "stop":
        movement_up = False
        movement_down = False
        movement_left = False
        movement_right = False

        scroll_up = False
        scroll_down = False
        scroll_left = False
        scroll_right = False

    # # debug / status output
    # print(
    #     f"up={movement_up}, "
    #     f"down={movement_down}, "
    #     f"left={movement_left}, "
    #     f"right={movement_right}"
    # )

def ClickLeftMouse():  # just of testing
    print("inside ClickLeftMouse")
    # with Mouse(absolute=False) as rel_mouse, Mouse(absolute=True) as abs_mouse:
    with Mouse(absolute=False) as rel_mouse:
        # print("mouse move")
        # abs_mouse.move(5000, 5000)
        print("mouse click right")
        time.sleep(1)
        rel_mouse.right_click()
        time.sleep(1)
        # # abs_mouse.move(3000, 3000)
        # print("mouse move")
        # abs_mouse.move(2000, 2000)
        # abs_mouse.move(20000, 20000)
        # time.sleep(1)
        print("mouse click left")
        time.sleep(1)
        rel_mouse.left_click()

# if __name__ == "__main__":
#     Main()
# ClickLeftMouse()
