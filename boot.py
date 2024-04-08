import sys
import threading
from queue import Queue
from main import main
import time

def read_input_and_dispatch(file_paths, queues, stop_event):
    time.sleep(5)
    for thread_id, file_path in enumerate(file_paths):
        try:
            with open(file_path, "r") as file:
                for line in file:
                    parts = line.strip().split(" ", 1)
                    if parts[0].startswith("id"):
                        message = f"m {parts[0]} {parts[1]}"  # Adjusted to 'id m message' format
                        queues[thread_id].put(message)
                    else:
                        print(f"Invalid format in file {file_path}: {line.strip()}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            continue
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            continue

if __name__ == '__main__':
    ip = sys.argv[1]
    base_port = int(sys.argv[2])

    # Number of nodes
    N = 5

    # Create queues for each thread to handle its input
    queues = [Queue() for _ in range(N)]
    # Event to signal threads to exit
    stop_event = threading.Event()

    # Define file paths for each thread
    file_paths = [f"./inputs/input5/trans{i}.txt" for i in range(N)]

    # Start the bootstrap node first
    bootstrap_thread = threading.Thread(target=main, args=(ip, base_port, queues[0], stop_event))
    bootstrap_thread.daemon = True
    bootstrap_thread.start()

    # Give some time for the bootstrap node to start
    time.sleep(1)

    # Start a separate thread to read input and dispatch to appropriate threads
    input_thread = threading.Thread(target=read_input_and_dispatch, args=(file_paths, queues, stop_event))
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
