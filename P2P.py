import socket
import threading

class P2P:
    # Class that represents the each node of the cluster    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET: IPv4, SOCK_STREAM: TCP
        self.connections = []

        self.start()

        # print(f"IP: {self.ip}, Port: {self.port}")
        # print("Peers:")
        # for peer in self.connections:
        #     print(peer, end=" ")

    # Method to create connection with another node
    def connect(self, peer_ip, peer_port):
        try:
            connection = self.socket.connect((peer_ip, peer_port))
            self.connections.append(connection)
            print(f"Connected to {peer_ip}:{peer_port}")
        except socket.error as e:
            print(f"Failed to connect to {peer_ip}:{peer_port}. Error: {e}")

    # Method that binds the socket to the ip and port and starts listening for incoming connections
    def listen(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen(10)  # 10: number of unaccepted connections that the system will allow before refusing new connections
        print(f"Listening for connections on {self.ip}:{self.port}")
    
        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            print(f"Accepted connection from {address}")

    # Method for exchanging data between peers
    def data_exchange(self, data):
        for connection in self.connections:
            try:
                connection.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")

    # Multithreaded Node; in order to be able to both listen and send data simultaneously
    def start(self):
        if (self.port == 47475):

            listen_thread = threading.Thread(target=self.listen)
            listen_thread.start()
        
        else:
            listen_thread = threading.Thread(target=self.connect, args=("91.140.28.86", 47475))
            listen_thread.start()