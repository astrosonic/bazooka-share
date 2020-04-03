from Node import Seeder
import socket as s
import threading as th
import json
import time

S=s.socket(s.AF_INET,s.SOCK_DGRAM)
HOST=s.gethostbyname(s.gethostname())
S.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
S.bind((HOST,6969))
peer_threads={}
sockets=[]


seeder=Seeder(3)

def refresh(soc,chain,addr):
	try:
		soc.sendto(json.dumps(chain).encode(),addr)
		return True
	except OSError as e:
		return False


def seed(soc,addr):
	msg="ORA ORA ORA".encode()
	flag,number=seeder.allocate_number()
	soc.sendto(json.dumps(number).encode(),addr)
	print(soc)
	if(type(number)==int):
		answer,ans_addr=soc.recvfrom(40)###NEED ANSWERING IP
		print(answer,ans_addr)
		if(answer):
			seeder.init_connection(addr)
			soc.sendto(json.dumps(seeder.size).encode(),ans_addr)
			flag=refresh(soc,seeder.get_chain(),ans_addr)
			if(not flag):
				#Something error
				print("FLAG ERROR",flag)
		else:
			soc.close()
			print("NO ANSWER FROM PEER")
		time1=time.time()
		while True:
			try:
				soc.sendto(msg,ans_addr)
				print(soc.recvfrom(1024),ans_addr,"IN THREAD",sep="\t")
				time.sleep(0.1)
				if(time.time()-time1>=5):
					soc.sendto("CHAIN".encode(),ans_addr)
					refresh(soc,seeder.get_chain(),ans_addr)
					print("CHAIN UPDATE")
					time1=time.time()
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
		
