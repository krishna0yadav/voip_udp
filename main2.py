import socket
import threading
#import os
#from queue import Queue

class Details:
	def __init__(self, clientip):
		self.clientip=clientip
		self.q='null'
	def getclientip(self):
		return self.clientip
	def setclientip(self, data):
		self.clientip=data
	def getq(self):
		return self.q
	def putq(self, data):
		self.q=data

def serv(obj):
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		s.bind(('',50007))
		while True:
			data, addr = s.recvfrom(1024)
			if obj.getclientip()!=addr[0]: 
				print('Connected by', addr)
				obj.setclientip(addr[0])
			ddata=data.decode()
			obj.putq(ddata)
			print(ddata)
			print("\n")
			if ddata=="end": break

def clie(obj):
	with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
		while True:
			message=input()
			reply=obj.getq()
			if reply=='null': data=message
			else : data="reply to message:'"+str(reply)+"\n"+message
			if reply=="end":data="end"
			data=data.encode()
			if obj.getclientip()=='':
				obj.setclientip(input("Enter ip: "))
			s.sendto(data,(obj.getclientip(),50007))
			if reply=="end":break

#q=Q
d=Details('')
servt=threading.Thread(target=serv, name='servt', args=(d,))
servt.start()
flag=input("Do you want to send a message(y/n): ")
if flag=='y' or flag=='Y':
	d.setclientip(input("Enter ip: "))
cliet=threading.Thread(target=clie, name='cliet', args=(d,))
cliet.start()