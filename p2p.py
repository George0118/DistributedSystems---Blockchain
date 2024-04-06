import socket
import json
import jsonpickle
import threading
import time
import pickle
from utils import BlockChainUtils
from blockchain import Blockchain
from config import N

# from Wallet import Wallet

# Class for the bootstrapping and "node-discovery" (represents all nodes' process, including bootstrap's)
class P2P:
    def __init__(self, ip, port, wallet):
        self.ip = ip
        self.port = port
        self.public_key = wallet.public_key
        self.peers = None     # Dictionary of peers' id: {'ip': ip, 'port': port, 'public_key': public_key, 'balance': balance, 'stake': stake}
        self.nodes = {}       # Dictionary of nodes' id: sending_socket}
        self.bootstrap_node = ("127.0.0.1", 40000)
        self.cluster_size = N
        self.wallet = wallet

        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
        self.listening_socket.bind((self.ip, self.port))

    def set_wallet(self, wallet):
        self.wallet = wallet

    def start_listening(self):
        self.listening_socket.listen(10)
        while True:
            peer_listening_socket, client_address = self.listening_socket.accept()
            data = peer_listening_socket.recv(1024).decode()
            peer_id = json.loads(data)
            threading.Thread(target=self.handle_connection, args=(peer_listening_socket,peer_id,)).start()
    
    def handle_connection(self, peer_socket, peer_id):
        while True:
            # Receive data from the client
            data = peer_socket.recv(4096)
            # Unpickle the received data
            message = pickle.loads(data)
            if message:
                decoded_message = BlockChainUtils.decode(message)
                if decoded_message.message_type == "TRANSACTION":
                    self.wallet.handle_transaction(decoded_message.data)
                elif decoded_message.message_type == "BLOCK":
                    self.wallet.handle_block(decoded_message.data, peer_id)
                else:
                    self.wallet.handle_blockchain(decoded_message.data, peer_id)


    def connect_to_all_peers(self):
        for peer_id, peer_info in self.peers.items():
            if peer_id != self.id:
                peer_ip = peer_info['ip']
                peer_port = peer_info['port']
                print(f"Attempting to connect to peer {peer_id} at {peer_ip}:{peer_port}...")
                try:
                    peer_send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    peer_send_socket.connect((peer_ip, peer_port))
                    peer_send_socket.send(json.dumps(self.id).encode())
                    self.nodes[peer_id] = peer_send_socket
                    print(f"Successfully connected to peer {peer_id}.")
                except ConnectionRefusedError:
                    print(f"Connection to peer {peer_id} at {peer_ip}:{peer_port} refused.")
                except Exception as e:
                    print(f"Error connecting to peer {peer_id}: {e}")

            if ((self.id, self.port) == self.bootstrap_node):
                # MAKE AND SEND TRANSATION
                pass
            else:
                while True:
                    if (self.peers[self.id]['balance'] < 1000):
                        break


    def connect_to_bootstrap_node(self, bootstrap_ip, bootstrap_port):
        bootstrap_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bootstrap_socket.connect((bootstrap_ip, bootstrap_port))

        # Receive my ID and Blockchain-so-far (only Genesis Block)
        id_blockchain_json = bootstrap_socket.recv(4096).decode()
        id_blockchain = json.loads(id_blockchain_json)
        self.id = id_blockchain['id']
        self.blockchain = jsonpickle.decode(id_blockchain['blockchain'])

        # Send my info: ip, port and public key
        ip_port_pubkey = {
            'ip': self.ip,
            'port': self.port,
            'public_key': self.public_key
        }
        bootstrap_socket.send(json.dumps(ip_port_pubkey).encode())

        # Receive peers' infos
        peers_info_json = bootstrap_socket.recv(40960).decode()
        # Update self.peers (id, ip, port and public_key)
        self.peers = json.loads(peers_info_json)
        
        bootstrap_socket.close()


    def bootstrap_mode(self):
        self.listening_socket.listen()
        i = 1
        temp_sockets = []
        
        while i < self.cluster_size:
            id = "id" + str(i)
            temp_socket, client_address = self.listening_socket.accept()

            id_blockchain = {
                'id': id,
                'blockchain': jsonpickle.encode(self.blockchain)
            }

            temp_socket.send(json.dumps(id_blockchain).encode())
            
            ip_port_pubkey_json = temp_socket.recv(1024).decode()
            ip_port_pubkey = json.loads(ip_port_pubkey_json)
            ip = ip_port_pubkey['ip']
            port = ip_port_pubkey['port']
            public_key = ip_port_pubkey['public_key']

            self.peers[id] = {'ip': ip, 'port': port, 'public_key': public_key, 'balance': 0, 'stake': 10}

            temp_sockets.append(temp_socket)            
            i += 1
        
        for socket in temp_sockets:
            socket.send(json.dumps(self.peers).encode())


    def p2p_network_init(self):

        # BOOTSTRAP NODE
        if ((self.ip, self.port) == self.bootstrap_node):
            self.id = "id0"
            self.peers = {self.id: {'ip': self.ip, 'port': self.port, 'public_key': self.public_key, 'balance': 0, 'stake': 10}}
            self.blockchain = Blockchain(self.wallet.public_key)
            self.bootstrap_mode()
            threading.Thread(target=self.start_listening).start()
            time.sleep(0.5)
            self.connect_to_all_peers()
            print("End of bootstrapping phase!")
        
        # NON-BOOTSTRAP NODES
        else:
            self.connect_to_bootstrap_node(self.bootstrap_node[0], self.bootstrap_node[1])
            threading.Thread(target=self.start_listening).start()
            time.sleep(0.5)
            self.connect_to_all_peers()
            print("End of bootstrapping phase!")