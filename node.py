from p2p import P2P
import pickle
from queue import Queue
import json
import threading
from wallet import Wallet
from commands import process_command

class Node:
    # Class that represents the each node of the cluster    
    def __init__(self, ip, port, input_queue: Queue, stop_event):
        self.ip = ip
        self.port = port
        self.wallet = Wallet()
        self.p2p = P2P(self.ip, self.port, self.wallet)
        self.p2p.p2p_network_init(stop_event)
        self.wallet.set_peers(self.p2p.peers, self.p2p.nodes)
        self.wallet.set_blockchain(self.p2p.blockchain)
        # self.wallet.set_blockchain(self.p2p.blockchain)
        self.p2p.set_wallet(self.wallet)

        # Start Blockchaining
        self.blockchaining(input_queue, stop_event)

    def command_reading(self, input_queue: Queue, stop_event):
        print(f"{self.p2p.id}: Ready and awaiting user commands.")
        while not stop_event.is_set():
            # Read command from the command line
            try:
                command = input_queue.get_nowait()
                if len(command.strip()) != 0:
                    arguments = process_command(command)
                    arguments = json.loads(arguments)

                    # Given the user id find its public key from your dictionary
                    if arguments["type"] != "Stake":
                        receiver_address = self.p2p.peers[arguments["receiver"]]["public_key"]
                    else:
                        receiver_address = 0

                    transaction_to_send = self.wallet.create_transaction(
                                                        receiver_address,
                                                        arguments["type"], 
                                                        arguments.get("amount", 0),  # Use default value if "amount" key is not present
                                                        arguments.get("message", "")  # Use default value if "data" key is not present
                                                    )
                    if self.wallet.check_transaction(transaction_to_send) is not None:
                        self.wallet.broadcast_transaction(transaction_to_send)

                    if self.wallet.transaction_pool.validation_required():
                        block = self.wallet.mint_block()
                        if block is not None:
                            self.wallet.broadcast_block(block)
            except Exception:
                pass  # Queue is empty

    def blockchaining(self, input_queue, stop_event):

        if self.p2p.id == 'id0':
            self.wallet.initial_distribution()

        # Command Reading Thread
        command_reading_thread = threading.Thread(target=self.command_reading, args=(input_queue, stop_event,))
        command_reading_thread.start()
        command_reading_thread.join()
                