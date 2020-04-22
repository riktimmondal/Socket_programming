import socket
import time
import os
import sys
import pickle

class StreamData:
	def __init__(self, source, dest, packet_no, data):
		self.source = source
		self.dest = dest
		self.packet_no = packet_no
		self.data = data


def ServerList():
	print("Server Working")
	msg = "Server is alive and ready to display what server dictory contain"
	serverSocket.sendto(msg.encode(), clientAddr)
	print("Msg send to client")
	print("List function is called")

	Files = os.listdir(path="E:\\Video_Conf\\Udp_socket\\udp_with_chunk")
	Lists = []
	for File in Files:
		Lists.append(File)
	Lists_string = str(Lists)
	serverSocket.sendto(Lists_string.encode(), clientAddr)
	print("List send from server")

def ServerExit():
	#print("Exiting server...")
	#serverSocket.close()
	#sys.exit()
	pass

def ServerSend(fileName):
	print("Server Working")
	
	#sending msg to client for validation
	msg = "Server is alive and ready to send file"
	datagram = StreamData()
	serverSocket.sendto(msg.encode(), clientAddr)
	
	print("Msg send to client "+str(clientAddr))
	print("Function to send file from server is called")

	#checking fileName exist in server
	if os.path.isfile(fileName):
		msg = "File exist and will be send"
		serverSocket.sendto(msg.encode(), clientAddr)

		sendPacketCounter = 0
		#Findig no. of packets to send from byte size
		sizeFile = os.stat(fileName).st_size
		print("File size in bytes:" + str(sizeFile))
		#considering chunk size of 4096 byte
		numberPacketToSend = int(sizeFile/4096)+1
		#Sending msg to client about the no. of packets it should receive
		serverSocket.sendto(str(numberPacketToSend).encode(), clientAddr)

		numberPacketToSend_counter = numberPacketToSend
		file_reader = open(fileName, "rb")
		while numberPacketToSend_counter != 0:
			#reading file contains in bytes(here 4096 bytes)
			data = file_reader.read(4096)
			serverSocket.sendto(data, clientAddr)
			sendPacketCounter += 1
			numberPacketToSend_counter -=1
			print("Packet number:" + str(sendPacketCounter))
			print("........Data sending in progress.....")
		file_reader.close()
		print("File sending process completed from server")

	else:
		msg="Error: File not present in server"
		serverSocket.sendto(msg.encode(), clientAddr)

def ServerReceive(fileName):
	print("Server Working")
	print("Server will receive file from client "+str(clientAddr))
	
	#sending msg to client for validation
	msg = "Server is alive and ready to receive file"
	serverSocket.sendto(msg.encode(), clientAddr)
	
	print("Function to receive file from client is called")

	if msgClient_split[0] == "send":
		receiveFileName = fileName
		file_writer = open("ClientSend-"+receiveFileName,"wb")
		receivePacketCounter = 0
		print("Starting receiving packets")

		try:
			# number of packet
			countReceived, countReceivedAddr = serverSocket.recvfrom(4096)
		except:
			print("Some error occured")
			sys.exit()
		numberPacketToReceived = int(countReceived.decode("utf-8"))
		while numberPacketToReceived != 0:
			receivedData, receiveDAddr = serverSocket.recvfrom(4096)
			data = file_writer.write(receivedData)
			receivePacketCounter += 1
			numberPacketToReceived -=1
			print("Received packet number:" + str(receivePacketCounter))
		file_writer.close()
		print("File receing is done in server") 
	else:
		print("ServerReceive not working")

def ServerElse():
    msg = "Error: You asked for: " + \
        msgClient_split[0] + " which is not understood by the server."
    serverSocket.sendto(msg.encode(), clientAddr)
    print("Message Sent. to client")

def checkArg():
    """Only 1 argument excepted"""
    if len(sys.argv) != 2:
        print(
            "ERROR. Wrong number of arguments passed. System will exit. Next time please supply 1 argument!")
        sys.exit()
    else:
        print("Correct input, Proceding...")

checkArg()
host = ""

#take port no. from input
try:
	port = int(sys.argv[1])
except ValueError:
    print("Error. Exiting. Please enter a valid port number.")
    sys.exit()
except IndexError:
    print("Error. Exiting. Please enter a valid port number next time.")
    sys.exit()   

#create the socket and bind it
try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Server socket initialized")
    serverSocket.bind((host, port))
    print("Successful binding. Waiting for Client now.")
    # s.setblocking(0)
    # s.settimeout(15)
except socket.error:
    print("Failed to create socket")
    sys.exit()

#server is alive continously     
while True:
	try:
		data, clientAddr = serverSocket.recvfrom(4096)
	except:
		print("Error occured")
		sys.exit()
	
	msgClient = data.decode("utf-8")
	msgClient_split = msgClient.split()
	if msgClient_split[0] == "send":
		print("Go to ServerReceive func")
		ServerReceive(msgClient_split[1])
	elif msgClient_split[0] == "receive":
		print("Go to ServerSend func")
		ServerSend(msgClient_split[1])
	elif msgClient_split[0] == "list":
		print("Go to ServerList func")
		ServerList()
	elif msgClient_split[0] == "exit":
		#print("Go to ServerExit function")
		ServerExit()
	else:
		ServerElse()

print("**************Program ENd************")
quit()		
