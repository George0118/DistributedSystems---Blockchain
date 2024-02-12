"""Broadcasts known connections and checks if new connections, with new nodes, are available"""

import threading
from Classes.Message import Message
from blockchain_utils import BlockChainUtils


class PeerDiscoveryHandler:
    """Broadcasts known connections and checks if new connections, with new nodes, are available"""

    def __init__(self, node):
        self.socket_communication = node

    def start(self):
        """Starts the status and discovery method in their own thread"""
        #status_thread = threading.Thread(target=self.status, args=())
        #status_thread.start()
        discovery_thread = threading.Thread(target=self.discovery, args=())
        discovery_thread.start()

    def status(self):
        """Broadcasting all the nodes you are connected to"""
        while True:
            print("Current Connections:")
            for peer in self.socket_communication.peers:
                print(
                    str(peer.ip) + ":" + str(peer.port)
                )  # Displays socket of peer (which is the port number added to the IP address)

    def discovery(self):
        """Checking for new nodes by broadcasting a handshake message"""
        while True:
            handshake_message = self.handshake_message()
            self.socket_communication.broadcast(handshake_message)

    def handshake(self, connected_node):
        """Performs a handshake with a connected node"""
        handshake_message = self.handshake_message()
        self.socket_communication.send(connected_node, handshake_message)

    def handshake_message(self):
        """Creates handshake message that contains data of a node's known nodes"""
        own_connector = self.socket_communication.socket_connector  # Own connector
        own_peers = self.socket_communication.peers  # Own peers
        data = own_peers
        message_type = "DISCOVERY"
        message = Message(own_connector, message_type, data)
        encoded_message = BlockChainUtils.encode(message)
        return encoded_message

    def handle_message(self, message):
        """If not in already, add message sender to peers list and then connect with
        new peers in the message sender's peer list"""
        peers_socket_connector = message.senderConnector  # Socket connector of sender
        peers_peer_list = message.data  # Peer list of sender
        new_peer = True
        for peer in self.socket_communication.peers:
            if peer.equals(peers_socket_connector):
                new_peer = False
        if new_peer:  # If the sender does not exist in your peers list, add them
            self.socket_communication.peers.append(peers_socket_connector)

        for peers_peer in peers_peer_list:
            peers_known = False
            for peer in self.socket_communication.peers:
                if peer.equals(peers_peer):
                    peers_known = True
            if not peers_known and not peers_peer.equals(
                self.socket_communication.socketConnector
            ):  # If a node is not in your peers list (and is not you), connect with it
                self.socket_communication.connect_with_node(
                    peers_peer.ip, peers_peer.port
                )