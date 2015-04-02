import socket
import sys, traceback
import threading
import Queue
import time

KNOWN_HEADERS = ['NICK', # NICK : Nickname, data is a string
				 'COLR', # COLR : Player color, data is a string
				 'OVER', # OVER : Game is Over, data is None
				 'URLR', # URLR : URL for the replay, data is a string
				 'MOVE', # MOVE : Player's move, data is a 4 int list (int from 0 to 7, so always 1 char)
				 'BORD', # BORD : Game state, data is a string representation of the board
				 'VALD', # VALD : Confirmation from the server for a client's action, data is a boolean
				 'CONN', # CONN : Asking for connexion, data is "login password-hash"
				 'SIUP', # SIUP : Asking for new account, data is "login password-hash"
				 'ERRO', # ERRO : Error, data is a humna readable error message
				 ]



# generic tow way conversion from raw data to string representation
def dataToString(header, data):
	if header in ['NICK', 'COLR', 'URLR', 'BORD', 'ERRO'] :
		return data
	elif header == 'OVER':
		return 'None'
	elif header == 'MOVE':
		return str(data[0])+str(data[1])+str(data[2])+str(data[3])
	elif header == 'VALD':
		if data :
			return 'T'
		else :
			return 'F'
	elif header in ['CONN', 'SIUP']:
		return data[0]+' '+data[1]
	else :
		print 'Unknown message type :', header
		raise

# and from string to raw data
def stringToData(header, data):
	if header in ['NICK', 'COLR', 'URLR', 'BORD', 'ERRO'] :
		return data
	elif header == 'OVER':
		return None
	elif header == 'MOVE':
		return [int(data[0]), int(data[1]), int(data[2]), int(data[3])]
	elif header == 'VALD':
		return data == 'T'
	elif header in ['CONN', 'SIUP']:
		return data.split(" ")
	else :
		print 'Unknown message type :', header
		raise



# generic receive function
def myreceive(sock, MSGLEN):
	msg = ''
	while len(msg) < MSGLEN:
		chunk = sock.recv(MSGLEN-len(msg))
		if chunk == '':
			raise RuntimeError("socket connection broken")
		msg = msg + chunk
	return msg

# send an object over the network
def sendData(sock, header, data):
	pack  = header
	datas = dataToString(header, data)
	pack += "%05d"%(len(datas))
	pack += datas
	sock.send(pack)
	if header not in KNOWN_HEADERS :
		print 'Unknown message type :', header

# recieve a message and return the proper object
def recvData(sock):
	header = myreceive(sock, 4)
	size   = int(myreceive(sock, 5))
	datas  = myreceive(sock, size)
	data   = stringToData(header, datas)
	print "recieved :", header, data
	if header not in KNOWN_HEADERS :
		print 'Unknown message type :', header
	return list([header, data])

# wait for a specific type of data and returns it
# header should be a list of string
def waitForMessage(sock, header):
	head = None
	while head not in header:
		head, data = recvData(sock)
	return stringToData(head, data)




#---------------------------------------
# Client soket thread object
#---------------------------------------


class CommClient(threading.Thread):
	def __init__(self):
		super(CommClient, self).__init__()
		self.connected = False
		self.running = False
		self.socket = None
		self.host = None
		self.port = None
		self.messIn = Queue.Queue()
		
	def connect(self, host, port):
		self.host = host
		self.port = port
		#create socket and connect
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print 'connecting to' , (self.host, self.port)
		self.sock.connect((self.host, self.port))
		self.connected = True
		
	def run(self):
		while not self.connected :
			time.sleep(0.1)
		
		self.running = True
		while self.running :
			try :
				data = recvData(self.sock)
				self.messIn.put(data)
			except Exception as e:
				print e
				traceback.print_exc(file=sys.stdout)
				self.sock.close
				self.running = False
		
	def write(self, header, data):
		if not self.connected :
			print "cannot send message, not connected yet"
			return False
		sendData(self.sock, header, data)
		
	def read(self, header = None):
		head = None
		while head != header:
			head, data = self.messIn.get(True) # block
		return head, data


















