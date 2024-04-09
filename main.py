import sys
from node import Node

def main(ip, port, stop_event):
    node = Node(ip, port, stop_event)
