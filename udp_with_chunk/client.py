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

def clientSend(fileName):
	print("Client wants to send")
	#check here whether server is alive or not then send
	try:
		serverValidData, serverAddr = clientSocket.recvfrom(4096)
	except:
		print("Some error occured while client receive")
		sys.exit()
	if serverValidData.decode("utf-8") == "Server is alive and ready to receive file":
		#sending data
		print("Start sending file")
		if os.path.isfile(fileName):
			receivePacketCounter = 0
			fileSize = os.stat(fileName).st_size
			print("File size in bytes: " + str(fileSize))
			numberPacketToSend = int(fileSize/4096)+1
			#Sending no. of packets to server
			print("Number of packets to be sent: " + str(numberPacketToSend))
			clientSocket.sendto(str(numberPacketToSend).encode(), serverAddr)

			file_reader = open(fileName, "rb")
			numberPacketToSend_counter = numberPacketToSend
			while numberPacketToSend_counter != 0:
				data = file_reader.read(4096)
				clientSocket.sendto(data, serverAddr)
				receivePacketCounter += 1
				numberPacketToSend_counter -=1
				print("Packet number:" + str(receivePacketCounter))
				print("Data sending in process:")
			file_reader.close()
			print("File sending process completed from client")
		else:
			print("File does not exist.")
	else:
		print("Server is Dead !!!!")


def clientReceive(fileName):
	print("Client wants to receive")
	#check here whether server is alive or not then recieve
	try:
		serverValidData, serverAddr = clientSocket.recvfrom(51200)
	except:
		print("Some error occured while client receive")
		sys.exit()
	if serverValidData.decode("utf-8") == "Server is alive and ready to send file":
		#check fileName exist in server or not
		try:
			serverData, serverAddr = clientSocket.recvfrom(51200)
		except:
			print("Some error occured while client receive")
			sys.exit()
		fileExistInServer = serverData.decode("utf-8")
		print('/'*15)
		print(fileExistInServer)
		print('/'*15)
		print("Inside Client Get")

		try:
			numberPacketsToReceived, serverAddr = clientSocket.recvfrom(4096)
		except:
			print("Some error occured while getting file size to download")
			sys.exit()
		#Getting first no. of packets
		numberPacketsToReceived = int(numberPacketsToReceived.decode("utf-8"))
		print('*'*15)
		print(numberPacketsToReceived)
		print('*'*15)
		file_writer = open("ClientReceived-"+fileName,"wb")
		receivePacketCounter = 0
		while  numberPacketsToReceived !=0 :
			receiveData, serverAddr = clientSocket.recvfrom(4096)
			data = file_writer.write(receiveData)
			receivePacketCounter += 1
			print("Received packet number:" + str(receivePacketCounter))
			numberPacketsToReceived -= 1
		file_writer.close()
		print("New file recieved check your directory")
	else:
		print("Server is not alive !!!!")

def clientExit():
	print("Exiting client")
	clientSocket.close()
	sys.exit()

def clientList():
	try:
		serverValidData, serverAddr = clientSocket.recvfrom(51200)
	except:
		print("Some error occured while client receive")
		sys.exit()
	if serverValidData.decode("utf-8") == "Server is alive and ready to display what server dictory contain":
		serverDictoryList, serverAddr = clientSocket.recvfrom(4096)
		data = serverDictoryList.decode("utf-8")
		print("These are files present in server")
		print(data)
	else:
		print("Server is Dead!!!")


def checkArg():
	if len(sys.argv) != 3:
		print("ERROR. Wrong number of arguments passed. System will exit. Next time please supply 2 argument!")
		sys.exit()
	else:
		print("Correct input, Proceding...")

checkArg()
host = sys.argv[1]
try:
	port = int(sys.argv[2])
except ValueError:
	print("Error. Exiting. Please enter a valid port number.")
	sys.exit()
except IndexError:
	print("Error. Exiting. Please enter a valid port number next time.")
	sys.exit()

try:
	"""
	socket.setblocking(flag)
	Set blocking or non-blocking mode of the socket: if flag is 0, the socket is set to non-blocking, else to blocking mode. Initially all sockets are in blocking mode.
	In non-blocking mode, if a recv() call doesn’t find any data, or if a send() call can’t immediately dispose of the data, an error exception is raised; in blocking mode,
	the calls block until they can proceed. s.setblocking(0) is equivalent to s.settimeout(0.0); s.setblocking(1) is equivalent to s.settimeout(None).

	socket.settimeout(value)
	Set a timeout on blocking socket operations. The value argument can be a nonnegative float expressing seconds, or None.
	If a float is given, subsequent socket operations will raise a timeout exception if the timeout period value has elapsed before the operation has completed.
	Setting a timeout of None disables timeouts on socket operations. s.settimeout(0.0) is equivalent to s.setblocking(0); s.settimeout(None) is equivalent to s.setblocking(1).
	"""
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print("Client socket initialized")
	clientSocket.setblocking(0)
	clientSocket.settimeout(15)


except socket.error:
	print("Failed to create socket")
	sys.exit()

while True:
	clientCommand = input("Please enter a command: \n1. receive [file_name]\n2. send [file_name]\n3. list\n4. exit\n ")

	try:
		clientSocket.sendto(clientCommand.encode('utf-8'), (host,port))
	except:
		print("Some error occured")
		sys.exit()

	commands = clientCommand.split()
	print("Procedding with user request")
	print("Pls check server for any error")

	if commands[0] == "receive":
		clientReceive(commands[1])
	elif commands[0] == "send":
		clientSend(commands[1])
	elif commands[0] == "list":
		clientList()
	elif commands[0] == "exit":
		clientExit()
	else:
		print('You have entered invlaid command')
		try:
			serverData, serverAddr = clientSocket.recvfrom(51200)
		except:
			print("Some error occured while client receive")
			sys.exit()
		print(serverData.decode('utf-8'))

print("**************Program ENd************")
quit()		



