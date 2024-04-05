from p2p import P2P
import pickle
import json
import threading
from wallet import Wallet
from commands import process_command

class Node:
    # Class that represents the each node of the cluster    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.wallet = Wallet()
        self.p2p = P2P(self.ip, self.port, self.wallet.public_key)
        self.p2p.p2p_network_init()
        self.wallet.set_peers(self.p2p.peers)
        # self.wallet.set_blockchain(self.p2p.blockchain)
        self.p2p.set_wallet(self.wallet)

        # Start Blockchaining
        self.blockchaining()

    def broadcast_message(p2p, message):
        for id, socket in p2p.nodes.items():
            if id != p2p.id:
                socket.send(json.dumps(message).encode())

    def command_reading(self):
        print(f"Ready and awaiting user commands.")
        while True:
            # Read command from the command line
            command = input("> ")
            if len(command.strip()) != 0:
                arguments = process_command(command)
                arguments = json.loads(arguments)

                # Given the user id find its public key from your dictionary
                receiver_address = self.p2p.peers[str(arguments["receiver"])]["public_key"]

                transaction_to_send = self.wallet.create_transaction(
                                                    receiver_address,
                                                    arguments["type"], 
                                                    arguments.get("amount", 0),  # Use default value if "amount" key is not present
                                                    arguments.get("message", "")  # Use default value if "data" key is not present
                                                )
                
                message = self.wallet.check_transaction(transaction_to_send)

                if message is not None:
                    message = pickle.dumps(message)
                    for socket in self.p2p.nodes.values():
                        socket.sendall(message)

                if self.wallet.transaction_pool.validation_required():
                    self.wallet.mint_block()

    def blockchaining(self):

        print("My current connections are:")
        for n in self.p2p.nodes.values():
            print(n)

        while self.wallet is None:
            pass

        # Command Reading Thread
        command_reading_thread = threading.Thread(target=self.command_reading)
        command_reading_thread.start()
                