import hashlib, sqlite3, os
from colorama import init, Fore, Style
init()

def nogenten(numvalue):
    strvalue=""
    if numvalue<10:
        strvalue="0"+str(numvalue)
    else:
        strvalue=str(numvalue)
    return strvalue

def nogenhun(numvalue):
    strvalue=""
    if numvalue<10:
        strvalue="00"+str(numvalue)
    elif numvalue>=10 and numvalue<100:
        strvalue="0"+str(numvalue)
    else:
        strvalue=str(numvalue)
    return strvalue

def nogenthd(numvalue):
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

def allcbyte(bytename,partcunt):
    buffsize=len(bytename)
    sizelist,poselist=[],[]
    if buffsize%partcunt==0:
        genptsiz=buffsize//partcunt
        for i in range(0,partcunt):
            sizelist.append(genptsiz)
    else:
        genptsiz=buffsize//partcunt
        endptsiz=buffsize%partcunt
        sizelist.append(genptsiz+endptsiz)
        for i in range(0,partcunt-1):
            sizelist.append(genptsiz)
    poselist.append(0)
    for i in range(1,partcunt+1):
        poselist.append(sum(sizelist[0:i]))
    return poselist

def spltsize(filename,partsize):
    actifile=open(filename,"rb")
    actibuff=actifile.read()
    actifile.close()
    buffsize=len(actibuff)
    hashlist={}
    count=0
    for i in range(0,buffsize,partsize):
        blocname=filename+"-"+str(count)
        blocbuff=actibuff[i:i+partsize]
        hashlist[blocname]=hashlib.sha512(blocbuff).hexdigest()
        blocfile=open(blocname,"wb")
        blocfile.write(blocbuff)
        blocfile.close()
        count+=1
    print("The file has been splitted into blocks of "+str(partsize)+" bytes")
    for i in hashlist.keys():
        print(i+"\t"+hashlist[i])

def makeldgr(filename,hashlist,sizelist,cuntlist):
    ldgrname=filename+".ldg"
    actifile=open(ldgrname,"wb")
    actifile.close()
    ldgrbase=sqlite3.connect(ldgrname)
    ldgrbase.execute("create table ldgrbase (partnumb text primary key not null, partname text not null, partsize int not null, sha512dg text not null);")
    for i in hashlist.keys():
        querystr="insert into ldgrbase (partnumb, partname, partsize, sha512dg) values ('"+str(cuntlist[i])+"', '"+str(i)+"', "+str(sizelist[i])+", '"+str(hashlist[i])+"')"
        ldgrbase.execute(querystr)
    ldgrbase.commit()
    ldgrbase.close()

def readldgr(ldgrname):
    ldgrlist=[]
    try:
        ldgrbase=sqlite3.connect(ldgrname)
        dbcursor=ldgrbase.execute("select * from ldgrbase")
        hashlist,sizelist,cuntlist={},{},{}
        for row in dbcursor:
            cuntlist[row[1]]=row[0]
            sizelist[row[1]]=row[2]
            hashlist[row[1]]=row[3]
        ldgrbase.close()
        ldgrlist=[cuntlist,sizelist,hashlist]
    except:
        ldgrlist=None
    return ldgrlist

def displdgr(filename):
    ldgrname=filename+".ldg"
    ldgrbase=sqlite3.connect(ldgrname)
    dbcursor=ldgrbase.execute("select * from ldgrbase")
    hashlist,sizelist,cuntlist={},{},{}
    for row in dbcursor:
        print("Part count  : "+str(row[0])+"\n"+\
              "Part name   : "+str(row[1])+"\n"+\
              "Part size   : "+str(row[2])+"\n"+\
              "SHA512 hash : "+str(row[3]))
    ldgrbase.close()

def pthealth(cuntlist,sizelist,hashlist):
    failcunt,passcunt=0,0
    chekcunt,misscunt=0,0
    for i in cuntlist.keys():
        chekcunt+=1
        try:
            actifile=open(i,"rb")
            actibuff=actifile.read()
            actifile.close()
            preshash=hashlib.sha512(actibuff).hexdigest()
            if preshash==hashlist[i]:
                passcunt+=1
            else:
                failcunt+=1
        except FileNotFoundError:
            misscunt+=1
    joinable=False
    if chekcunt==passcunt:
        joinable=True
    print(Fore.CYAN+"File health check has been performed"+"\n"+
          Fore.RESET+\
          "Total checks          : "+str(chekcunt)+"\n"+\
          "Files with wrong hash : "+str(failcunt)+"\n"+\
          "Files with match hash : "+str(passcunt)+"\n"+\
          "Files missing         : "+str(misscunt)+"\n"+\
          "Health result         : "+str(joinable)+"\n")
    return joinable

def joincunt(filename):
    ldgrname=filename+".ldg"
    ldgrlist=readldgr(ldgrname)
    if ldgrlist==None:
        print(Fore.RED+"The ledger could not be read properly!"+Fore.RESET+"\n"+\
              "Make sure you have \n"+\
              "- Privileges to access the ledger file \n"+\
              "- the ledger file present in the directory \n"+\
              "- been pointing towards to right location")
    else:
        cuntlist=ldgrlist[0]
        sizelist=ldgrlist[1]
        hashlist=ldgrlist[2]
        totlpart=int(list(cuntlist.values())[-1])
        totlprog=0
        if (pthealth(cuntlist,sizelist,hashlist)):
            print(Fore.CYAN+"Initiating join procedure..."+Fore.RESET)
            actibuff=b""
            for i in cuntlist.keys():
                blocfile=open(i,"rb")
                blocbuff=blocfile.read()
                blocfile.close()
                os.system("rm "+i)
                actibuff+=blocbuff
                totlprog=totlprog+100/totlpart
                print("Joined "+i+" to parent file "+Style.DIM+"("+str(totlprog)[0:4]+"% completed)"+Style.RESET_ALL)
            actifile=open(filename,"wb")
            actifile.write(actibuff)
            actifile.close()
            os.system("rm "+ldgrname)
            print(Fore.CYAN+"Join process successfully completed!"+Fore.RESET)
        else:
            print(Fore.RED+"Join procedure could not be initiated!"+Fore.RESET+"\n"+\
                "Some parts are missing or corrupted - Download them again")

def spltcunt(filename,partcunt):
    try:
        actifile=open(filename,"rb")
        actibuff=actifile.read()
        buffsize=len(actibuff)
        actifile.close()
        if (partcunt>=10 and partcunt<10000):
            if (partcunt>buffsize):
                print(Fore.RED+"Splitting operation could not be initiated!"+Fore.RESET+"\n"+\
                      "The number of parts is greater than the byte size of your file")
            else:
                poselist=allcbyte(actibuff,partcunt)
                hashlist,sizelist,cuntlist={},{},{}
                totlprog=0
                print(Fore.CYAN+"PROTEXON SPLITTER [by t0xic0der]"+Fore.RESET+"\n"+\
                    "File name   : "+filename+"\n"+\
                    "File size   : "+str(buffsize)+" bytes\n"+\
                    "Part count  : "+str(partcunt)+" parts\n"+\
                    "Ledger name : "+filename+".ldg\n")
                if partcunt>=10 and partcunt<=100:
                    print(Fore.CYAN+"FILE PARTS"+Fore.RESET)
                    for i in range(1,partcunt+1):
                        blocname=filename+"."+nogenten(i)
                        blocbuff=actibuff[poselist[i-1]:poselist[i]]
                        hashlist[blocname]=hashlib.sha512(blocbuff).hexdigest()
                        sizelist[blocname]=len(blocbuff)
                        cuntlist[blocname]=nogenten(i)
                        blocfile=open(blocname,"wb")
                        blocfile.write(blocbuff)
                        blocfile.close()
                        totlprog=totlprog+(100/partcunt)
                        print(str(cuntlist[blocname])+"\t"+str(blocname)+ " created!\t"+Style.DIM+str(sizelist[blocname])+" bytes\t"+Style.RESET_ALL+str(hashlist[blocname])+"\t"+Style.DIM+str(totlprog)[0:4]+"% completed"+Style.RESET_ALL)
                    makeldgr(filename,hashlist,sizelist,cuntlist)
                    print(Fore.CYAN+str(partcunt)+" parts have been created successfully! Ledger was created at "+filename+".ldg"+Fore.RESET)
                elif partcunt>=100 and partcunt<=1000:
                    print(Fore.CYAN+"FILE PARTS"+Fore.RESET)
                    for i in range(1,partcunt+1):
                        blocname=filename+"."+nogenhun(i)
                        blocbuff=actibuff[poselist[i-1]:poselist[i]]
                        hashlist[blocname]=hashlib.sha512(blocbuff).hexdigest()
                        sizelist[blocname]=len(blocbuff)
                        cuntlist[blocname]=nogenhun(i)
                        blocfile=open(blocname,"wb")
                        blocfile.write(blocbuff)
                        blocfile.close()
                        totlprog=totlprog+(100/partcunt)
                        print(str(cuntlist[blocname])+"\t"+str(blocname)+ " created!\t"+Style.DIM+str(sizelist[blocname])+" bytes\t"+Style.RESET_ALL+str(hashlist[blocname])+"\t"+Style.DIM+str(totlprog)[0:4]+"% completed"+Style.RESET_ALL)
                    makeldgr(filename,hashlist,sizelist,cuntlist)
                    print(Fore.CYAN+str(partcunt)+" parts have been created successfully! Ledger was created at "+filename+".ldg"+Fore.RESET)
                elif partcunt>=1000 and partcunt<10000:
                    print(Fore.CYAN+"FILE PARTS"+Fore.RESET)
                    for i in range(1,partcunt+1):
                        blocname=filename+"."+nogenthd(i)
                        blocbuff=actibuff[poselist[i-1]:poselist[i]]
                        hashlist[blocname]=hashlib.sha512(blocbuff).hexdigest()
                        sizelist[blocname]=len(blocbuff)
                        cuntlist[blocname]=nogenthd(i)
                        blocfile=open(blocname,"wb")
                        blocfile.write(blocbuff)
                        blocfile.close()
                        totlprog=totlprog+(100/partcunt)
                        print(str(cuntlist[blocname])+"\t"+str(blocname)+ " created!\t"+Style.DIM+str(sizelist[blocname])+" bytes\t"+Style.RESET_ALL+str(hashlist[blocname])+"\t"+Style.DIM+str(totlprog)[0:4]+"% completed"+Style.RESET_ALL)
                    makeldgr(filename,hashlist,sizelist,cuntlist)
                    print(Fore.CYAN+str(partcunt)+" parts have been created successfully! Ledger was created at "+filename+".ldg"+Fore.RESET)
        else:
            print(Fore.RED+"Splitting operation could not be initiated!"+Fore.RESET+"\n"+\
                  "Splitting the file in this many parts is not at all recommended")
    except FileNotFoundError:
        print(Fore.RED+"Splitting operation could not be initiated!"+Fore.RESET+"\n"+\
              "The requested file is not accessible. Make sure that - \n"+\
              "- You have sufficient privileges to the directory \n"+
              "- The path you have provided is correct \n"+
              "- The file is indeed present in the given path")