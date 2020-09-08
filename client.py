import socket
with socket.socket(socket.AF_INET6,socket.SOCK_DGRAM) as s:
	for i in range(200):
		data=str(i)+"  "+input("Enter message: "+str(i)+"  ")
		data=data.encode()
		s.sendto(data,("192.168.43.90",50007))