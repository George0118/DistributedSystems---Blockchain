from p2p import P2P
import pickle
from queue import Queue
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
        self.p2p = P2P(self.ip, self.port, self.wallet)
        self.p2p.p2p_network_init()
        self.wallet.set_peers(self.p2p.peers, self.p2p.nodes)
        self.wallet.set_blockchain(self.p2p.blockchain)
        # self.wallet.set_blockchain(self.p2p.blockchain)
        self.p2p.set_wallet(self.wallet)

        # Start Blockchaining
        self.blockchaining()

    def command_reading(self,):
        print(f"{self.p2p.id}: Ready and awaiting user commands.")
        while True:
            # Read command from the command line
            try:
                command = input("> ")
                if len(command.strip()) != 0:
                    if command == "view":
                        last_block_transactions, last_validator_id = self.wallet.view_block()
                        print("{self.p2p.id}: Last validated block's transactions:")
                        for transaction in last_block_transactions:
                            print(transaction)
                        print("With validator (by id):", last_validator_id)

                    elif command == "balance":
                        balance, stake = self.wallet.my_balance()
                        print(f"{self.p2p.id}: My balance is:", balance, "BCCs and my stake is:", stake)

                    elif command == "help":
                        print("{self.p2p.id}: Acceptable commands:")
                        print("t <number>: Perform a transaction with the specified amount")
                        print("m <text>: Send a message with the provided text")
                        print("stake <number>: Stake the specified amount")
                        print("view: View the last validated block's transactions and validator")
                        print("balance: View your current balance (up to the last validated block)")
                    else:
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

    def blockchaining(self):

        if self.p2p.id == 'id0':
            self.wallet.initial_distribution()

        # Command Reading Thread
        command_reading_thread = threading.Thread(target=self.command_reading, args=())
        command_reading_thread.start()
        command_reading_thread.join()
                