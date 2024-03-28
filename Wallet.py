from Crypto.PublicKey import RSA    # pycryptodome
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Transaction import Transaction
from TranscationPool import TransactionPool
from Message import Message
import json
from BlockChainUtils import BlockChainUtils

class Wallet:

    def __init__(self):
        # self.blockchain = blockchain
        self.generate_wallet()
        self.nonce = 0
        self.transaction_pool = TransactionPool()
    
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
        public_key_obj = RSA.import_key(public_key)
        transaction_data = json.dumps(transaction_data).encode('utf-8')
        hash_data = SHA256.new(transaction_data)        # transaction_data.encode('utf-8')
        try:
            pkcs1_15.new(public_key_obj).verify(hash_data, signature)
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

    def check_transaction(self, transaction:Transaction):
        """
        Checks if transaction is valid and does not already exist - if valid it broadcasts it
        """
        if self.validate_transaction(transaction):
            # If the signature is valid and the transaction is new, it is added to the pool
            self.transaction_pool.add_transaction(transaction)
            message = Message("TRANSACTION", transaction)
            encoded_message = BlockChainUtils.encode(message)
            if self.transaction_pool.validation_required():
                self.mint_block()
            return encoded_message
        else:
            print("Invalid transaction")
            return None
        
    def handle_transaction(self, transaction:Transaction):
        """
        Checks if transaction is valid and does not already exist - if valid it broadcasts it
        """
        if self.validate_transaction(transaction):
            # If the signature is valid and the transaction is new, it is added to the pool
            self.transaction_pool.add_transaction(transaction)
            if self.transaction_pool.validation_required():
                self.mint_block()
        else:
            print("Invalid transaction") 

    def validate_transaction(self, transaction):
        """
        Validates a transaction
        """
        data = transaction.payload()
        signature = transaction.signature
        signer_address = transaction.sender_address

        signature_valid = self.verify_transaction(signer_address, data, signature)  # Check if signature is valid

        transaction_exists = self.transaction_pool.transaction_exists(transaction)  # Checks if transaction already exists in the pool

        # transaction_in_block = self.blockchain.transaction_exists(transaction)
        # transaction_covered = self.blockchain.transaction_covered(transaction)
        if (
            not transaction_exists
            # and not transaction_in_block
            and signature_valid
            # and transaction_covered
        ):
            return True
        return False       

