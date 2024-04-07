import sys
from node import Node

def main(ip, port, input_queue, stop_event):
    node = Node(ip, port, input_queue, stop_event)
