import socket
import threading
import os
from queue import Queue

serveradd=('',50007)
clientip='192.168.10.10'
clientadd=(clientip,50007)
q=Queue()
cip=Queue()
_sentinel=object()
q.put(_sentinel)

def serv(serveradd, clientip, q):
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		s.bind(serveradd)
		data, addr = s.recvfrom(1024)
		if clientip!=addr[0]: print('Connected by', addr)
		clientip=addr[0]
		ddata=data.decode()
		q.put(ddata)
		cip.put(clientip)
		print(ddata)
		while True:
			data, addr = s.recvfrom(1024)
			if clientip!=addr[0]: print('Connected by', addr)
			clientip=addr[0]
			if not data: break
			ddata=data.decode()
			cip.put(clientip)
			q.put(ddata)
			print(ddata)
			if not cliet.is_alive():
				cliet.start()
			if ddata=="end": break

def clie(cip, q):
	with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
		while True:
			temp=q.get()
			if temp==_sentinel:
				q.put(_sentinel)
				reply=''
			else: reply=temp
			if reply=='': data=input("Enter message: ")
			else : data="reply to message:'"+reply+"\n"+input("Enter message: ")
			if reply=="end":data="end"
			data=data.encode()
			s.sendto(data,(cip.get(),50007))
			if reply=="end":break
		

servt=threading.Thread(target=serv, name='servt', args=(serveradd, clientip, q))
servt.start()
flag=input("Do you want to send a message(y/n): ")
if flag=='y' or flag=='Y':
	clientip=input("Enter ip: ")
	cip.put(clientip)
	clientadd=(clientip, 50007)
	cliet=threading.Thread(target=clie, name='cliet', args=(cip, q))
	if not cliet.is_alive():
			cliet.start()
else: 
	cliet=threading.Thread(target=clie, name='cliet', args=(cip, q))