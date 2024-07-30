import socket
import threading
import random

SERVER_IP = '127.0.0.1' 
SERVER_PORT = 12345  
MAX_CONNECTIONS = 100  


class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        print(f"Sent a file to {self.client_address}")
        try:
            numbers = [random.randint(-999999999, 999999999) for _ in range(250000)]
            numbers_string = ','.join(map(str, numbers))
            self.client_socket.sendall(numbers_string.encode())
        except Exception as e:
            print(f"Error handling client {self.client_address}: {e}")
        finally:
            self.client_socket.close()
            print(f"Connection from {self.client_address} closed.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(MAX_CONNECTIONS)
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = ClientHandler(client_socket, client_address)
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
