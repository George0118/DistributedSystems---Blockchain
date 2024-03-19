from Crypto.PublicKey import RSA    # pycryptodome
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class Wallet:

    def __init__(self):
        self.generate_wallet()
    
    def generate_wallet(self):
        key = RSA.generate(2048)
        self.private_key = key.export_key().decode('utf-8')
        self.public_key = key.publickey().export_key().decode('utf-8')
    
    def sign_transaction(self, transaction_data):
        hash_data = SHA256.new(transaction_data)        # transaction_data.encode('utf-8')
        signature = pkcs1_15.new(self.private_key).sign(hash_data)
        return signature
    
    def verify_transaction(self, public_key, transaction_data, signature):
        hash_data = SHA256.new(transaction_data)        # transaction_data.encode('utf-8')
        try:
            pkcs1_15.new(public_key).verify(hash_data, signature)
            return True
        except (ValueError, TypeError):
            return False
    ## https://www.pycryptodome.org/src/signature/pkcs1_v1_5
        

    def create_transaction(self, receiver_address, ):
        transaction = Transaction(self.publicKeyString(), receiver_address, )

        signature = self.sign_transaction(transaction.payload())
        transaction.sign(signature)
        return transaction

    def createBlock(self, transactions, lastHash, blockCount):
        block = Block(transactions, lastHash,
                        self.publicKeyString(), blockCount)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block

