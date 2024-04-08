"""For creating and managing a list of transactions"""
from config import CAPACITY

class TransactionPool:
    """For creating and managing a list of transactions"""

    def __init__(self):
        self.transactions = []  # A list of transactions

    def add_transaction(self, transaction):
        """Adds transaction to list"""
        self.transactions.append(transaction)

    def transaction_exists(self, transaction):
        """Checks if a transaction exists in the list"""
        for pool_transaction in self.transactions:
            if pool_transaction.equals(transaction):
                return True
        return False

    def remove_from_pool(self, transactions, Ivalidator, wallet = None):
        """Removes transactions from the pool, i.e., if they have been added to a block"""
        if Ivalidator == True:
            self.transactions = []
        else:
            rest_transactions = [t1 for t1 in self.transactions if not any(t1.equals(t2) for t2 in transactions)]
            self.transactions = []
            for transaction in rest_transactions:
                wallet.handle_transaction(transaction)

    def validation_required(self):
        """Decides if it is time to create a new block"""
        return len(self.transactions) >= CAPACITY
    
    def get_length(self):
        return len(self.transactions)