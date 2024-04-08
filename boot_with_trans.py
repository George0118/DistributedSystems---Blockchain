import sys
import threading
from queue import Queue
from main import main
import time
from config import N

def read_input_and_dispatch(queues, stop_event):
    time.sleep(5)
    while not stop_event.is_set():
        # Assuming filenames are stored in the format "trans{N}.txt" where N is the thread ID
        for thread_id, _ in enumerate(queues):
            filepath = f"./inputs/input5/trans{thread_id}.txt"
            try:
                with open(filepath, "r") as file:
                    for line in file:
                        # Parse the line to extract the thread ID and message
                        parts = line.strip().split(" ", 2)
                        if len(parts) == 3:
                            message = f"{parts[1]} {parts[2]}"  # Extract the message part
                            queues[thread_id].put(message.strip())  # Put the command into the appropriate thread's queue
                        else:
                            print(f"Invalid format in file {filepath}: {line.strip()}")
            except FileNotFoundError:
                print(f"File {filepath} not found.")
                continue
            except Exception as e:
                print(f"Error reading file {filepath}: {e}")
                continue




if __name__ == '__main__':
    ip = sys.argv[1]
    base_port = int(sys.argv[2])

    # Create queues for each thread to handle its input
    queues = [Queue() for _ in range(N)]
    # Event to signal threads to exit
    stop_event = threading.Event()

    # Start the bootstrap node first
    bootstrap_thread = threading.Thread(target=main, args=(ip, base_port, queues[0], stop_event))
    bootstrap_thread.daemon = True
    bootstrap_thread.start()

    # Give some time for the bootstrap node to start
    time.sleep(1)

    # Start a separate thread to read input and dispatch to appropriate threads
    input_thread = threading.Thread(target=read_input_and_dispatch, args=(queues, stop_event))
    input_thread.daemon = True
    input_thread.start()

    threads = []
    for i in range(1, N):
        t = threading.Thread(target=main, args=(ip, base_port+i, queues[i], stop_event))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Ensure the input thread terminates
    input_thread.join()

