import sys
import socket
import threading
from queue import Queue
import sounddevice as sd
import soundfile as sf




def callback(indata, outdata, frames, time, status):
	if qinmic.full():
		#print("\r[callback] qinmic overflow.",end="")
		qinmic.get_nowait()
	qinmic.put_nowait(indata[:])
	if qplay.empty():
		#print("\r[callback] qplay underflow.",end="")
		odata=b'\x00'*len(outdata)
	else:
		odata=qplay.get_nowait()
	if len(odata) < len(outdata):
		outdata[:len(odata)] = odata
		outdata[len(odata):] = b'\x00' * (len(outdata) - len(odata))
	outdata[:]=odata




def stre(qplay,qinmic):
	event = threading.Event()
	stream = sd.RawStream(samplerate=8000, blocksize=1024, channels=1, dtype='int16', callback=callback, finished_callback=event.set)
	with stream:
		event.wait()




def beep(qplay):
	global beepdata,beepfs
	while qplay.empty():
		sd.play(beepdata, beepfs)
		sd.wait()




def serv(qplay):
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		s.bind(('',50007))
		global ip
		while True:
			data, addr = s.recvfrom(2048)
			if ip!=addr[0]: 
				ip=addr[0]
			qplay.put_nowait(data)
			if data==b'end':
				print("                                        call ended.\n                                         write [end] to exit..\n                                        ")
				return




def clie(qinmic):
	global ip
	with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
		if not qinmic.empty():
			temp1=qinmic.get_nowait()
			with qinmic.mutex:
				qinmic.queue.clear()
			qinmic.put_nowait(temp1)
		while True:
			try:
				if not qinmic.empty():
					temp=qinmic.get_nowait()
					if ip!='':
						s.sendto(temp,(ip,50007))
			except:
				nothing()
				#print("",end="")
				#print("\r[clie] host unreachable.",end="")
				
def nothing():
	return




beepdata, beepfs = sf.read('A168000.wav', dtype='int16')
ip=''
qplay=Queue()
qinmic=Queue()
flag=input("                                        Do you want to make a call(y/n):\n                                        ")
if flag=='y' or flag=='Y':
	ip=input("                                        Enter ip:\n                                        ")
servt=threading.Thread(target=serv, name='servt', args=(qplay,), daemon=True)
servt.start()
beept=threading.Thread(target=beep, name='beept', args=(qplay,), daemon=True)
beept.start()
stret=threading.Thread(target=stre, name='stret', args=(qplay,qinmic), daemon=True)
stret.start()
cliet=threading.Thread(target=clie, name='cliet', args=(qinmic,), daemon=True)
cliet.start()
while True:
	if input("                                        Write [end] anytime to end program:\n                                        ")=='end' :
		if not ip=='':
			with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
				endd=b'end'
				try:
					s.sendto(endd,(ip,50007))
				except: break
		sys.exit()