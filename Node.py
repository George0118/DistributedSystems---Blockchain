from P2P import P2P
from Wallet import Wallet
from Blockchain import Blockchain

class Node:
    # Class that represents the each node of the cluster    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.blockchain = Blockchain()

        self.p2p = P2P(self.ip, self.port)

    ### Other defs