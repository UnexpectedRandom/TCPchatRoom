############################################ CLIENT ############################################

import socket, threading

HOST = '127.0.0.1'
PORT = 444
HEADER = 1024
FORMATER = 'utf-8'

ClientNickname = input("What do you want your nickname to be: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

def writeMessages():
    while True:
        message = '{}: {}'.format(ClientNickname, input(''))
        client.send(message.encode(FORMATER))

def getMessages():
    while True:
        try:
            message = client.recv(HEADER).decode(FORMATER)
            if message == 'NICKNAME ':
                client.send(ClientNickname.encode(FORMATER))
            else:
                print(message)
        except:
            print("Error Occured in Server")
            client.close()
            break

writeThread = threading.Thread(target=getMessages)
writeThread.start()

ReciveTheMessages = threading.Thread(target=writeMessages)
ReciveTheMessages.start()