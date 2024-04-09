import sys
from node import Node
from queue import Queue
import threading

if __name__ == '__main__':
    ip = sys.argv[1]
    port = int(sys.argv[2])

    stop_event = threading.Event()
    
    node = Node(ip, port, stop_event)
