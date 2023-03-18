############################################ SERVER ############################################
import socket, threading

HOST = '127.0.0.1'
PORT = 444
HEADER = 1024
FORMATER = 'utf-8'

# Global variables
clients = []
usernames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)
        
# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast('{} left!'.format(username).encode(FORMATER))
            usernames.remove(username)
            break
        
# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store nicknames
        client.send('NICKNAME '.encode(FORMATER))
        nickname = client.recv(1024).decode(FORMATER)
        usernames.append(nickname)
        clients.append(client)

        # Print And Broadcast nicknames
        print("nicknames is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode(FORMATER))
        client.send('Connected to server!'.encode(FORMATER))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("[SERVER] Server Has Started...")
receive()