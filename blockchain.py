"""For creating and managing a linked list of chain"""

from block import Block
from utils import BlockChainUtils
from transaction import Transaction
from config import N


class Blockchain:
    """For creating and managing a linked list of chain"""

    def __init__(self, bootstrap_public_key):
        self.chain = [Block.genesis()]
        self.chain[0].transactions.append(self.create_genesis_transaction(bootstrap_public_key))

    def create_genesis_transaction(self, bootstrap_public_key):
        """Creates the genesis transaction"""
        genesis_transaction = Transaction(
            sender_address="0",
            receiver_address=bootstrap_public_key,
            amount=1000 * N,
            nonce=0,
            message="",
            type="Exchange",
        )
        return genesis_transaction

    def add_block(self, block:Block):
        """Adds a block to the blockchain and executes the transactions in the block"""
        total_fees = block.sum_fees()
        self.chain.append(block)
        print(len(self.chain))
        return total_fees
    
    def get_prevhash(self):
        """Returns the hash of the last block in the blockchain"""
        last_block = self.chain[-1]
        return last_block.current_hash
    
    def next_index(self):
        return len(self.chain)