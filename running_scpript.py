import sys
import threading
from queue import Queue
from main import main
import time
from config import N

def read_input_and_dispatch(queues, stop_event):
    time.sleep(5)
    while not stop_event.is_set():
        user_input = input("Enter command: ").strip()
        if user_input.lower() == "exit":
            stop_event.set()  # Set the stop event to signal threads to exit
            break
        elif user_input:
            try:
                thread_id, command = user_input.split(':')
                thread_id = int(thread_id.strip()[2:])  # Extract thread id from input
                queues[thread_id].put(command.strip())  # Put the command into the appropriate thread's queue
            except ValueError:
                print("Invalid input format. Please enter in the format 'idN: command'.")

if __name__ == '__main__':
    ip = sys.argv[1]
    base_port = int(sys.argv[2])

    # Create queues for each thread to handle its input
    queues = [Queue() for _ in range(N)]
    # Event to signal threads to exit
    stop_event = threading.Event()

    # Start a separate thread to read input and dispatch to appropriate threads
    input_thread = threading.Thread(target=read_input_and_dispatch, args=(queues, stop_event))
    input_thread.daemon = True
    input_thread.start()

    threads = []
    for i in range(N):
        t = threading.Thread(target=main, args=(ip, base_port+i, queues[i], stop_event))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Ensure the input thread terminates
    input_thread.join()
