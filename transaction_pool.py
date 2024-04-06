"""For creating and managing a list of transactions"""
capacity = 5


class TransactionPool:
    """For creating and managing a list of transactions"""

    def __init__(self):
        self.transactions = []  # A list of transactions

    def add_transaction(self, transaction):
        """Adds transaction to list"""
        self.transactions.append(transaction)
        print(len(self.transactions))

    def transaction_exists(self, transaction):
        """Checks if a transaction exists in the list"""
        for pool_transaction in self.transactions:
            if pool_transaction.equals(transaction):
                return True
        return False

    def remove_from_pool(self, transactions):
        """Removes transactions from the pool, i.e., if they have been added to a block"""
        new_pool_transactions = []
        for pool_transaction in self.transactions:
            insert = True
            for transaction in transactions:
                if pool_transaction.equals(transaction):
                    insert = False
            if insert:
                new_pool_transactions.append(pool_transaction)
        self.transactions = new_pool_transactions

    def validation_required(self):
        """Decides if it is time to create a new block"""
        return len(self.transactions) >= capacity
    
    def get_length(self):
        return len(self.transactions)