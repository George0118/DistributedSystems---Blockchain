import sys
import threading
from main import main
import time
from config import N

if __name__ == '__main__':
    ip = sys.argv[1]
    base_port = int(sys.argv[2])
    
    # Event to signal threads to exit
    stop_event = threading.Event()

    main(ip, base_port, stop_event)