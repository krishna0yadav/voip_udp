import sys
import socket
import threading
#import os
from queue import Queue
import sounddevice as sd
import soundfile as sf




def callback(indata, outdata, frames, time, status):
	
	#print("callback started\n")
	#print(len(outdata[:]))
	#assert frames == args.blocksize
	
	if status.output_underflow:
		print('Output underflow: increase blocksize?', file=sys.stderr)
		raise sd.CallbackAbort
		assert not status
	try:
		qinmic.put_nowait(indata[:])
	except queue.Full:
		print('Buffer is full: increase buffersize?', file=sys.stderr)
		raise sd.CallbackAbort
	try:
		if qplay.empty():
			
			#qplay.put_nowait(open("A.wav",'rb').read())
			#temp2 = qplay.get_nowait()
			#print(len(temp2))
			#odata=temp2
			
			odata=b'\x00'*len(outdata)
		else:
			odata = qplay.get_nowait()
	except queue.Empty:
		print('Buffer is empty: increase buffersize?', file=sys.stderr)
		raise sd.CallbackAbort
	if len(odata) < len(outdata):
		outdata[:len(odata)] = odata
		outdata[len(odata):] = b'\x00' * (len(outdata) - len(odata))
		raise sd.CallbackStop
	else:
		outdata[:] = odata




def stre(qplay,qinmic):
	
	#while qplay.empty():
	
	with qinmic.mutex:
		qinmic.queue.clear()
	event = threading.Event()
	stream = sd.RawStream(samplerate=8000, blocksize=1024, device=None, channels=1, dtype='int16', callback=callback, finished_callback=event.set)
	with stream:
		event.wait()




def beep(qplay):
	data, fs = sf.read('A.wav', dtype='int16')
	while qplay.empty():
		sd.play(data, fs)
		sd.wait()




def serv(obj,qplay):
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		s.bind(('',50007))
		while True:
			data, addr = s.recvfrom(2048)
			clientip=''
			while not obj.empty():
				clientip=obj.get()
			if clientip!=addr[0]: 
				
				#print('Connected by', addr)
				
				obj.put(addr[0])
			else:
				obj.put(clientip)
				
			#ddata=data.decode()
			#obj.putq(ddata)
			
			qplay.put_nowait(data)
			
			#print(ddata)
			#print(type(ddata))
			#print(len(ddata))
			#print(str(ddata)=="end")
			#print("\n")
			
			if data==b'end':
				print("call ended.\n write [end] to exit..\n")
				return




def clie(obj,qinmic):
	while obj.empty():
		_=''
	with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
		temp1=qinmic.get()
		with qinmic.mutex:
			qinmic.queue.clear()
		qinmic.put_nowait(temp1)
		while True:
			
			#message=input()
			#reply=obj.getq()
			#if reply=='null': data=message
			#else : data="reply to message:'"+str(reply)+"\n"+message
			#if reply=="end":data="end"
			#data=message
			#data=data.encode()
			#if obj.empty():
				#temp=input("Enter ip: ")
			#else:
			
			while not obj.empty():
					temp=obj.get()
			obj.put(temp)
			try:
				s.sendto(qinmic.get_nowait(),(temp,50007))
			except:
				print("error")
				continue
			#if message=="end": return
			#if reply=="end":break




d=Queue()
qplay=Queue()
qinmic=Queue()
servt=threading.Thread(target=serv, name='servt', args=(d,qplay), daemon=True)
servt.start()
beept=threading.Thread(target=beep, name='beept', args=(qplay,), daemon=True)
beept.start()
stret=threading.Thread(target=stre, name='stret', args=(qplay,qinmic), daemon=True)
stret.start()
flag=input("Do you want to make a call(y/n): ")
if flag=='y' or flag=='Y':
	if d.empty():
		d.put(input("Enter ip: "))
cliet=threading.Thread(target=clie, name='cliet', args=(d,qinmic), daemon=True)
cliet.start()
while True:
	if input("Write [end] anytime to end program:\n")=='end' :
		if not d.empty():
			with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
				temp=''
				while not d.empty():
					temp=d.get()
				d.put(temp)
				endd=b'end'
				try:
					s.sendto(endd,(temp,50007))
				except: break
					
		#stret.exit()
		#cliet.exit()
		#servt.exit()
		
		sys.exit()









