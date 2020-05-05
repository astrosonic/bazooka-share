from Node import Peer
import socket as s
import threading as th
import json
import sys
import time
import random




HOST=s.gethostbyname(s.gethostname())


P=s.socket(s.AF_INET,s.SOCK_DGRAM)
P.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
P.bind((HOST,6970))

peer_obj=Peer()

def inter_peer(seeder_chain,soc,i,ip):
	print(seeder_chain,ip,"IN INTER_PEER",sep="\t")
	ip=tuple(ip)
	"""
	SECURITY CHECKING AND PEER AUTHENTICATION
	"""
	try:
		soc.sendto(json.dumps(peer_obj.number).encode(),ip)
		data,ip=soc.recvfrom(1024)
	except:
		print("Error connecting to peer",ip)
	
	msg=b"DORA RORA RORA"
	while True:
		try:
			soc.sendto(msg,ip)
			print(soc.recvfrom(1024),"FROM CHOTU "+str(i),sep="\t")
		except OSError as e:
			print("THREAD ERROR OCCURED",e)
			break
	"""
	THE BELOW IS ROUGH FOR INTER-PEER COMMUNICATION
	IGNORE IT
	"""
	while True:
		try:
			"""
			GET TOTAL BLOCKS NUMBER
			"""
			number=10
			required_blocks=set(range(number)).difference(seeder_chain["Data"])
			req=random.choice(required_blocks)

			soc.sendto(str(req).encode(),ip)

			seeder_chain["Data"].append(req)

			data,_=soc.recvfrom(1024)
			data=data.decode()
			"""
			Data will contain block number
			"""
			while data!="OVERIDA".encode():
				try:
					data,_=soc.recvfrom(1024)
				except:
					print("FIle sending error. Fix SHIT")
			"""
			LOAD FILE INTO VARIABLE
			"""
			file=b"DORA RARA RARA"
			ctr=int(len(block)/1024)+1

			"""
			FURTHER PART OF CHECKING THE BLOCK TRANSFERS
			history=[False]*ctr
			After a block has successfully transfered to the peer, history[block_number]=True
			If error happens the history can be used to resend the block
			"""
			

			while ctr!=0:
				"""
				LOAD BLOCK INTO VARIABLE
				"""
				block=file
				try:
					soc.sendto(block,ip)
				except:
					"""
					ADDING THE ERROR AND INDEX OF ERROR BlOCK IN HISTORY
					"""
					pass

		except:
			pass

def process_chain(chain,soc):
	chain,ip_table=chain["CHAIN"],chain["IP_TABLE"]
	for i in map(str,range(peer_obj.number+1,peer_obj.size+1)):
		if(i not in peer_obj.fellow_peer.keys() and chain[i]['Vac']!=-1):
			peer_obj.fellow_peer[i]=[]
			peer_obj.fellow_peer[i].append(s.socket(s.AF_INET,s.SOCK_DGRAM))
			peer_obj.fellow_peer[i][-1].setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
			peer_obj.fellow_peer[i].append(th.Thread(target=inter_peer,args=(chain[i],peer_obj.fellow_peer[i][0],i,ip_table[int(i)-1],)))
			peer_obj.fellow_peer[i][-1].start()





def seeder(S,ip,number):
	print("INSIDE SEEDER THREAD",ip,number,sep='\t')
	msg="MUDA MUDA MUDA".encode()
	"""
	SECURITY CHECKING AND PRIVATE/PUBIC KEY TRANSFER
	"""
	S.sendto("I AM HERE!".encode(),ip)
	size,_=S.recvfrom(1024)
	print(size,"SIZE")
	size=json.loads(size)
	peer_obj.update_data(size,number)
	chain,_=S.recvfrom(1024)
	chain=json.loads(chain.decode())

	name,_=S.recvfrom(1024)
	if(name[:6]==b"LEDGER"):
		name=name.decode()
		ledger_name=name.split("-")[-1]
		ledger=open(ledger_name,"wb")
		temp,_=S.recvfrom(1024)
		while temp!=b"LEDGER_OVER":
			ledger.write(temp)
			temp,_=S.recvfrom(1024)
	else:
		print("LEDGER ERROR")
		sys.exit()
	#ledger,_=S.recvfrom(1024)
	total_blocks,_=S.recvfrom(1024)
	#print(ledger,"LEDGER")
	print(total_blocks)
	peer_obj.seeder_chain["CHAIN"],peer_obj.seeder_chain["IP_TABLE"]=json.loads(chain[0]),json.loads(chain[1])
	print(peer_obj.seeder_chain,"INITIAL D")
	"""
	RECV LEDGER SHIT
	"""
	
	t1=time.time()
	ctr=0
	while True:
		try:
			data,_=S.recvfrom(1024)
			if(data==b"INIT BLOCK TRANSFER"):
				meta,_=S.recvfrom(1024)
				block_number,length=json.loads(meta.decode())
				print(block_number,length,sep="\t")	
				break
				"""
				GET FILE INFO FROM LEDGER BASED ON BLOCK NUMBER
				"""
				filename=""
				file_obj=open(filename,"wb")
				dat,_=file_obj.recvfrom(1024)
				while dat!=b"OVERDIA":
					file_obj.write(dat)
					dat,_=file_obj.recvfrom(1024)
				file_obj.close()
				"""
				VERIFY FILE CREDENTIALS AND SHIT
				"""
				S.sendto(b"DONE BLOCK NUMBER{0}".format(block_number))

				resp,_=S.recvfrom(1024)
				if(resp==b"CHAIN"):
					S.sendto(json.dumps(peer_obj.seeder_chain["CHAIN"][str(peer_obj.number)]).encode(),ip)
					chain,_=S.recvfrom(2048)
					chain=json.loads(chain.decode())
					peer_obj.seeder_chain["CHAIN"],peer_obj.seeder_chain["IP_TABLE"]=json.loads(chain[0]),json.loads(chain[1])
					print(peer_obj.seeder_chain,"NEW CHAIN")
					process_chain(peer_obj.seeder_chain,S)
					
			#ans,_=S.recvfrom(1024)
			"""
			HERE IF BLOCK TRANSFER IS COMPLETE THEN CHAIN WILL BE UPDATED
			ADD BLOCK CHECKING PROCEDURE
			eg: block_checking(block_recieved)
			"""
			"""
			if(time.time()-t1>=5):
				peer_obj.seeder_chain["CHAIN"][str(peer_obj.number)]['Data'].append(ctr)
				ctr+=1
				t1=time.time()

			if(ans=="CHAIN".encode()):
				S.sendto(json.dumps(peer_obj.seeder_chain["CHAIN"][str(peer_obj.number)]).encode(),ip)
				chain,_=S.recvfrom(2048)
				chain=json.loads(chain.decode())
				peer_obj.seeder_chain["CHAIN"],peer_obj.seeder_chain["IP_TABLE"]=json.loads(chain[0]),json.loads(chain[1])
				print(peer_obj.seeder_chain,"NEW CHAIN")
				process_chain(peer_obj.seeder_chain,S)
			else:
				


				S.sendto(msg,ip)

				

			THIS COMMENT IS TRASH
			"""



			#time.sleep(0.2)#####REMOVE SLEEP FOR SPEED TESTING
		except OSError as e:
			print(e)

def peer(data,addr,soc):
	"""
	SECURITY CHECKS FOR SEEDER-PEER AUTHENTICATION
	"""
	msg=b"DORA RORA RORA"
	while True:
		try:
			soc.sendto(msg,addr)
			print(soc.recvfrom(1024))
			time.sleep(1)
		except:
			break




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
		data=json.loads(data.decode())
		print(data,type(data),sep="\t")
		if(addr not in peer_obj.fellow_peer.keys() and type(data)==int): #### IF INT THEN FELLOW PEER
			"""
			IMPLEMENT PEER_OBJ.FELLOW_PEER SHIT AS DONE ABOVE FOR PEER AND ENABLE COMMUNICATION
			"""
			print("FELLOW_PEER")
			socketo=s.socket(s.AF_INET,s.SOCK_DGRAM)
			socketo.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR,1)
			peer_thread=th.Thread(target=peer,args=(data,addr,socketo,))
			peer_thread.start()
			peer_obj.fellow_peer[data]=[socketo,peer_thread]
		if(addr[0] not in peer_obj.fellow_peer.keys() and type(data)==str):##### IF STR THEN DOWN LEVEL PEER
			print("DOWN LEVEL PEER")

	except OSError as e:
		print(e)
		pass



"""
NOTES FOR FUTURE IMPLEMENTATION


1. Add break statement at the end of except statement in thread
2. Implement seeder part for peer objects
3. Implement peer block transfers for peer-peer connection.
"""