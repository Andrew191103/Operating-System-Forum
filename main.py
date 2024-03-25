# Andrew Sebastian Sibuea ID2602169711
# Operating System Forum

import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

# Global variables
buffer = []
lock = threading.Lock()
producer_done = False

# Producer thread function
def producer():
    global buffer, producer_done
    for _ in range(MAX_COUNT):
        number = random.randint(LOWER_NUM, UPPER_NUM)
        lock.acquire()
        buffer.append(number)
        with open("all.txt", "a") as f:
            f.write(str(number) + '\n')
        lock.release()
        print(f"Produced: {number}")
    producer_done = True

# Consumer thread function
def consumer(file_name, parity):
    while not producer_done or buffer:
        lock.acquire()
        if buffer:
            number = buffer.pop()
            if number % 2 == parity:
                with open(file_name, "a") as f:
                    f.write(str(number) + '\n')
                print(f"Consumed {number} and written to {file_name}")
        lock.release()

# Main function
def main():
    producer_thread = threading.Thread(target=producer)
    consumer_thread1 = threading.Thread(target=consumer, args=("odd.txt", 1))
    consumer_thread2 = threading.Thread(target=consumer, args=("even.txt", 0))

    producer_thread.start()
    consumer_thread1.start()
    consumer_thread2.start()

    producer_thread.join()
    consumer_thread1.join()
    consumer_thread2.join()

    print("All threads terminated.")

if __name__ == "__main__":
    main()
