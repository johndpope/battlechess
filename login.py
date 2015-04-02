import sys, os
from PySide import QtGui, QtCore
from communication import CommClient


class LoginWidg(QtGui.QWidget):
	# default window size
	def __init__(self, client, wparent=None):
		super(LoginWidg, self).__init__(wparent)
		self.width, self.height = 640, 480
		self.wparent = wparent
		self.client = client
		
		layout = QtGui.QGridLayout()
		self.login = QtGui.QLineEdit(self)
		self.passwd = QtGui.QLineEdit(self)
		self.passwd.setEchoMode(QtGui.QLineEdit.Password)
		signin = QtGui.QPushButton("Sign In", self)
		signup = QtGui.QPushButton("Sign Up", self)
		
		layout.addWidget(QtGui.QLabel("Login"), 0, 0)
		layout.addWidget(self.login, 0, 1)
		layout.addWidget(QtGui.QLabel("Pass"), 1, 0)
		layout.addWidget(self.passwd, 1, 1)
		layout.addWidget(signin, 2, 0)
		layout.addWidget(signup, 2, 1)
		
		self.setLayout(layout)
		
		signin.clicked.connect(self.tryConnect)
		signup.clicked.connect(self.tryRegister)
		
	def tryConnect(self):
		log = self.login.text()
		passwd = self.passwd.text()
		self.client.write('CONN', [log, passwd])
		head, data = self.client.read('VALD')
		if data :
			print 'successfully signed in'
		else :
			print 'ERROR while signing in'
			head, data = self.client.read('ERRO')
			print data
			
	
	def tryRegister(self):
		log = self.login.text()
		passwd = self.passwd.text()
		self.client.write('SIUP', [log, passwd])
		head, data = self.client.read('VALD')
		if data :
			print 'successfully signed up'
		else :
			print 'ERROR while signing up'
			head, data = self.client.read('ERRO')
			print data



if __name__ == "__main__":
	client = CommClient()
	client.connect("localhost", 8887)
	client.start()
	app = QtGui.QApplication(sys.argv)

	mainWin = LoginWidg(client)
	mainWin.show()

	ret = app.exec_()
	sys.exit(ret)

