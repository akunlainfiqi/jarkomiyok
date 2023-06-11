from socket import *
import socket
import threading
import time
import sys
import json
import logging
from chat import Chat

chatserver = Chat()

class ProcessTheClient(threading.Thread):
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)
		
	def ngewe(self, p):
		print('entod')

	def run(self):
		rcv=""
		while True:
			data = self.connection.recv(64)
			if data:
				d = data.decode()
				rcv=rcv+d
				if rcv[-2:]=='\r\n':
					#end of command, proses string
					logging.warning("data dari client: {}" . format(rcv))
					# try:
					# 	j = rcv.split(" ")
					# 	command = j[0].strip()
					# 	if (command == 'connectserver'):
					# 		ip = j[1].strip()
					# 		port = j[2].strip()

					# 		self.connection.sendall("success connect".encode())
					# 		rcv = ""
					# except error as e:
					# 	logging.warning(e)
					# 	continue
					hasil = json.dumps(chatserver.proses(rcv))
					hasil=hasil+"\r\n\r\n"
					logging.warning("balas ke  client: {}" . format(hasil))
					self.connection.sendall(hasil.encode())
					rcv=""
			else:
				break
		self.connection.close()

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.the_shards = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0',8889))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning("connection from {}" . format(self.client_address))
			
			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)
	

def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()
