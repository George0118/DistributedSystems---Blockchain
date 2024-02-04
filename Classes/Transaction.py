# Transactions

import time
import json
import hashlib
import socket
import pickle

class Transaction:
    def __init__(self, receiver_address, me, amount, message):
        
        self.receiver_address = receiver_address    # Receiver Address

        self.sender_address = me.publicKey          # Sender Address (MyAddress)
        self.signature = None              # Signature (Needs to be signed)
        self.nonce = me.counter                     # Nonce

        self.fee = amount*0.03 + len(message)       # Calculate whole amount
        self.message = message                      # Message (if no message then "")

        self.transaction_id = self.generate_transaction_id      # Based on the characteristics set transaction_id

    def generate_transaction_id(self):

        transaction_data = {
            'receiver': self.receiver_address,
            'sender': self.sender_address,
            'signature': self.signature,
            'nonce': self.nonce,
            'fee': self.fee,
            'message': self.message,
            'timestamp': time.time()
        }

        transaction_data_json = json.dumps(transaction_data, sort_keys=True)

        # Hash the JSON string using SHA-256
        transaction_id = hashlib.sha256(transaction_data_json.encode()).hexdigest()

        return transaction_id
    
    def transaction_signing(self, signature):
        self.signature = signature
    
    def broadcast_transaction(self, communication_info):
        if(self.signature == None):         # Check if Transcation is signed
            print("Transaction not signed! Can't broadcast...\n")
        else:
            for IP_address, Port in communication_info:         # If it is then broadcast to everyone
                self.send_transaction(IP_address, Port) 
            print("Transcation broadcasted successfully\n")

    def send_transaction(self, IP_address, Port):
        try:
            # Create a socket object
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Connect to the server
            client_socket.connect((IP_address, Port))

            # Serialize the transaction using pickle
            serialized_transaction = pickle.dumps(self)

            # Send the serialized transaction
            client_socket.send(serialized_transaction)

        except Exception as e:
            print(f"Error broadcasting transaction: {e}\n")

        finally:
            # Close the socket
            client_socket.close()


    