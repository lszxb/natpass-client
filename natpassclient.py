import socket
import sys

defaultPort = 7989

def connectToClient(myName, clientName, serverIP, serverPort=defaultPort, sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
    data = 'request\n' + myName + '\n' + clientName
    sock.sendto(data.encode('utf-8')， (serverIP, serverPort))
    clientIP = None
    clientPort = None
    while True:
        respone = sock.recv(1024).decode('utf-8').split('\n')
        if respone[0] == 'wait':
            serverID = respone[1]
            data = 'done\n' + myName
            sock.sendto(data.encode('utf-8')， (serverIP, serverPort)
        elif respone[0] == 'send' and respone[-1] == serverID:
            data = 'hello\n' + myName
            clientIP = respone[1]
            clientPort = int(respone[2])
            sock.sendto(data.encode('utf-8')， (clientIP, clientPort))
            data = 'done\n' + myName
            sock.sendto(data.encode('utf-8')， (serverIP, serverPort)
        elif respone[0] == 'hello' and respone[-1] == clientName:
            data = 'welcome\n' + myName
            sock.sendto(data.encode('utf-8'), (clientIP, clientPort))
        elif respone[0] == 'welcome' and respone[-1] == clientName:
            data = 'sure\n' + myName
            sock.sendto(data.encode('utf-8'), (clientIP, clientPort))
            break
        elif respone[0] == 'sure' and respone[-1] == clientName:
            data = 'success\n' + myName
            sock.sendto(data.encode('utf-8')， (serverIP, serverPort)
            break
    return sock, (clientIP, clientPort)



if __name__ == '__main__':
    if len(sys.argv) == 4:
        if connectToClient(sys.argv[1], sys.argv[2], sys.argv[3]):
            print('Success!')
        else:
            print('Error!')
    elif len(sys.argv) == 5:
        if connectToClient(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])):
            print('Success!')
        else:
            print('Error!')
    else:
        exit(1)