"""For saving the IP and port of a connection"""


class SocketConnector:
    """For saving the IP and port of a connection"""

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def equals(self, connector):
        """To see if a connector is same as another"""
        return connector.ip == self.ip and connector.port == self.port

    def to_dict(self):
        """Convert the connector to a dictionary"""
        return {"ip": self.ip, "port": self.port}