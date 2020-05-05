from Node import Seeder
import socket as s
import threading as th
import json
import time
import fade_modern
import random

S=s.socket(s.AF_INET,s.SOCK_DGRAM)
HOST=s.gethostbyname(s.gethostname())
S.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
S.bind((HOST,6969))
peer_threads={}
sockets=[]

ledgobjc = ""
blocqant = ""
ledgname = ""

def mainfunc():
	print("[S.P.E.E.D.] " + "\n" +
		  "[Defaulted file segregation to SPLIT-BY-COUNT]" + "\n" +
		  "[LOG] You have joined the network as a seeder")
	global filename, blocqant, ledgobjc
	filename = str(input("[QUE] Locate the file you wish to send "))
	#blocqant = int(input("[QUE] Enter the block count "))
	blocqant=20
	spltobjc = fade_modern.splmodel(filename)
	spltobjc.spltcunt(blocqant)
	global ledgname
	ledgname = filename + ".sbc"
	ledgfile = open(ledgname,"rb")
	ledgobjc = ledgfile.read()
	ledgfile.close()

"""
INIT FILE NAME AND GENERATE BLOCKS WITH LEDGER
ASK FOR TIER SIZE
"""

seeder=Seeder(3)
# Add functionality to be able to modify this later

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
		answer,ans_addr=soc.recvfrom(40)
		print(answer,ans_addr)
		if(answer):
			seeder.init_connection(addr)
			soc.sendto(json.dumps(seeder.size).encode(),ans_addr)
			flag=refresh(soc,seeder.get_chain(),ans_addr)
			soc.sendto(("LEDGER-"+ledgname).encode(),ans_addr)
			ledger_read_file=open(ledgname,"rb")
			ledger_read=ledger_read_file.read()
			for i in range(len(ledger_read)//1024+1):
				soc.sendto(ledger_read[i*1024:(i+1)*1024],ans_addr)
			soc.sendto(b"LEGDER_OVER",ans_addr)
			ledger_read_file.close()
			#soc.sendto(json.dumps(ledgobjc).encode(),ans_addr)
			soc.sendto(json.dumps(blocqant).encode(),ans_addr)
			"""
			SEND LEDGER SHIT
			"""
			if(not flag):
				#Something error
				print("FLAG ERROR",flag)
		else:
			soc.close()
			print("NO ANSWER FROM PEER")
		time1=time.time()
		while True:
			try:
				"""
				if(time.time()-time1>=5):
					soc.sendto("CHAIN".encode(),ans_addr)
					chain,_=soc.recvfrom(2048)
					chain=chain.decode()
					print(chain,"\t FROM PEER",number)
					seeder.update_chain(chain,number)
					refresh(soc,seeder.get_chain(),ans_addr)
					print("CHAIN UPDATE")
					time1=time.time()
				"""
				#else:
				
				blckordr=set(range(1,blocqant+1)).difference(set(seeder.children_chain[number]['Data']))
				print(blckordr)
				blckinfo = fade_modern.fetcblck(blckordr, ledgname)
				temp=[blckordr,len(blckinfo)]
				soc.sendto(b"INIT BLOCK TRANSFER",ans_addr)
				soc.sendto(json.dumps(temp).encode(),ans_addr)
				for i in range(len(blckinfo)//1024+1):
					soc.sendto(blckinfo[i*1024:(i+1)*1024],ans_addr)
				soc.sendto(b"OVERIDA",ans_addr)
				#soc.sendto(msg,ans_addr)
				print(soc.recvfrom(1024),"IN THREAD",sep="\t")

				soc.sendto("CHAIN".encode(),ans_addr)
				chain,_=soc.recvfrom(2048)
				chain=chain.decode()
				print(chain,"\t FROM PEER",number)
				seeder.update_chain(chain,number)
				refresh(soc,seeder.get_chain(),ans_addr)
				print("CHAIN UPDATE")

				#time.sleep(0.2)
			except OSError as e:
				print(e)
mainfunc()
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
		