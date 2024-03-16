import socket
import threading

class P2P:
    # Class that represents the each node of the cluster    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.connections = []
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET: IPv4, SOCK_STREAM: TCP
        self.socket.bind((self.ip, self.port))
        # self.socket.listen(10)  # 10: number of unaccepted connections that the system will allow before refusing new connections

        self.start()

    # Method to create connection with another node
    def connect(self, peer_ip, peer_port):
        try:
            connection = self.socket.connect((peer_ip, peer_port))
            self.connections.append(connection)
            print(f"Connected to {peer_ip}:{peer_port}")
            new_connection = self.socket.recv(1024)
            print(f"Received {new_connection}")
            
        except socket.error as e:
            print(f"Failed to connect to {peer_ip}:{peer_port}. Error: {e}")

    # Method that binds the socket to the ip and port and starts listening for incoming connections
    def listen(self):
        self.socket.listen(10)
        print(f"Listening for connections on {self.ip}:{self.port}")
        while (len(self.connections) < 9):
            connection, address = self.socket.accept()
            print(f"Accepted connection from {address}")

            # Broadcast the new connection to the other peers and, afterwards, add it to the connections list
            self.data_exchange(connection)
            # TODO: send to new connection the so-far connections
            self.connections.append(connection)
            

    # Method for exchanging data between peers
    def data_exchange(self, data):
        for connection in self.connections:
            try:
                connection.sendall(data)
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")

    # Multithreaded Node; in order to be able to both listen and send data simultaneously
    def start(self):
        if (self.port == 40000):
            listen_thread = threading.Thread(target=self.listen)
            listen_thread.start()
            # exchange_thread = threading.Thread(target=self.exchange_thread, args=self.connections)
            # exchange_thread.start()
        
        else:
            listen_thread = threading.Thread(target=self.connect, args=("127.0.0.1", 40000))
            listen_thread.start()
