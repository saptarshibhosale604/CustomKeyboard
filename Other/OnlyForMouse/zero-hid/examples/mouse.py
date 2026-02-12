from zero_hid import Mouse

print("Init")

with Mouse() as m:
    for i in range(50):
        print(f"moving mouse: i {i}")
        m.move(5, 5)
