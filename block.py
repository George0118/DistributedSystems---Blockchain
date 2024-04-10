"""For creating and managing blocks - a container that holds data (including transactions)"""

from config import CAPACITY
import time
from utils import BlockChainUtils


class Block:
    """
    For creating and managing blocks - a container that holds data (including transactions)
    """

    def __init__(self, transactions, previous_hash, validator, index):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.validator = validator  # Public Key of validator
        self.previous_hash = previous_hash
        self.current_hash = self.hash_block()

    @staticmethod
    def genesis():
        """
        Creates first block (as a starting point)
        """
        genesis_block = Block(
            transactions=[], previous_hash="1", validator="0", index=0
        )  # The first transaction will be made in the blockchain class
        genesis_block.timestamp = 0  # This means the timestamp of the genesis block is
        # constant
        return genesis_block

    def to_dict(self):
        """
        Will help display block in readable dictionary form
        """
        data = {}
        data["index"] = self.index
        data["previous_hash"] = self.previous_hash
        data["validator"] = self.validator
        data["timestamp"] = self.timestamp
        data["current_hash"] = self.current_hash
        json_transactions = []
        for transaction in self.transactions:
            json_transactions.append(transaction.to_dict())
        data["transactions"] = json_transactions
        return data

    def hash_block(self):
        """
        Creates hash of block
        """
        data = {}
        data["index"] = self.index
        data["previous_hash"] = self.previous_hash
        data["validator"] = self.validator
        data["timestamp"] = self.timestamp
        json_transactions = []
        for transaction in self.transactions:
            json_transactions.append(transaction.to_dict())
        data["transactions"] = json_transactions
        return BlockChainUtils.hash(data).hexdigest()

    def payload(self):
        """
        Generates same dictionary as to_dict method but without current_hash
        """
        data = {}
        data["index"] = self.index
        data["previous_hash"] = self.previous_hash
        data["validator"] = self.validator
        data["timestamp"] = self.timestamp
        json_transactions = []
        for transaction in self.transactions:
            json_transactions.append(transaction.to_dict())
        data["transactions"] = json_transactions
        return data
    
    def is_full(self):
        """
        Checks if the block is full
        """
        return len(self.transactions) >= CAPACITY

    def sum_fees(self):
        """
        Sums the fees of all transactions in the block
        """
        fees = [transaction.fee for transaction in self.transactions]
        return sum(fees)
