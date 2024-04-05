"""Consensus algorithm - keeps track of amount of stake of each account 
(to decide who is the next validator)"""

from BlockChainUtils import BlockChainUtils
from Lot import Lot


class ProofOfStake:
    """Consensus algorithm - keeps track of amount of stake of each account
    (to decide who is the next validator)"""

    def __init__(self):
        self.stakers = {}  # Mapping of account to stake
        # self.set_genesis_node_stake()  # Initial staker

    def update(self, public_key_string, stake):
        """Updates stake of an account"""
        if public_key_string in self.stakers:  # If public key in dictionary, update
            self.stakers[public_key_string] += stake
        else:  # Else, add to dictionary
            self.stakers[public_key_string] = stake

    def get(self, public_key_string):
        """Returns stake of an account"""
        if public_key_string in self.stakers:
            return self.stakers[public_key_string]
        return None

    def validator_lots(self, seed):
        """Creates list of all lots"""
        lots = []
        for validator in self.stakers:
            for stake in range(self.get(validator)):
                lots.append(Lot(validator, stake + 1, seed))
        return lots

    def winner_lot(self, lots, seed):
        """Finds which lot won"""
        winner_lot = None
        least_offset = None
        reference_hash_int_value = int(BlockChainUtils.hash(seed).hexdigest(), 16)
        # The lot whose hash is closest to this value is the winner lot
        # (will always be 16 bytes)
        for lot in lots:
            lot_int_value = int(lot.lot_hash(), 16)
            offset = abs(lot_int_value - reference_hash_int_value)
            if least_offset is None or offset < least_offset:
                least_offset = offset
                winner_lot = lot
        return winner_lot  # Returns winner_lot

    def validator(self, last_block_hash):
        """Finds who will be the validator and returns their public key"""
        lots = self.validator_lots(last_block_hash)
        winner_lot = self.winner_lot(lots, last_block_hash)
        return winner_lot.public_key