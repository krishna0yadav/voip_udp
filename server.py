import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
	s.bind((HOST, PORT))
	temp=('',0)
	while True:
		data, addr = s.recvfrom(1024)
		if temp!=addr: print('Connected by', addr)
		temp=addr
		if not data: break
		print(data.decode())