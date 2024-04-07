# Transactions

import time
import json
import hashlib

class Transaction:
    def __init__(self, type, receiver_address, sender_address, amount, message, nonce):

        self.type = type                            # Set the Transcation Type (Initialization | Stake | Exchange)
        
        if self.type != "Stake":
            self.receiver_address = receiver_address    # Receiver Address
        else:
            self.receiver_address = 0

        self.sender_address = sender_address        # Sender Address (MyAddress)
        self.signature = None                       # Signature (Needs to be signed)
        self.nonce = nonce                          # Nonce

        if self.type != "Exchange":
            self.fee = 0
            self.message = ""
        else:
            self.fee = amount*0.03 + len(message)       # Calculate the fee
            self.message = message                      # Message (if no message then "")

        self.amount = amount                        # Amount to send

        self.transaction_id = self.generate_transaction_id()      # Based on the characteristics set transaction_id

    def generate_transaction_id(self):

        transaction_data = {
            'type': self.type,
            'receiver': self.receiver_address,
            'sender': self.sender_address,
            'nonce': self.nonce,
            'fee': self.fee,
            'amount': self.amount,
            'message': self.message,
            'timestamp': time.time()
        }

        transaction_data_json = json.dumps(transaction_data, sort_keys=True)

        # Hash the JSON string using SHA-256
        transaction_id = hashlib.sha256(transaction_data_json.encode()).hexdigest()

        return transaction_id
    
    def transaction_signing(self, signature):
        self.signature = signature

    def to_dict(self):
        """
        Convert the transaction to a dictionary, without signature.
        """
        return {
            "sender_address": self.sender_address,
            "receiver_address": self.receiver_address,
            "fee": self.fee,
            "amount": self.amount,
            "message": self.message,
            "type_of_transaction": self.type,
            "nonce": self.nonce,
            "transaction_id": self.transaction_id,
            "signature": self.signature,
        }

    def equals(self, transaction):
        """
        Check if two transactions are equal.
        """
        return self.transaction_id == transaction.transaction_id
        
    def payload(self):
        """
        Generate the payload for the transaction.
        """
        return {
            'type': self.type,
            'receiver': self.receiver_address,
            'sender': self.sender_address,
            'nonce': self.nonce,
            'fee': self.fee,
            'amount': self.amount,
            'message': self.message,
            'transaction_id': self.transaction_id
        }

