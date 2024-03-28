"""Stores and manages lots"""

from blockchain_utils import BlockChainUtils


class Lot:
    """Stores and manages lots"""

    def __init__(self, public_key, iteration, last_block_hash):
        self.public_key = str(public_key)
        self.iteration = iteration
        self.last_block_hash = str(last_block_hash)

    def lot_hash(self):
        """Creates the lot hash is based on the public key and last block hash"""
        hash_data = self.public_key + self.last_block_hash
        for _ in range(self.iteration):  # Different iteration will hash a different
            # number of times and so create a different final hash
            hash_data = BlockChainUtils.hash(hash_data).hexdigest()
        return hash_data
