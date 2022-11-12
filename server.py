import select
import socket
import sys
import threading
from DES import decryption


class Server:                   #Inisialization Server 
    def __init__(self):         
        self.host = '127.0.0.1'
        self.port = 80
        self.threads = []

    def open_socket(self):     
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(3)

    def run(self):               # Turn the server on
        self.open_socket()
        input_list = [self.server]
        while 1:                # As long as the server on, the encryption keeps receive message
                                # encrypt and decrypt the message
            read_ready, write_ready, exception = select.select(input_list, [], [])
            for r in read_ready:
                if r == self.server:
                    client_socket, client_address = self.server.accept()        # Server notice every client connected
                    print("A client found")
                    c = Client(client_socket, client_address, input_list)
                    c.start()
                    self.threads.append(c)
                elif r == sys.stdin:
                    _ = sys.stdin.readline()
        self.server.close()

        for c in self.threads:
            c.join()


class Client(threading.Thread):                 # Client initialization in server
    def __init__(self, client, address, input_list):
        threading.Thread.__init__(self)
        self.sock = socket
        self.SOCKET_LIST = input_list
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):                              # run the client
        try:
            while 1:
                data = self.client.recv(self.size)              # Message receiver by server
                if data:
                    data = data.decode('utf-8')                 # Encrypted by DES
                    print(f'Ciphertext : {data}')               # Show message encrypted by DES
                    decrypted = decryption(data)                # Decrypted by DES
                    print(f'Decrypted Text: {decrypted}\n')     # Show message decrypted from the encryption
                    self.client.send(data.encode('utf-8'))
                else:
                    self.client.close()
        except:
            if self.sock in self.SOCKET_LIST:                   
                self.SOCKET_LIST.remove(self.sock)              # Server notified if client disconnected

            print("No client found")
            self.client.close()


if __name__ == "__main__":
    try:
        server = Server()
        server.run()
    except KeyboardInterrupt:
        sys.exit(0)
