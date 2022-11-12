import socket
import sys
from DES import encryption
from DES import decryption

class Client:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 80

    def open_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def run(self):
        self.open_socket()
        # try:
        while True:
                print ("You may Enter your message:")
                msg = input()
                msg = encryption(msg)
                self.client.send(msg.encode('utf-8'))

if __name__ == "__main__":
    client = Client()
    client.run()
