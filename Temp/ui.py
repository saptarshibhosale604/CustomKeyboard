import threading
import time
import mouseManager02

#
# def counter_loop():
#     count = 1
#     while True:
#         print(f"[Counter Thread] Count: {count}")
#         count += 1
#         time.sleep(2)
#

def main():
    # Main thread work
    # print("“Discipline is choosing between what you want now and what you want most.”")
    #
    # # Start independent loop in another thread
    # counter_thread = threading.Thread(
    #     target=counter_loop,
    #     daemon=True  # exits automatically when main thread exits
    # )
    # counter_thread.start()
    #
    # Keep main thread alive (optional but useful)
    print("Enter movement command: up, down, left, right, stop")
    print("Type 'exit' to quit\n")

    while True:
        command = input("Command: ").strip().lower()
        mouseManager02.Main(command)
        time.sleep(1)


if __name__ == "__main__":
    main()

