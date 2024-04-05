from Crypto.PublicKey import RSA    # pycryptodome
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from transaction import Transaction
from block import Block
from transaction_pool import TransactionPool
from mesasage import Message
import json
from utils import BlockChainUtils
from proof_of_stake import ProofOfStake
from blockchain import Blockchain
from config import N

class Wallet:

    def __init__(self):
        self.generate_wallet()
        self.nonce = 0
        self.transaction_pool = TransactionPool()
        self.pos = ProofOfStake()

    def set_peers(self, peers):
        self.peers = peers
    
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
            self.execute_transaction(transaction)
        else:
            print("Invalid transaction") 

    def validate_transaction(self, transaction:Transaction):
        """
        Validates a transaction
        """
        data = transaction.payload()
        signature = transaction.signature
        signer_address = transaction.sender_address

        signature_valid = self.verify_transaction(signer_address, data, signature)  # Check if signature is valid

        transaction_covered = self.transaction_covered(transaction)
        if (
            signature_valid
            and transaction_covered
        ):
            return True
        return False     
    
    def transaction_covered(self, transaction:Transaction):
        """ Checks whether the sender has enough money to execute this transaction """
        sender_id = None
        for id, dict_id in self.peers.items():
            if dict_id["public_key"] == transaction.sender_address:
                sender_id = id
        current_balance = self.peers[sender_id]["balance"]
        if current_balance >= transaction.amount + transaction.fee:
            return True
        else:
            return False
    
    def execute_transaction(self, transaction:Transaction):
        """ Executes a Transaction saving its changes to the wallets"""
        # If the transaction is Exchange or Initialization then remove from sender balance and add to receiver
        if transaction.type == "Exchange" or transaction.type == "Initialization":      
            receiver_id = None
            sender_id = None
            for id, dict_id in self.peers.items():
                if dict_id["public_key"] == transaction.receiver_address:
                    receiver_id = id
                if dict_id["public_key"] == transaction.sender_address:
                    sender_id = id
            
            self.peers[sender_id]["balance"] -= (transaction.amount + transaction.fee)
            self.peers[receiver_id]["balance"] += transaction.amount

        elif transaction.type == "Stake":       # If the transaction is Stake then remove the money from the balance
            sender_id = None
            for id, dict_id in self.peers.items():
                if dict_id["public_key"] == transaction.sender_address:
                    sender_id = id
            
            self.peers[sender_id]["balance"] -= (transaction.amount - self.peers[sender_id]["stake"])

    def handle_block(self, block:Block, sender):
        """
        Checks if block is valid - if valid it add it to your blockchain
        """
        if self.validate_block(block, sender):
            # If block is valid then execute any transactions that are in the block and not in the pool
            for transaction in block.transactions:
                if transaction not in self.transaction_pool.transactions:
                    self.execute_transaction(transaction)
            self.transaction_pool.remove_from_pool(
                block.transactions
            )
            # And add the block to the blockchain
            self.update_stakes(block)
            self.blockchain.add_block(block)
        else:
            print("Invalid block")   
    
    def validate_block(self, block:Block, pos_validator):
        """
        Validates a block
        """
        validator = block.validator
        block_hash = block.payload()
        index_valid = self.blockchain.index_valid(block)
        last_block_hash_valid = self.blockchain.last_block_hash_valid(block, block_hash)
        if (
            last_block_hash_valid
            and validator == pos_validator
            and index_valid
        ):
            return True
        return False

    def mint_block(self):
        """
        Checks if you are the validator and triggers block creation if necessary
        """
        prev_hash = self.blockchain.get_prevhash()
        validator = self.pos.validator(prev_hash)
        if validator == self.public_key:
            print("I am the validator")
            index = self.blockchain.next_index()
            block = Block(self.transaction_pool.transactions, prev_hash, validator, index)
            self.transaction_pool.remove_from_pool(
                self.transaction_pool.transactions
            )  # Clears transaction pool by removing all transactions added to block
            self.update_stakes(block)
            message = Message("BLOCK", block)
            return message
        else:
            print("I am not the validator")
            return None
        
    def update_stakes(self, block:Block):
        for transaction in block.transactions:
            if transaction.type == "Stake":
                change_id = None
                for id, dict_id in self.peers.items():
                    if dict_id["public_key"] == transaction.sender_address:
                        change_id = id
                self.peers[change_id]["stake"] = transaction.amount


        
        
        

