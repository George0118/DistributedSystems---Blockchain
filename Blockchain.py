"""For creating and managing a linked list of chain"""

from block import Block
from utils import BlockChainUtils
from proof_of_stake import ProofOfStake

from transaction import Transaction
from config import N


class Blockchain:
    """For creating and managing a linked list of chain"""

    def __init__(self):
        self.chain = [Block.genesis()]

        self.pos = ProofOfStake()
        self.chain[0].transactions.append(self.create_genesis_transaction())

    def create_genesis_transaction(self):
        """Creates the genesis transaction"""
        bootstrap_node_public_key = AccountModel.get_bootstrap_public_key(
            self.account_model
        )
        genesis_transaction = Transaction(
            sender_address="0",
            receiver_address=bootstrap_node_public_key,
            amount=1000 * N,
            nonce=0,
            message="",
            type_of_transaction="EXCHANGE",
        )
        return genesis_transaction

    def add_block(self, block):
        """Adds a block to the blockchain and executes the transactions in the block"""
        self.execute_transactions(block.transactions)
        total_fees = block.total_fees()
        self.account_model.update_balance(block.validator, total_fees)
        self.chain.append(block)

    def to_dict(self):
        """Will help display blockchain in readable dictionary form"""
        data = {}
        json_blocks = []
        for block in self.chain:
            json_blocks.append(block.to_dict())
        data["chain"] = json_blocks
        return data

    def index_valid(self, block):
        """Checks if the index is one greater than the previous block's index"""
        return (
            self.chain[-1].index == block.index - 1
        )  # Note - indexing with -1 gets latest block

    def last_block_hash_valid(self, block):
        """Checks if the last hash is the hash of the previous block's hash"""
        latest_blockchain_block_hash = BlockChainUtils.hash(
            self.chain[-1].payload()
        ).hexdigest()
        return latest_blockchain_block_hash == block.previous_hash

    def get_covered_transaction_set(self, transactions):
        """Gets all of the covered transactions"""
        covered_transactions = []
        for transaction in transactions:
            if self.transaction_covered(transaction):
                covered_transactions.append(transaction)
            else:
                print("transaction is not covered by sender")
        return covered_transactions

    def transaction_covered(self, transaction: Transaction):
        """Checks if a transaction is covered by the sender's funds"""
        if transaction.type_of_transaction == "EXCHANGE":
            return (
                True  # If a transaction is an exchange transaction it is always covered
            )
        sender_balance = self.account_model.get_balance(transaction.sender_address)
        if len(transaction.message) == 0 and transaction.amount == 0:
            print("Invalid transaction")
            return False
        if transaction.type_of_transaction == "DEFAULT":
            fee = sender_balance >= len(transaction.message) + transaction.amount * 1.03
            return (
                sender_balance >= len(transaction.message) + transaction.amount * 1.03
                and fee != 0
            )
        return False

    def execute_transactions(self, transactions):
        """Will execute each transaction in a list of transactions"""
        for transaction in transactions:
            self.execute_transaction(transaction)

    def execute_transaction(self, transaction: Transaction):
        """Will execute a transaction"""
        sender = transaction.sender_address
        receiver = transaction.receiver_address
        if transaction.type_of_transaction == "STAKE":
            if receiver == 0:  # For the transaction to actually be of type stake,
                # the receiver public key must be 0
                amount = transaction.amount
                self.pos.update(sender, amount)  # The stake is added
                self.account_model.update_balance(sender, -amount)
                # The amount staked is deducted from balance
        else:
            if len(transaction.message) == 0 and transaction.amount == 0:
                print("Invalid transaction")
                return
            if len(transaction.message) == 0 and transaction.amount > 0:
                # If there is no message, then it is a regular transaction with 3% fee
                sender = transaction.sender_address
                receiver = transaction.receiver_address
                amount = transaction.amount
                self.account_model.update_balance(
                    sender, -amount * 1.03
                )  # Subtract from sender
                self.account_model.update_balance(receiver, amount)  # Add to receiver
            else:  # If there is a message (and perhaps an amount too)
                sender = transaction.sender_address
                receiver = transaction.receiver_address
                amount = len(transaction.message) + transaction.amount * 1.03
                self.account_model.update_balance(
                    sender, -amount
                )  # Subtract from sender

    def next_validator(self):
        """Returns the next validator"""
        last_block_hash = BlockChainUtils.hash(
            self.chain[-1].payload()
        ).hexdigest()  # Gets last block hash
        next_validator = self.pos.validator(last_block_hash)
        return next_validator

    def create_block(self, transactions_from_pool, validator_wallet):
        """Creates a new block"""
        covered_transactions = self.get_covered_transaction_set(
            transactions_from_pool
        )  # See which transactions are covered
        self.execute_transactions(covered_transactions)  # Executes covered transactions
        new_block = validator_wallet.create_block(
            covered_transactions,
            BlockChainUtils.hash(self.chain[-1].payload()).hexdigest(),
            len(self.chain),
        )  # Creates new block and adds signature (uses method in wallet)
        self.chain.append(new_block)  # Adds new block to blockchain
        return new_block  # Block is returned so that it can be broadcast

    def transaction_exists(self, transaction: Transaction):
        """Checks if transaction is already in blockchain"""
        for block in self.chain:  # Iterate through all chain
            for block_transaction in block.transactions:  # Iterate in block
                if transaction.equals(block_transaction):
                    return True  # The transaction already exists in the blockchain
        return False

    def validator_valid(self, block: Block):
        """Checks if validator is actually valid"""
        validator_public_key = self.pos.validator(block.previous_hash)
        proposed_block_validator = block.validator
        return validator_public_key == proposed_block_validator

    def transactions_valid(self, transactions):
        """Checks if transactions are actually valid"""
        covered_transactions = self.get_covered_transaction_set(transactions)
        if len(covered_transactions) == len(transactions):
            return True
        return False
    
    def get_prevhash(self):
        """Returns the hash of the last block in the blockchain"""
        last_block = self.chain[-1]
        return last_block.current_hash
    
    def next_index(self):
        return len(self.chain)