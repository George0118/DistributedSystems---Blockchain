import sys
import threading
from queue import Queue
from node import Node
import time
from config import N


if __name__ == '__main__':
    ip = sys.argv[1]
    base_port = int(sys.argv[2])

    # Event to signal threads to exit
    stop_event = threading.Event()

    node = Node(ip, base_port, stop_event)




    # # Start the bootstrap node first
    # bootstrap_thread = threading.Thread(target=main, args=(ip, base_port, stop_event, queue))
    # bootstrap_thread.start()

    # # Give some time for the bootstrap node to start
    # time.sleep(1)

    # threads = [bootstrap_thread]
    # for i in range(1, N):
    #     t = threading.Thread(target=main, args=(ip, base_port+i, stop_event, queues[i]))
    #     threads.append(t)
    #     t.start()

    # # Wait for all threads to finish
    # for t in threads:
    #     t.join()

    # # Ensure the input thread terminates
    # input_thread.join()
