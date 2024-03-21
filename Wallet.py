from Crypto.PublicKey import RSA    # pycryptodome
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Transaction import Transaction
import json

class Wallet:

    def __init__(self):
        self.generate_wallet()
        self.nonce = 0
    
    def generate_wallet(self):
        key = RSA.generate(2048)
        self.private_key = key.export_key().decode('utf-8')
        self.public_key = key.publickey().export_key().decode('utf-8')
    
    def sign_transaction(self, transaction_data):
        private_key_obj = RSA.import_key(self.private_key)
        transaction_data = json.dumps(transaction_data).encode('utf-8')
        hash_data = SHA256.new(transaction_data)        # transaction_data.encode('utf-8')
        signature = pkcs1_15.new(private_key_obj).sign(hash_data)
        return signature
    
    def verify_transaction(self, public_key, transaction_data, signature):
        hash_data = SHA256.new(transaction_data)        # transaction_data.encode('utf-8')
        try:
            pkcs1_15.new(public_key).verify(hash_data, signature)
            return True
        except (ValueError, TypeError):
            return False
    ## https://www.pycryptodome.org/src/signature/pkcs1_v1_5
        

    def create_transaction(self, receiver_address, type, amount, message):
        transaction = Transaction(type, receiver_address, self.public_key, amount, message, self.nonce)
        signature = self.sign_transaction(transaction.payload())
        transaction.transaction_signing(signature)
        self.nonce += 1
        return transaction

    # def createBlock(self, transactions, lastHash, blockCount):
    #     block = Block(transactions, lastHash,
    #                     self.publicKeyString(), blockCount)
    #     signature = self.sign(block.payload())
    #     block.sign(signature)
    #     return block

