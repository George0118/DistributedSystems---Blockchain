"""Contains various static methods for the Blockchain system"""

import json
import jsonpickle
from Crypto.Hash import SHA256


class BlockChainUtils:
    """
    Contains various static methods for the Blockchain system
    """

    @staticmethod
    def hash(data):
        """
        Creates a hash of data using the SHA-256 hash algorithm.
        """
        data_string = json.dumps(data)  # Takes data and makes it into string form
        data_bytes = data_string.encode("utf-8")  # Encodes data into bytes
        data_hash = SHA256.new(data_bytes)  # Hashes data
        return data_hash

    @staticmethod
    def encode(object_to_encode):
        """
        Encodes message object into a format that is allowed to be sent across the network
        """
        return jsonpickle.encode(object_to_encode, unpicklable=True)

    @staticmethod
    def decode(encoded_object):
        """
        Recreates object
        """
        return jsonpickle.decode(encoded_object)