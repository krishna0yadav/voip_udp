import socket
import threading
#import os
from queue import Queue

def serv(obj):
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		s.bind(('',50007))
		while True:
			data, addr = s.recvfrom(1024)
			clientip=''
			while not obj.empty():
				clientip=obj.get()
			if clientip!=addr[0]: 
				print('Connected by', addr)
				obj.put(addr[0])
			else:
				obj.put(clientip)
			ddata=data.decode()
			#obj.putq(ddata)
			print(ddata)
			print(type(ddata))
			print(len(ddata))
			print(str(ddata)=="end")
			print("\n")
			if str(ddata)=="end": return

def clie(obj):
	with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
		while True:
			message=input()
			#reply=obj.getq()
			#if reply=='null': data=message
			#else : data="reply to message:'"+str(reply)+"\n"+message
			#if reply=="end":data="end"
			data=message
			data=data.encode()
			if obj.empty():
				temp=input("Enter ip: ")
			else:
				while not obj.empty():
					temp=obj.get()
			obj.put(temp)
			s.sendto(data,(temp,50007))
			if message=="end": return
			#if reply=="end":break

d=Queue()
servt=threading.Thread(target=serv, name='servt', args=(d,))
servt.start()
flag=input("Do you want to send a message(y/n): ")
if flag=='y' or flag=='Y':
	if d.empty():
		d.put(input("Enter ip: "))
cliet=threading.Thread(target=clie, name='cliet', args=(d,))
cliet.start()