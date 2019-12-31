'''
Peer ka hai ye
'''

from Node import Peer
import socket as s
import threading as th
import json

HOST,PORT=str(input()).split(" ")
PORT=int(PORT)
P=s.socket(s.AF_INET,s.SOCK_STREAM)
P.connect((HOST,PORT))
S=s.socket(s.AF_INET,s.SOCK_STREAM)
HOST=s.gethostbyname(s.gethostname())
S.bind((HOST,7000))
S.listen()

temp=P.recv(20)
seeder_ip=json.loads(temp)
print(seeder_ip)
P.send(b'1')
while type(seeder_ip)!=int:
	P.connect((seeder_ip[0],seeder_ip[1]))
	seeder_ip = json.loads(P.recv(20))
	P.send(b'1')
size=P.recv(1).decode()
peer=Peer(int(size),seeder_ip)
try:
	
	temp=P.recv(1024)
	print(temp)
	peer.peer_chain=json.loads(temp)
	P.send(b'1')
	temp=P.recv(1024)
	print(temp)
	peer.ip_table=json.loads(temp)
	P.send(b'Y')
except OSError as e:
	print(e)
while True:
	try:
		P.recv(1)
		P.send(b'1')	
	except KeyboardInterrupt as e:
		break


