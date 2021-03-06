import sys
import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 1234)
print('starting server up on %s port %s' % server_address)
sock.bind(server_address)

while True:
    print('waiting to receive message rom client')
    data, address = sock.recvfrom(4096)
    
    print('received %s bytes from %s' % (len(data), address))
    print(data)
    
    if data:
        sent = sock.sendto(data, address)
        print('sent %s bytes back to %s' % (sent, address))