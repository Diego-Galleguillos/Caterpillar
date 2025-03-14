import socket
import threading
import time
import random
import sys

class client_manager:
    def __init__(self, id):
        self.id = id
        self.message = "Initial message from server."
        self.new = True

    def modify_message(self, new_message):
        self.message = new_message
        self.new = True
    
    def handle_client(self, client_socket):
        self.response = ""
        self.client_socket = client_socket
        client_socket.settimeout(0.1)  # Set a timeout for the recv method
        try:
            while True:
                try:
                    request = client_socket.recv(1024)
                    if request:
                        print(f"Received from client {self.id}: {request.decode()}")
                        self.response = f"{self.message} - {request.decode()}"
                        if self.new:
                            client_socket.send(self.message.encode())
                except socket.timeout:
                    # Timeout reached, send a message even if no request received
                        if self.new:
                            client_socket.send(self.message.encode())
                self.new = False
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            client_socket.close()

def main():
    con = int(input("Enter the number of connections: "))
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(6)
    print("Server listening on port 9999")

    clients = []
    client_id = 0
    while client_id < con:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        
        client = client_manager(client_id)
        clients.append(client)

        client_handler = threading.Thread(target=client.handle_client, args=(client_socket,))
        client_handler.start()
        client_id += 1
    
    message = input("Enter the new message: ")

    while "exit" not in message:
        message = input(f"Enter the new message for clients: ")
        if message == "exit":
            break
        if message == "gait":
            for client in clients:
                #message = "0_1"
                client.modify_message(message)
                while client.response == "":
                    time.sleep(0.001)
                client.response = ""
        elif message == 'gait2':
            for client in clients:
                message = "gait"
                client.modify_message(message)
                if client.id == 2:
                    while client.response == "":
                        time.sleep(0.001)
                    client.response = ""
        elif message == 'gaitd':
            message = "0_1"
            for client in clients:
                client.modify_message(message)
                time.sleep(1)
        else:        
            for client in clients:
                client.modify_message(message)

    
    sys.exit()



        

if __name__ == "__main__":
    main()
