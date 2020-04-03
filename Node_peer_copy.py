from Node import Peer
import socket as s
import threading as th
import json
import sys
import time



#S=s.socket(s.AF_INET,s.SOCK_DGRAM)
HOST=s.gethostbyname(s.gethostname())

#S.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)


P=s.socket(s.AF_INET,s.SOCK_DGRAM)
P.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
P.bind((HOST,6970))

peer_obj=Peer()
def seeder(S,ip,number):
	print("INSIDE SEEDER THREAD",ip,number,sep='\t')
	msg="MUDA MUDA MUDA".encode()
	S.sendto("I AM HERE!".encode(),ip)
	size,_=S.recvfrom(1024)
	print(size,"SIZE")
	size=json.loads(size)
	peer_obj.update_data(size,number)
	chain,_=S.recvfrom(1024)
	print(chain,"CHAIN")
	while True:
		try:
			ans,_=S.recvfrom(1024)
			print(ans)
			if(ans=="CHAIN".encode()):
				chain,_=S.recvfrom(2048)
				print(chain)
			S.sendto(msg,ip)
			time.sleep(0.1)
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




peer_threads={}
sockets=[]
"""
FIND SEEDER SHIT
"""
Seeder=(HOST,6969)
seeder_soc=s.socket(s.AF_INET,s.SOCK_DGRAM)
seeder_soc.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
try:
	P.sendto("Connect".encode(),Seeder)
	data,ip=P.recvfrom(1024)
	data=json.loads(data)
	print(data,"Seeder answer loaded",type(data))
	while type(data)!=int:
		P.sendto("Connect".encode(),data)
		data,ip=P.recvfrom(1024)
		data=json.loads(data)
	seeder_thread=th.Thread(target=seeder,args=(seeder_soc,ip,data,))
	seeder_thread.start()
	seeder_thread_active=True
except:
	pass
print("SEEDER DONE")
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
