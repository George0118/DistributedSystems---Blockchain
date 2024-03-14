"""For creating messages"""

class Message:
    """For creating messages"""

    def __init__(self, sender_connector, message_type, data):
        self.sender_connector = sender_connector  # Where to send message
        self.message_type = message_type
        self.data = data