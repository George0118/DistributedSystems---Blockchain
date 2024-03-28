import copy
from Classes.TransactionPool import TransactionPool
from wallet import Wallet
from blockchain import Blockchain
from Classes.SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Classes.Message import Message
from BlockChainUtils import BlockChainUtils
from enum import Enum


class NodeState(Enum):
    DOWN = "DOWN"   # Node is dead
    UP = "UP"       # Node is up and ready to receive the 1000 BCC
    INITIALIZED = "INITIALIZED"     # Node is initialized with the 1000 BCC
    READY = "READY"     # Node has 1000 BCC and is ready to start making transcations
    ERROR = "ERROR"     # Node is in Error state

class Node:
    """
    The managing entity that runs the blockchain system in the network of nodes
    """

    def __init__(self, ip, port):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.blockchain = Blockchain()
        self.transaction_pool = TransactionPool()
        self.wallet = Wallet()
        self.api = None
        self.state = NodeState.DOWN
        self.stakes_list = []       # For each Node keep their stake (last stake they have set in a valid block)
        self.funds_list = []        # For each Node keep their funds (money) to not allow for invalid transcations

    def start_p2p(self):
        """
        Starts socket communication
        """
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.start_socket_communication(self)
        self.state = NodeState.UP

    def start_api(self, api_port):
        """
        Starts Node API
        """
        self.api = NodeAPI()
        self.api.inject_node(self)
        self.api.start(api_port)

    def validate_transaction(self, transaction):
        """
        Validates a transaction
        """
        data = transaction.payload()
        signature = transaction.signature
        signer_address = transaction.sender_address

        signature_valid = Wallet.verify_transaction(data, signature, signer_address)  # Check if signature is valid

        transaction_exists = self.transaction_pool.transaction_exists(transaction)  # Checks if transaction already exists in the pool

        transaction_in_block = self.blockchain.transaction_exists(transaction)
        transaction_covered = self.blockchain.transaction_covered(transaction)
        if (
            not transaction_exists
            and not transaction_in_block
            and signature_valid
            and transaction_covered
        ):
            return True
        return False

    def handle_transaction(self, transaction):
        """
        Checks if transaction is valid and does not already exist - if valid it broadcasts it
        """
        if self.validate_transaction(transaction):
            # If the signature is valid and the transaction is new, it is added to the pool
            self.transaction_pool.add_transaction(transaction)
            message = Message(self.p2p.socket_connector, "TRANSACTION", transaction)
            encoded_message = BlockChainUtils.encode(message)
            self.p2p.broadcast(encoded_message)  # Broadcasts transaction as message
            if self.transaction_pool.validation_required():
                self.mint_block()
        else:
            print("Invalid transaction")

    def validate_block(self, block):
        """
        Validates a block
        """
        validator = block.validator
        block_hash = block.payload()
        signature = block.signature
        # index_valid = self.blockchain.index_valid(block)
        last_block_hash_valid = self.blockchain.last_block_hash_valid(block)
        validator_valid = self.blockchain.validator_valid(block)
        transactions_valid = self.blockchain.transactions_valid(block.transactions)
        signature_valid = Wallet.verify_signature(block_hash, signature, validator)
        if (
            last_block_hash_valid
            and validator_valid
            and transactions_valid
            and signature_valid
        ):
            return True

    def validate_chain(self, blockchain):
        """
        Validates a chain
        """
        for block in blockchain.chain:
            if block.index == 0:
                continue
            if not self.validate_block(block):
                return False
        return True

    def broadcast_block(self, block):
        """
        Broadcasts new block to all participant
        """
        # Checks if block is valid for security purposes
        index_valid = self.blockchain.index_valid(block)

        if not index_valid:
            self.request_chain()
        if self.validate_block(block):
            self.blockchain.add_block(block)
            self.transaction_pool.remove_from_pool(block.transactions)
            message = Message(self.p2p.socket_connector, "BLOCK", block)
            self.p2p.broadcast(BlockChainUtils.encode(message))

    def handle_blockchain_request(self, requesting_node):
        """
        Sends blockchain to requesting node as a message
        """
        message = Message(self.p2p.socket_connector, "BLOCKCHAIN", self.blockchain)
        self.p2p.send(requesting_node, BlockChainUtils.encode(message))

    def handle_blockchain(self, blockchain):
        """
        Updates our blockchain
        """
        local_blockchain_copy = copy.deepcopy(self.blockchain)  # Copy of own blockchain
        local_block_count = len(
            local_blockchain_copy.chain
        )  # Number of chain in our blockchain
        received_chain_block_count = len(
            blockchain.chain
        )  # Number of chain in received blockchain
        if local_block_count < received_chain_block_count:
            for block_number, block in enumerate(
                blockchain.chain
            ):  # Iterating through received blockchain
                if block_number >= local_block_count:  # Until a new block is found
                    local_blockchain_copy.add_block(block)
                    self.transaction_pool.remove_from_pool(block.transactions)
            self.blockchain = local_blockchain_copy

    def mint_block(self):
        """
        Checks if you are the validator and triggers block creation if necessary
        """
        validator = self.blockchain.next_validator()
        if validator == self.wallet.public_key():
            print("I am the validator")
            block = self.blockchain.create_block(
                self.transaction_pool.transactions, self.wallet
            )
            self.transaction_pool.remove_from_pool(
                self.transaction_pool.transactions
            )  # Clears transaction pool by removing all transactions added to block
            message = Message(self.p2p.socket_connector, "BLOCK", block)
            self.p2p.broadcast(
                BlockChainUtils.encode(message)
            )  # The new block is broadcast
        else:
            print("I am not the validator")

    def request_chain(self):
        """
        Generating a message that requests the blockchain
        """
        message = Message(self.p2p.socket_connector, "BLOCKCHAINREQUEST", None)
        self.p2p.broadcast(BlockChainUtils.encode(message))

    def stake(self, amount):
        """
        Stakes an amount
        """
        self.wallet.create_transaction(0, amount, "", "STAKE")