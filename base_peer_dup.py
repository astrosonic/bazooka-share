from Node import Peer
import socket as s
import threading as th
import json
import sys
import time


S=s.socket(s.AF_INET,s.SOCK_DGRAM)
HOST=s.gethostbyname(s.gethostname())

Seeder=(HOST,6970)

S.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)

P=s.socket(s.AF_INET,s.SOCK_DGRAM)
P.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
P.bind((HOST,6971))

def seeder():
	msg="MUDA MUDA MUDA".encode()
	data,addr=S.recvfrom(1024)
	while True:
		try:
			S.sendto(msg,addr)
			ans=S.recvfrom(1024)
			print(ans)
			time.sleep(1)
		except:
			pass

def peer(data,addr,soc):
	while True:
		try:
			soc.sendto("ORA".encode(),addr)
			print(soc.recvfrom(1024))
			time.sleep(1)
		except:
			pass




seeder_thread=th.Thread(target=seeder)
peer_threads={}
sockets=[]
"""
FIND SEEDER SHIT
"""
try:
	S.sendto("Connect".encode(),Seeder)
	seeder_thread.start()
	seeder_thread_active=True
except:
	pass
while True:
	try:
		data,addr=P.recvfrom(1024)
		if(addr[0] not in peer_threads.keys()):
			sockets.append(s.socket(s.AF_INET,s.SOCK_DGRAM))
			sockets[-1].setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
			peer_threads[addr[0]]=th.Thread(target=peer,args=(data,addr,sockets[-1],))
			peer_threads[addr[0]].start()
	except:
		pass
