# SPLITTER WITH CLASSES
# Dec 18, 2019 [20:33 IST]

'''
Advantages :
1. Better object implementation
2. Better collection and dispersal of useless variables
3. Better out of memory exception handling

Disadvantages :
1. Slightly slower than the actual implementation
2. Requires a driver script for invoking functions
3. Cannot run from the get-go with basic imports

Changes :
1. Removed splitting by size function
2. Read Ledger function disposed off in favour of intrinsic init call
3. Reduced overhead due to reading ledger only once for 
    3.1. Displaying audit
    3.2. Block integrity check
    3.3. Reading from file
4. Removed ledger list metadata in favour of a set of three class variables
5. Reduced split function to one-third of instruction length

Bugs
1. New instance of join model needs to be created on joining every new ledger
'''

import hashlib, sqlite3, os, time
from colorama import init, Fore, Style
init()

class splmodel:
    def __init__(self,filename,partcunt):
        try:
            actifile=open(filename,"rb")
            self.actibuff=actifile.read()
            actifile.close()
            self.filename=filename
            self.partcunt=partcunt
            self.buffsize=len(self.actibuff)
        except FileNotFoundError:
            print(Fore.RED+"[ERROR OCCURRED]"+Fore.RESET+"\n"+\
                "Splitting operation could not be initiated!\n"+\
                "The requested file is not accessible. Make sure that - \n"+\
                "- You have sufficient privileges to the directory \n"+
                "- The path you have provided is correct \n"+
                "- The file is indeed present in the given path")

    def nogenten(self,numvalue):
        strvalue=""
        if numvalue<10:
            strvalue="0"+str(numvalue)
        else:
            strvalue=str(numvalue)
        return strvalue
    def spltsort(self):
            if (self.partcunt>=10 and self.partcunt<10000):
                if (self.partcunt>self.buffsize):
                    print(Fore.RED+"[ERROR OCCURRED]"+Fore.RESET+"\n"+\
                        "Splitting operation could not be initiated!\n"+\
                        "The number of parts is greater than the byte size of your file")
                else:
                    poselist=self.allcbyte()
                    hashlist,sizelist,cuntlist={},{},{}
                    totlprog=0
                    print(Fore.CYAN+"[PROTEXON SPLITTER by t0xic0der]"+Fore.RESET+"\n"+\
                        "File name   : "+self.filename+"\n"+\
                        "File size   : "+str(self.buffsize)+" bytes\n"+\
                        "Part count  : "+str(self.partcunt)+" parts\n"+\
                        "Ledger name : "+self.filename+".ldg\n")
                    print(Fore.CYAN+"[STARTING SPLIT OPERATION]"+Fore.RESET)      
                    startsec=time.time()
                    for i in range(1,self.partcunt+1):
                        if self.partcunt>=10 and self.partcunt<=100:
                            blocname=self.filename+"."+self.nogenten(i)
                            cuntlist[blocname]=self.nogenten(i)
                        elif self.partcunt>=100 and self.partcunt<=1000:
                            blocname=self.filename+"."+self.nogenhun(i)
                            cuntlist[blocname]=self.nogenhun(i)
                        elif self.partcunt>=1000 and self.partcunt<10000:
                            blocname=self.filename+"."+self.nogenthd(i)
                            cuntlist[blocname]=self.nogenthd(i)
                        blocbuff=self.actibuff[poselist[i-1]:poselist[i]]
                        hashlist[blocname]=hashlib.sha512(blocbuff).hexdigest()
                        sizelist[blocname]=len(blocbuff)
                        blocfile=open(blocname,"wb")
                        blocfile.write(blocbuff)
                        blocfile.close()
                        totlprog=totlprog+(100/self.partcunt)
                        print(str(cuntlist[blocname])+"\t"+str(blocname)+ " created!\t"+Style.DIM+str(sizelist[blocname])+" bytes\t"+Style.RESET_ALL+str(hashlist[blocname])+"\t"+Style.DIM+str(totlprog)[0:4]+"% completed"+Style.RESET_ALL)
                    self.makeldgr(hashlist,sizelist,cuntlist)
                    endinsec=time.time()
                    totatime=str(endinsec-startsec).split(".")[0]+"."+str(endinsec-startsec).split(".")[1][0:2]
                    print("\n"+Fore.CYAN+"[SPLIT OPERATION COMPLETED]"+Fore.RESET+"\n"+\
                        "Parts created  : "+str(self.partcunt)+" parts \n"+\
                        "Ledger created : "+str(self.filename)+".ldg \n"+\
                        "Time taken     : "+str(totatime)+" seconds \n")
            else:
                print(Fore.RED+"[ERROR OCCURRED]"+Fore.RESET+"\n"+\
                    "Splitting operation could not be initiated!\n"+\
                    "We do not recommend splitting in this many parts")
    def nogenhun(self,numvalue):
        strvalue=""
        if numvalue<10:
            strvalue="00"+str(numvalue)
        elif numvalue>=10 and numvalue<100:
            strvalue="0"+str(numvalue)
        else:
            strvalue=str(numvalue)
        return strvalue

    def nogenthd(self,numvalue):
        strvalue=""
        if numvalue<10:
            strvalue="000"+str(numvalue)
        elif numvalue>=10 and numvalue<100:
            strvalue="00"+str(numvalue)
        elif numvalue>=100 and numvalue<1000:
            strvalue="0"+str(numvalue)
        else:
            strvalue=str(numvalue)
        return strvalue
    
    def allcbyte(self):
        sizelist,poselist=[],[]
        if self.buffsize%self.partcunt==0:
            genptsiz=self.buffsize//self.partcunt
            for i in range(0,self.partcunt):
                sizelist.append(genptsiz)
        else:
            genptsiz=self.buffsize//self.partcunt
            endptsiz=self.buffsize%self.partcunt
            sizelist.append(genptsiz+endptsiz)
            for i in range(0,self.partcunt-1):
                sizelist.append(genptsiz)
        poselist.append(0)
        for i in range(1,self.partcunt+1):
            poselist.append(sum(sizelist[0:i]))
        return poselist

    def makeldgr(self,hashlist,sizelist,cuntlist):
        ldgrname=self.filename+".ldg"
        actifile=open(ldgrname,"wb")
        actifile.close()
        ldgrbase=sqlite3.connect(ldgrname)
        ldgrbase.execute("create table ldgrbase (partnumb text primary key not null, partname text not null, partsize int not null, sha512dg text not null);")
        for i in hashlist.keys():
            querystr="insert into ldgrbase (partnumb, partname, partsize, sha512dg) values ('"+str(cuntlist[i])+"', '"+str(i)+"', "+str(sizelist[i])+", '"+str(hashlist[i])+"')"
            ldgrbase.execute(querystr)
        ldgrbase.commit()
        ldgrbase.close()

    def spltsort(self):
            if (self.partcunt>=10 and self.partcunt<10000):
                if (self.partcunt>self.buffsize):
                    print(Fore.RED+"[ERROR OCCURRED]"+Fore.RESET+"\n"+\
                        "Splitting operation could not be initiated!\n"+\
                        "The number of parts is greater than the byte size of your file")
                else:
                    poselist=self.allcbyte()
                    hashlist,sizelist,cuntlist={},{},{}
                    totlprog=0
                    print(Fore.CYAN+"[PROTEXON SPLITTER by t0xic0der]"+Fore.RESET+"\n"+\
                        "File name   : "+self.filename+"\n"+\
                        "File size   : "+str(self.buffsize)+" bytes\n"+\
                        "Part count  : "+str(self.partcunt)+" parts\n"+\
                        "Ledger name : "+self.filename+".ldg\n")
                    print(Fore.CYAN+"[STARTING SPLIT OPERATION]"+Fore.RESET)      
                    startsec=time.time()
                    for i in range(1,self.partcunt+1):
                        if self.partcunt>=10 and self.partcunt<=100:
                            blocname=self.filename+"."+self.nogenten(i)
                            cuntlist[blocname]=self.nogenten(i)
                        elif self.partcunt>=100 and self.partcunt<=1000:
                            blocname=self.filename+"."+self.nogenhun(i)
                            cuntlist[blocname]=self.nogenhun(i)
                        elif self.partcunt>=1000 and self.partcunt<10000:
                            blocname=self.filename+"."+self.nogenthd(i)
                            cuntlist[blocname]=self.nogenthd(i)
                        blocbuff=self.actibuff[poselist[i-1]:poselist[i]]
                        hashlist[blocname]=hashlib.sha512(blocbuff).hexdigest()
                        sizelist[blocname]=len(blocbuff)
                        blocfile=open(blocname,"wb")
                        blocfile.write(blocbuff)
                        blocfile.close()
                        totlprog=totlprog+(100/self.partcunt)
                        print(str(cuntlist[blocname])+"\t"+str(blocname)+ " created!\t"+Style.DIM+str(sizelist[blocname])+" bytes\t"+Style.RESET_ALL+str(hashlist[blocname])+"\t"+Style.DIM+str(totlprog)[0:4]+"% completed"+Style.RESET_ALL)
                    self.makeldgr(hashlist,sizelist,cuntlist)
                    endinsec=time.time()
                    totatime=str(endinsec-startsec).split(".")[0]+"."+str(endinsec-startsec).split(".")[1][0:2]
                    print("\n"+Fore.CYAN+"[SPLIT OPERATION COMPLETED]"+Fore.RESET+"\n"+\
                        "Parts created  : "+str(self.partcunt)+" parts \n"+\
                        "Ledger created : "+str(self.filename)+".ldg \n"+\
                        "Time taken     : "+str(totatime)+" seconds \n")
            else:
                print(Fore.RED+"[ERROR OCCURRED]"+Fore.RESET+"\n"+\
                    "Splitting operation could not be initiated!\n"+\
                    "We do not recommend splitting in this many parts")

class jinmodel:
    def __init__(self,filename):
        self.ldgrname=filename+".ldg"
        self.filename=filename
        self.hashlist={}
        self.sizelist={}
        self.cuntlist={}
        try:
            ldgrbase=sqlite3.connect(self.ldgrname)
            dbcursor=ldgrbase.execute("select * from ldgrbase")
            for row in dbcursor:
                self.cuntlist[row[1]]=row[0]
                self.sizelist[row[1]]=row[2]
                self.hashlist[row[1]]=row[3]
            ldgrbase.close()
        except FileNotFoundError:
            print(Fore.RED+"[ERROR OCCURRED]"+Fore.RESET+"\n"+\
                "The ledger could not be read properly!\n"+\
                "Make sure you have \n"+\
                "- Privileges to access the ledger file \n"+\
                "- the ledger file present in the directory \n"+\
                "- been pointing towards to right location")

    def displdgr(self):
        print(Fore.CYAN+"[LEDGER CONTENTS]"+Fore.RESET)
        for i in self.cuntlist.keys():
            print("Part count  : "+str(self.cuntlist[i])+"\n"+\
                  "Part name   : "+str(i)+"\n"+\
                  "Part size   : "+str(self.sizelist[i])+"\n"+\
                  "SHA512 hash : "+str(self.hashlist[i]))

    def pthealth(self):
        failcunt,passcunt=0,0
        chekcunt,misscunt=0,0
        startsec=time.time()
        for i in self.cuntlist.keys():
            chekcunt+=1
            try:
                actifile=open(i,"rb")
                actibuff=actifile.read()
                actifile.close()
                preshash=hashlib.sha512(actibuff).hexdigest()
                if preshash==self.hashlist[i]:
                    passcunt+=1
                else:
                    failcunt+=1
            except FileNotFoundError:
                misscunt+=1
        endinsec=time.time()
        totatime=str(endinsec-startsec).split(".")[0]+"."+str(endinsec-startsec).split(".")[1][0:2]
        joinable=False
        if chekcunt==passcunt:
            joinable=True
        print(Fore.CYAN+"[BLOCK INTEGRITY CHECK]"+"\n"+Fore.RESET+\
            "Total checks          : "+str(chekcunt)+"\n"+\
            "Files with wrong hash : "+str(failcunt)+"\n"+\
            "Files with match hash : "+str(passcunt)+"\n"+\
            "Files missing         : "+str(misscunt)+"\n"+\
            "Time taken for check  : "+str(totatime)+" seconds\n"+\
            "Integrity result      : "+str(joinable)+"\n")
        return joinable

    def joincunt(self):
        totlpart=int(list(self.cuntlist.values())[-1])
        totlprog=0
        if (self.pthealth()):
            print(Fore.CYAN+"[STARTING JOIN OPERATION]"+Fore.RESET)
            startsec=time.time()
            actibuff=b""
            for i in self.cuntlist.keys():
                blocfile=open(i,"rb")
                blocbuff=blocfile.read()
                blocfile.close()
                os.system("rm "+i)
                actibuff+=blocbuff
                totlprog=totlprog+100/totlpart
                print("Joined "+i+" to parent file "+Style.DIM+"("+str(totlprog)[0:4]+"% completed)"+Style.RESET_ALL)
            actifile=open(self.filename,"wb")
            actifile.write(actibuff)
            actifile.close()
            os.system("rm "+self.ldgrname)
            endinsec=time.time()
            totatime=str(endinsec-startsec).split(".")[0]+"."+str(endinsec-startsec).split(".")[1][0:2]
            print("\n"+Fore.CYAN+"[JOIN OPERATION COMPLETED]"+Fore.RESET+"\n"+\
                "Time taken : "+totatime+" seconds"+Fore.RESET)
        else:
            print(Fore.RED+"[ERROR OCCURRED]"+Fore.RESET+"\n"+\
                "Join procedure could not be initiated!\n"+\
                "Some parts are missing or corrupted - Download them again")