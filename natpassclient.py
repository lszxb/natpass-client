#!/usr/bin/env python3


import socket
import sys

defaultPort = 7989


def ConnectToClient(myName, clientName, serverIP, serverPort=defaultPort,
                    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
    data = 'request\n' + clientName + '\n' + myName
    sock.sendto(data.encode('utf-8'), (serverIP, serverPort))
    clientIP = None
    clientPort = None
    serverID = None
    while True:
        response, addr = sock.recvfrom(1024)
        response = response.decode('utf-8').split('\n')
        if response[0] == 'wait':
            serverID = response[1]
            data = 'done\n' + myName
            sock.sendto(data.encode('utf-8'), (serverIP, serverPort))
        elif response[0] == 'send' and response[-1] == serverID:
            data = 'hello\n' + myName
            clientIP = response[1]
            clientPort = int(response[2])
            sock.sendto(data.encode('utf-8'), (clientIP, clientPort))
            data = 'done\n' + myName
            sock.sendto(data.encode('utf-8'), (serverIP, serverPort))
        elif response[0] == 'hello' and response[-1] == clientName:
            data = 'welcome\n' + myName
            clientIP = addr[0]
            clientPort = addr[1]
            sock.sendto(data.encode('utf-8'), (clientIP, clientPort))
        elif response[0] == 'welcome' and response[-1] == clientName:
            data = 'sure\n' + myName
            sock.sendto(data.encode('utf-8'), (clientIP, clientPort))
            break
        elif response[0] == 'sure' and response[-1] == clientName:
            data = 'success\n' + myName
            sock.sendto(data.encode('utf-8'), (serverIP, serverPort))
            break
        else:
        	return None
        print(serverID)
    return sock, (clientIP, clientPort)


if __name__ == '__main__':
    if len(sys.argv) == 4:
        if ConnectToClient(sys.argv[1], sys.argv[2], sys.argv[3]):
            print('Success!')
        else:
            print('Error!')
    elif len(sys.argv) == 5:
        if ConnectToClient(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])):
            print('Success!')
        else:
            print('Error!')
    else:
        exit(1)
