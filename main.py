import sys
from node import Node

if __name__ == '__main__':

    ip = sys.argv[1]
    port = int(sys.argv[2])
    # apiPort = int(sys.argv[3])

    node = Node(ip, port)

    # node.startAPI(apiPort)