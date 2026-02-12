from hidpi import Mouse
import time

print("Initialized")

for i in range(20):
    print(f"mouse moving: count: {i}")
    Mouse.move(50, 0)
    # time.sleep(0.03)
    time.sleep(0.3)

