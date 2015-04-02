#!/usr/bin/python

import socket
import sys, traceback
import signal
import threading
import time
from Board import Board
from communication import sendData, recvData, waitForMessage
import sqlite3
import re
def validText(strg, search=re.compile(r'[^a-zA-Z0-9_]').search):
	return len(strg)>2 and not bool(search(strg))



class GameThread(threading.Thread):
	def __init__(self, client_1, client_2):
		super(GameThread, self).__init__()
		self.client_1 = client_1
		self.client_2 = client_2
		self.nick_1 = ""
		self.nick_2 = ""
		self.board = Board()

	def run(self):
		self.nick_1 = waitForMessage(self.client_1, 'NICK')
		self.nick_2 = waitForMessage(self.client_2, 'NICK')
		filename = time.strftime("games/%Y_%m_%d_%H_%M_%S")
		filename += "_"+self.nick_1+"_Vs_"+self.nick_2+".txt"
		log = open(filename, "w")
		log.write(self.nick_1+' Vs. '+self.nick_2+'\n')
		
		sendData(self.client_1, 'URLR', "http://git.sxbn.org/battleChess/"+filename)
		sendData(self.client_2, 'URLR', "http://git.sxbn.org/battleChess/"+filename)


		sendData(self.client_1, 'NICK', self.nick_2)
		sendData(self.client_2, 'NICK', self.nick_1)


		loop = True
		try :
			while loop:
				valid = False
				while not valid :
					head, move = recvData(self.client_1)
					if head == "OVER" :
						loop = False
						raise # jump to finaly
					elif head == 'MOVE':
						i, j, ii, jj = move
						valid, pos = self.board.move(i,j,ii,jj, 'w')
						#print "got move from", [i,j], "to", [ii,jj], "from white", valid
						sendData(self.client_1, 'VALD', valid)
					else :
						print 'error : server was expecting MOVE, not', head
						raise 

				log.write("%d %d %d %d\n"%(i,j,ii,jj))
				if self.board.winner : # if we have a winner, send the whole board
					endBoard = self.board.toString()
					sendData(self.client_1, 'BORD', endBoard)
					sendData(self.client_2, 'BORD', endBoard)
					break # game is over
				else :
					sendData(self.client_1, 'BORD', self.board.toString('w'))
					sendData(self.client_2, 'BORD', self.board.toString('b'))

				valid = False
				while not valid :
					head, move = recvData(self.client_2)
					if head == "OVER" :
						loop = False
						raise # jump to finaly
					elif head == 'MOVE':
						i, j, ii, jj = move
						valid, pos = self.board.move(i,j,ii,jj, 'b')
						#print "got move from", [i,j], "to", [ii,jj], "from black", valid
						sendData(self.client_2, 'VALD', valid)
					else :
						print 'error : server was expecting MOVE, not', head
						raise 	

				log.write("%d %d %d %d\n"%(i,j,ii,jj))
				if self.board.winner : # if we have awinner, send the whole board
					endBoard = self.board.toString()
					sendData(self.client_1, 'BORD', endBoard)
					sendData(self.client_2, 'BORD', endBoard)
					break # game is over
				else :
					sendData(self.client_1, 'BORD', self.board.toString('w'))
					sendData(self.client_2, 'BORD', self.board.toString('b'))
		except Exception as e:
			print e
			traceback.print_exc(file=sys.stdout)
			pass
		finally : # Always close the game
			#print "finishing the game"
			log.flush()
			log.close()
			sendData(self.client_1, 'OVER', None)
			sendData(self.client_2, 'OVER', None)
			self.client_1.close()
			self.client_2.close()


class UserThread(threading.Thread):
	def __init__(self, sock, dbfile):
		super(UserThread, self).__init__()
		self.sock = sock
		self.userID = None
		self.dbfile = dbfile
	
	# try to connect an user with given password
	def tryConnect(self, log, passwd):
		print "trying to log with", log, ':', passwd
		self.db.execute('select id, pass from users where login=?', (log,))
		data = self.db.fetchone()
		print data
		if data is None:
			sendData(self.sock, 'VALD', False)
			sendData(self.sock, 'ERRO', "Unknown user %s"%log)
			print "unknown user"
			return False
		else :
			if passwd != data[1]:
				sendData(self.sock, 'VALD', False)
				sendData(self.sock, 'ERRO', "Invalid password for user %s"%log)
				print "invalid password"
				return False
			else :
				self.userID = data[0]
				self.userName = log
				sendData(self.sock, 'VALD', True)
				print "success"
				return True
			
	# try to register a new user with given log / passord
	def tryRegister(self, log, passwd):
		print "trying to register with", log, ':', passwd
		if not validText(log) or not validText(passwd):
			sendData(self.sock, 'VALD', False)
			sendData(self.sock, 'ERRO', "Invalid login / password. please respect [a-Z0-9_]")
			return False
		
		self.db.execute('select * from users where login=?', (log,))
		data = self.db.fetchone()
		if data is not None:
			sendData(self.sock, 'VALD', False)
			sendData(self.sock, 'ERRO', "Account name %s already taken"%log)
			return False
		else :
			# add user
			self.db.execute("INSERT INTO users (login, pass) VALUES (?, ?)", (log, passwd))
			# retrieve its ID
			self.db.execute('select id from users where login=?', (log,))
			data = self.db.fetchone()
			self.userID = data[0]
			self.userName = log
			sendData(self.sock, 'VALD', True)
			return True
	
	def run(self):
		# auto commit to DataBase
		conn = sqlite3.connect(self.dbfile, isolation_level=None)
		self.db = conn.cursor()
		try :
			# state 1 : waiting for sign in or sign up
			connected = False
			while not connected:
				header, data = recvData(self.sock)
				if header not in ['CONN', 'SIUP']:
					sendData(self.sock, 'VALD', False)
					sendData(self.sock, 'ERRO', "please connect or register before sending any request")
				elif header == 'CONN' :
					connected = self.tryConnect(data[0], data[1])
				elif header == 'SIUP':
					connected = self.tryRegister(data[0], data[1])
			# connexion done
			while True :
				print "waiting for other commands"
				time.sleep(1)
				
		except Exception as e:
			print e
			traceback.print_exc(file=sys.stdout)
		finally:
			sendData(self.sock, 'OVER', None)
			self.sock.close()



if __name__ == '__main__':
	PORT = 8887
	HOST = '' # default value
	if len(sys.argv) == 1 :
		print "Usage:\n\t", sys.argv[0], "PORT"
	if len(sys.argv) > 1 :
		PORT = int(sys.argv[1])
	if len(sys.argv) > 2 :
		HOST = sys.argv[2]
	
	#print " starting server on "+socket.gethostname()+":"+str(PORT)

	#create an INET, STREAMing socket
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serversocket.bind((HOST, PORT))

	# register SIGINT to close socket
	def signal_handler(signal, frame):
		print('You pressed Ctrl+C!')
		serversocket.close()
		sys.exit(0)


	#become a server socket
	serversocket.listen(5)
	loop = True
	while loop :
		try :
			#accept connections from outside
			(sock, address) = serversocket.accept()
			user = UserThread(sock, "btch.db")
			user.start()
		except Exception as e:
			print e
			loop = False
			serversocket.close()
