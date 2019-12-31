'''
Seeder Code hai ye
'''


from Node import Seeder
import socket as s
import threading as th
import json

seeder=Seeder(5)
S=s.socket(s.AF_INET,s.SOCK_STREAM)
HOST=s.gethostbyname(s.gethostname())
S.bind((HOST,6969))
S.listen()

def serve(conn,addr):
	flag,number=seeder.allocate_number()
	conn.send(json.dumps(number).encode())
	conn.recv(1)
	if(flag):
		print("Tier 1")
		seeder.init_connection(addr)
		chain,table=seeder.get_chain()
		conn.send(str(seeder.size).encode())
		conn.send(chain)
		conn.recv(1)
		conn.send(table)
		ack=conn.recv(1)
		print(ack)
		'''
		File SHIT
		'''
		while True:
			try:
				conn.send(b'1')
				conn.recv(1)
			except KeyboardInterrupt:
				break
	else:
		print("other Tier")




thread=[]
while True:
	try:
		conn,addr=S.accept()
		thread.append(th.Thread(target=serve,args=(conn,addr,)))
		thread[-1].start()
	except KeyboardInterrupt as e:
		break