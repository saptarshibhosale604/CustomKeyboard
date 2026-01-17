############## V02 ##############
You are an expert Python developer. Write a complete, production-ready Python script for the following task.

## Task
Create a python script for mouse movement


## Detail
- you will be provided with a main.py file the file is for basic mouse movement using keyboard input.
- your job is to convert that file into a constantly updating mouse movement script.
- if i hold `h` key then mouse should go to right,
else if i hold `j` key then mouse should go down,
else if i hold `d` key then mouse should go up,
else if i hold `l` key then mouse should go left,
- and if i press `u` then press left key
else if i press `i` then press right key

## File
main.py:

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

## Requirements
- Name of the script main.py
- Make the logic and script very simple
- Handle errors gracefully with try-except blocks
- Include docstrings and comments
- Use PascalCase for Functions
- Use camelCase for Variables
- Only create 1 file, do not create readme file or any other file

############## V02 ##############

You are an expert Python developer. Write a complete, production-ready Python script for the following task.

## Task
Create a python script which acts like a Terminal User Interface(TUI)


## Detail


## Requirements
- Name of the script tui.py
- Make the logic and script very simple
- Handle errors gracefully with try-except blocks
- Include docstrings and comments
- Use PascalCase for Functions
- Use camelCase for Variables
- Only create 1 file, do not create readme file or any other file

## Examples
Input: {example_input}
Expected Output:

