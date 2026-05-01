# from zero_hid import Mouse
import mouse
from time import sleep

print("init")

sleep(1)

with Mouse() as m:
    print("going up")
    m.scroll_y(50)
    sleep(1)
    print("going down")
    m.scroll_x(50)
