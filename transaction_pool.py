"""For creating and managing a list of transactions"""
from config import CAPACITY


class TransactionPool:
    """For creating and managing a list of transactions"""

    def __init__(self):
        self.transactions = []  # A list of transactions

    def set_wallet(self, wallet):
        self.wallet = wallet

    def add_transaction(self, transaction):
        """Adds transaction to list"""
        with self.wallet.lock:
            self.transactions.append(transaction)

    def transaction_exists(self, transaction):
        """Checks if a transaction exists in the list"""
        for pool_transaction in self.transactions:
            if pool_transaction.equals(transaction):
                return True
        return False

    def remove_from_pool(self, transactions):
        """Removes transactions from the pool, i.e., if they have been added to a block"""
        with self.wallet.lock:
            rest_transactions = [t1 for t1 in self.transactions if not any(t1.equals(t2) for t2 in transactions)]
            self.transactions = []
        for transaction in rest_transactions:
            if self.wallet is not None:
                self.wallet.handle_transaction(transaction, True)

    def validation_required(self):
        """Decides if it is time to create a new block"""
        with self.wallet.lock:
            return len(self.transactions) >= CAPACITY
    
    def get_length(self):
        return len(self.transactions)