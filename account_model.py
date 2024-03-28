"""For holding information about and managing all the accounts in the network"""


class AccountModel:
    """For holding information about and managing all the accounts in the network"""

    def __init__(self):
        self.accounts = []  # List of public keys of all the participants in the network
        self.balances = {}  # Mapping between public key and token

    def generate_wallet(self, public_key_string):
        """Adds account and sets balance to zero"""
        if public_key_string not in self.accounts:
            self.accounts.append(public_key_string)
            self.balances[public_key_string] = 0

    def get_balance(self, public_key_string):
        """Returns balance in account"""
        if (
            public_key_string not in self.accounts
        ):  # If an account does not exist, it is added
            self.generate_wallet(public_key_string)
        return self.balances[public_key_string]

    def update_balance(self, public_key_string, amount):
        """Updates balance in account"""
        if (
            public_key_string not in self.accounts
        ):  # If an account does not exist, it is added
            self.generate_wallet(public_key_string)
        self.balances[public_key_string] += amount

    def get_bootstrap_public_key(self):
        """Returns the public key of the bootstrap account"""
        return self.accounts[0]
