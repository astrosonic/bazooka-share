from Node import Seeder
import socket as s
import threading as th
import json

S=s.socket(s.AF_INET,s.SOCK_DGRAM)
HOST=s.gethostbyname(s.gethostname())
S.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
S.bind((HOST,6969))
peer_threads={}
sockets=[]
def seed(soc,addr):
	msg="ORA ORA ORA".encode()
	while True:
		try:
			soc.sendto(msg,addr)
			print(soc.recvfrom(1024),addr,"IN THREAD",sep="\t")
			time.sleep(1)
		except:
			pass
while True:
	thread=[]
	try:
		data,addr=S.recvfrom(1024)
		print(data,addr,"IN MAIN",sep="\t")
		if(addr not in peer_threads.keys()):
			sockets.append(s.socket(s.AF_INET,s.SOCK_DGRAM))
			sockets[-1].setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
			thread.append(th.Thread(target=seed,args=(sockets[-1],addr,)))
			thread[-1].start()
	except:
		pass
		