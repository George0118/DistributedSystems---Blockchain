import random


class ProofOfStake:
    """Consensus algorithm - keeps track of amount of stake of each account
    (to decide who is the next validator)"""

    def __init__(self):
        self.stakes = {}  # Mapping of account to stake

    def set_stakes(self, stakes):
        """Sets the stakes"""
        self.stakes = stakes

    def validator_lots(self):
        """Creates list of all lots"""
        lots = []
        for validator, stake in self.stakes.items():
            for _ in range(stake):
                lots.append(validator)
        return lots

    def winner_lot(self, lots, seed):
        """Finds which lot won"""
        random.seed(seed)
        winner_lot = random.choice(lots)
        return winner_lot  # Returns winner_lot

    def validator(self, last_block_hash):
        """Finds who will be the validator and returns their public key"""
        lots = self.validator_lots()
        winner_id = self.winner_lot(lots, last_block_hash)
        return winner_id
