import sys
import threading
from node import Node


if __name__ == '__main__':
    ip = sys.argv[1]
    base_port = int(sys.argv[2])
    N = int(sys.argv[3])
    CAPACITY = int(sys.argv[4])

    # Event to signal threads to exit
    stop_event = threading.Event()

    node = Node(ip, base_port, stop_event)

