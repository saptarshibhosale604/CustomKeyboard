from zero_hid import Mouse
from time import sleep

# Total movement per command
MOVE_STEP = 30
# MOVE_STEP = 100

# HID limit for relative mouse
MAX_DELTA = 127


def move_relative(mouse, dx, dy):
    """
    Split large movements into HID-safe chunks
    """
    while dx != 0 or dy != 0:
        step_x = max(-MAX_DELTA, min(MAX_DELTA, dx))
        step_y = max(-MAX_DELTA, min(MAX_DELTA, dy))

        mouse.move(step_x, step_y)

        dx -= step_x
        dy -= step_y

        sleep(0.005)


def execute_command(command, mouse):
    command = command.lower().strip()

    if command == "up":
        move_relative(mouse, 0, -MOVE_STEP)

    elif command == "down":
        move_relative(mouse, 0, MOVE_STEP)

    elif command == "left":
        move_relative(mouse, -MOVE_STEP, 0)

    elif command == "right":
        move_relative(mouse, MOVE_STEP, 0)

    elif command == "left click":
        mouse.left_click()

    elif command == "right click":
        mouse.right_click()

    elif command in ("exit", "quit"):
        return False

    else:
        print("❌ Invalid command")

    return True


def Main(cmd):
    # print("Mouse Control Started")
    # print("Commands: up, down, left, right, left click, right click")
    # print("Type 'exit' to quit\n")

    with Mouse(absolute=False) as mouse:
        # cmd = input("Enter command: ")
        execute_command(cmd, mouse)

    # with Mouse(absolute=False) as mouse:
    #     while True:
    #         cmd = input("Enter command: ")
    #         if not execute_command(cmd, mouse):
    #             break

    print("Mouse Control Stopped")


if __name__ == "__main__":
    Main('na')

