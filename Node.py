import json

class JsonError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return 'Invalid Chain input'


class Seeder():
    def __init__(self,size):
        self.size=size
        self.number=0
        self.children_chain={}
        self._init_chain(self.children_chain,size)
        self.ip_table=['0']*size
        
    def _init_chain(self,chain,size):
        for i in range(1,size+1):
            chain[i]={'Data':[],'Vac':-1}
    
    def allocate_number(self):
        try:
            index=self.ip_table.index('0')
            self.number+=1
            return [True,self.number]
        except:
            temp=min(self.children_chain,key=lambda x: self.children_chain[x]['Vac'])
            return [False,self.ip_table[temp-1]]

    def init_connection(self,ip):
        try:
            self.ip_table[self.number-1]=ip
            self.children_chain[self.number]['Vac']=1
            return True
        except:
            return False

    def update_chain(self,block,number):
        try:
            self.children_chain[number]=json.loads(block)
        except Exception as e:
            raise JsonError

    def get_chain(self):
        return [json.dumps(self.children_chain),json.dumps(self.ip_table)]


class Peer(Seeder):

    def __init__(self):
        self.fellow_peer={}
        self.seeder_chain={}

    def update_data(self,size,number):
        super().__init__(size)
        self.number=number
        
    def init_peer_chain(self,chain):
        "Requires decoded list of chain"
        self.peer_chain=chain[0]
        self.peer_ip=chain[1]


    def send_block(self):
        return json.dumps(self.peer_chain[self.number])

    def update_block(self,data):
        self.peer_chain[self.number]['Data']=data



"""
EXPECTED ERRORS:
1. IP mismatch because ip_table list filling is done seperately without concrete indexing
Agar index 1 hai aur ek sath 2 peers connect ho to har baar possible nahi hai ki jo pehle connect hoga
uska number is same as number-1
"""