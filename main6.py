import sys
import socket
import threading
from queue import Queue
import sounddevice as sd
import soundfile as sf




def callback(indata, outdata, frames, time, status):
	if qinmic.full():
		print("\r[callback] qinmic overflow.",end="")
		qinmic.get()
	qinmic.put_nowait(indata[:])
	if qplay.empty():
		print("\r[callback] qplay underflow.",end="")
		odata=b'\x00'*len(outdata)
	else:
		odata=qplay.get_nowait()
	outdata[:]=odata




def stre(qplay,qinmic):
	#with qinmic.mutex:
	#	print("\r[stre] qinmic clear.",end="")
	#	qinmic.queue.clear()
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
				clientip=addr[0]
			obj.put(clientip)
			qplay.put_nowait(data)
			if data==b'end':
				print("                                        call ended.\n                                         write [end] to exit..\n                                        ")
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
			while not obj.empty():
					temp=obj.get()
			obj.put(temp)
			try:
				s.sendto(qinmic.get_nowait(),(temp,50007))
			except:
				print("\r[clie] host unreachable.",end="")




d=Queue()
qplay=Queue()
qinmic=Queue()
flag=input("                                        Do you want to make a call(y/n):\n                                        ")
if flag=='y' or flag=='Y':
	if d.empty():
		d.put(input("                                        Enter ip:\n                                        "))
servt=threading.Thread(target=serv, name='servt', args=(d,qplay), daemon=True)
servt.start()
beept=threading.Thread(target=beep, name='beept', args=(qplay,), daemon=True)
beept.start()
stret=threading.Thread(target=stre, name='stret', args=(qplay,qinmic), daemon=True)
stret.start()
cliet=threading.Thread(target=clie, name='cliet', args=(d,qinmic), daemon=True)
cliet.start()
while True:
	if input("                                        Write [end] anytime to end program:\n                                        ")=='end' :
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
		sys.exit()