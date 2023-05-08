
import socket

class TCPClient:
	def __init__(self, server, port, function):
		self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clientsock.connect((server, port))
		function(self,self.clientsock)

	def receive(self, socks):
		msg = socks.recv(2048)
		return msg

	def send(self, msg, socks):
		socks.sendall(msg)


class TCPServer(TCPClient):
	def __init__(self, port, queuelen):
		self.serverport = port
		self.queuelen = queuelen
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.bind(('localhost',  self.serverport))
		self.serversocket.listen(self.queuelen)

	def pollingAccept(self, function):
		while True:
			(acceptsocket ,address) = self.serversocket.accept()
			function(self,acceptsocket)
		return acceptsocket, address

	def threadedAccept(self, function):
		while True:
			(acceptsocket ,address) = self.serversocket.accept()
			function(self,acceptsocket)
    		ct = client_thread(so,acceptsocket)
    		ct.run()
		return acceptsocket, address
        