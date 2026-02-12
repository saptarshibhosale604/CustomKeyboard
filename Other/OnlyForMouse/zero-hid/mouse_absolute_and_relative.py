from zero_hid import Mouse
from time import sleep

# Absolute mouse used for positioning. relative mouse used for clicking.
with Mouse(absolute=False) as rel_mouse, Mouse(absolute=True) as abs_mouse:
    print("mouse move")
    abs_mouse.move(5000, 5000)
    sleep(1)
    print("mouse click right")
    rel_mouse.right_click()
    sleep(1)
    # abs_mouse.move(3000, 3000)
    print("mouse move")
    # abs_mouse.move(2000, 2000)
    abs_mouse.move(20000, 20000)
    sleep(1)
    print("mouse click left")
    rel_mouse.left_click()
