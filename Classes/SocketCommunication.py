from Classes.SocketConnector import SocketConnector
from p2pnetwork.node import Node
from Classes.PeerDiscoveryHandler import PeerDiscoveryHandler
from Classes.SocketConnector import SocketConnector
from BlockChainUtils import BlockChainUtils
import json

class SocketCommunication(Node):
    """To allow P2P communication with other nodes"""

    def __init__(self, ip, port, node_id):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []  # List of connected nodes
        self.peer_discovery_handler = PeerDiscoveryHandler(self)  # Creates peer discovery handler
        self.socket_connector = SocketConnector(ip, port)
        self.node_id = node_id

    def start_socket_communication(self, node):
        """Uses provided IP and port (which form a socket) to open communication
        with other nodes"""
        self.node = node
        self.start()
        self.peer_discovery_handler.start()

    def broadcast(self, message):
        """Broadcasts message to all connected nodes"""
        self.send_to_nodes(message)

    def node_message(self, node, data):
        """To send a message to a connected node"""
        message = BlockChainUtils.decode(
            json.dumps(data)
        )  # Decodes message back to object
        if message.messageType == "DISCOVERY":
            self.peer_discovery_handler.handle_message(data)
        elif message.messageType == "TRANSACTION":
            transaction = message.data
            self.node.handleTransaction(transaction)
        elif message.messageType == "BLOCK":
            block = message.data
            self.node.broadcast_block(block)
        elif message.messageType == "BLOCKCHAINREQUEST":
            self.node.handleBlockchainRequest(node)
        elif message.messageType == "BLOCKCHAIN":
            blockchain = message.data
            self.node.handleBlockchain(blockchain)
