from p2p import P2P
import pickle
import json
import threading
from wallet import Wallet
from blockchain import Blockchain
from commands import process_command

class Node:
    # Class that represents the each node of the cluster    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.wallet = Wallet()
        self.p2p = P2P(self.ip, self.port, self.wallet)
        self.p2p.p2p_network_init()
        self.wallet.set_peers(self.p2p.peers, self.p2p.nodes)
        self.wallet.set_blockchain(self.p2p.blockchain)
        # self.wallet.set_blockchain(self.p2p.blockchain)
        self.p2p.set_wallet(self.wallet)

        # Start Blockchaining
        self.blockchaining()

    def command_reading(self):
        print(f"Ready and awaiting user commands.")
        while True:
            # Read command from the command line
            command = input("> ")
            if len(command.strip()) != 0:
                arguments = process_command(command)
                arguments = json.loads(arguments)

                # Given the user id find its public key from your dictionary
                receiver_address = self.p2p.peers[arguments["receiver"]]["public_key"]

                transaction_to_send = self.wallet.create_transaction(
                                                    receiver_address,
                                                    arguments["type"], 
                                                    arguments.get("amount", 0),  # Use default value if "amount" key is not present
                                                    arguments.get("message", "")  # Use default value if "data" key is not present
                                                )
                
                self.wallet.broadcast_transaction(transaction_to_send)

                if self.wallet.transaction_pool.validation_required():
                    self.wallet.mint_block()

    def blockchaining(self):

        if self.p2p.id == 'id0':
            self.wallet.initial_distribution()

        # Command Reading Thread
        print(self.p2p.peers)
        command_reading_thread = threading.Thread(target=self.command_reading)
        command_reading_thread.start()
                