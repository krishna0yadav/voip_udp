# voip_udp awesome
Project selection and requirement gathering might took a week,
so, project started on 22 sept 2019 approx.

it might took a week in design and analysis,
so, design of project started on 1 oct 2019 approx.

first python file developed on 9 october 2019
server.py made on 9 oct
client.py made on 11 oct
main1.py, main2.py, main3.py made on 15 oct
main4.py made on 18 oct
main5.py, main6.py, main7.py, main8.py made on 22 oct

main8.py is the final version of the project
project finished on 22 oct 2019

didn't remember presentation date, maybe around a week after completion

Note: I'm totally sure about the code's dates 'cause it is stored locally, rest of the dates are a rough approximation.

!!Pasting final code below!!
=========================================================================

import sys
import socket
import threading
from queue import Queue
import sounddevice as sd
import soundfile as sf




def callback(indata, outdata, frames, time, status):	# responsible for playing audio streams from "playing queue"
	try:												# and for putting mic data from system to "mic queue"
		
		if qinmic.full():
			qinmic.get_nowait()
		qinmic.put_nowait(indata[:]) #puts 'mic data to qinmic(mic queue)'
		if qplay.empty():
			odata=b'\x00'*len(outdata)
		else:
			odata=qplay.get_nowait() 	#retreives 'playing queue' data
		if len(odata) < len(outdata):
			outdata[:len(odata)] = odata
			outdata[len(odata):] = b'\x00' * (len(outdata) - len(odata))
		outdata[:]=odata				#plays 'playing queue' data
	except:
		nothing()




def stre(qplay,qinmic): # handling audio streams to and from system(mic and speaker) also uses callback function defined above
	try:
		
		event = threading.Event()
		stream = sd.RawStream(samplerate=8000, blocksize=1024, channels=1, dtype='int16', callback=callback, finished_callback=event.set)
		with stream:
			event.wait()
	except:
		nothing()




def beep(qplay): # just for playing a background beep until our call connects
	try:
		
		global beepdata,beepfs
		while qplay.empty():
			sd.play(beepdata, beepfs)
			sd.wait()
	except:
		nothing()




def serv(qplay): # responsible for recieving audio data from from other user and putting it to the "playing queue"
	try:
		
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			s.bind(('',50007))
			global ip
			while True:
				data, addr = s.recvfrom(2048) # recieving audio data from the other user
				if ip!=addr[0]: 
					ip=addr[0]
				qplay.put_nowait(data) # putting recieved data to the "playing queue"
				if data==b'end':
					print("                                        call ended.\n                                         write [end] to exit..\n                                        ")
					return
	except:
		nothing()




def clie(qinmic): #responsible for taking microphone data from "mic queue" and sending it to the other device.
	try:
		
		global ip
		with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
			if not qinmic.empty():			#this 'if' part is responsible for clearing the mic queue
				temp1=qinmic.get_nowait()	#prior to using it
				with qinmic.mutex:
					qinmic.queue.clear()
				qinmic.put_nowait(temp1)
			while True:
				try:
					if not qinmic.empty():
						temp=qinmic.get_nowait() # getting mic data from qinmic(a queue)
						if ip!='':
							s.sendto(temp,(ip,50007)) # sending data to other device
				except:
					nothing()
	except:
		nothing()




def nothing():
	return




try:
	
	beepdata, beepfs = sf.read('A168000.wav', dtype='int16') #getting beep audio
	ip=''
	qplay=Queue() # for storing data to be played on speaker
	qinmic=Queue() # for storing data recieved from our microphone
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
		if input("                                        Write [end] anytime to end program:\n                                        ")=='end' : # for ending our program
			if not ip=='':
				with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
					endd=b'end'
					try:
						s.sendto(endd,(ip,50007))
					except: break
			sys.exit()
except:
	nothing()
