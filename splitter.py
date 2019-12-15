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

def allcsize(filename,partcunt):
    actifile=open(filename,"rb")
    actibuff=actifile.read()
    actifile.close()
    filesize=len(actibuff)
    sizelist,poselist=[],[]
    if filesize%partcunt==0:
        genptsiz=filesize//partcunt
        for i in range(0,partcunt):
            sizelist.append(genptsiz)
    else:
        genptsiz=filesize//partcunt
        endptsiz=filesize%partcunt
        sizelist.append(genptsiz+endptsiz)
        for i in range(0,partcunt-1):
            sizelist.append(genptsiz)
    poselist.append(0)
    for i in range(1,partcunt+1):
        poselist.append(sum(sizelist[0:i]))
    return poselist

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

def displdgr(ldgrname):
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
    print(Fore.GREEN+"File health check has been performed"+"\n"+
          Style.RESET_ALL+\
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
        print(Fore.RED+"The ledger could not be read properly!"+Style.RESET_ALL+"\n"+\
              "Make sure you have \n"+\
              "- Privileges to access the ledger file \n"+\
              "- the ledger file present in the directory \n"+\
              "- been pointing towards to right location")
    else:
        cuntlist=ldgrlist[0]
        sizelist=ldgrlist[1]
        hashlist=ldgrlist[2]
        if (pthealth(cuntlist,sizelist,hashlist)):
            print(Fore.GREEN+"Initiating join procedure..."+Style.RESET_ALL)
            actibuff=b""
            for i in cuntlist.keys():
                blocfile=open(i,"rb")
                blocbuff=blocfile.read()
                blocfile.close()
                os.system("rm "+i)
                actibuff+=blocbuff
                print("Joined "+i+" to parent file (100%)")
            actifile=open(filename,"wb")
            actifile.write(actibuff)
            actifile.close()
            os.system("rm "+ldgrname)
            print(Fore.GREEN+"Join process successfully completed!"+Style.RESET_ALL)
        else:
            print(Fore.RED+"Join procedure could not be initiated!"+Style.RESET_ALL+"\n"+\
                "Some parts are missing or corrupted - Download them again")

def spltcunt(filename,partcunt):
    try:
        actifile=open(filename,"rb")
        actibuff=actifile.read()
        actifile.close()
        poselist=allcbyte(actibuff,partcunt)
        buffsize=len(actibuff)
        hashlist,sizelist,cuntlist={},{},{}
        print(Fore.GREEN+"PROTEXON SPLITTER [by t0xic0der]"+Style.RESET_ALL+"\n"+\
            "File name   : "+filename+"\n"+\
            "File size   : "+str(buffsize)+" bytes\n"+\
            "Part count  : "+str(partcunt)+" parts\n"+\
            "Ledger name : "+filename+".ldg\n")
        if partcunt>=10 and partcunt<100:
            print(Fore.GREEN+"FILE PARTS"+Style.RESET_ALL)
            for i in range(1,partcunt+1):
                blocname=filename+"."+nogenten(i)
                blocbuff=actibuff[poselist[i-1]:poselist[i]]
                hashlist[blocname]=hashlib.sha512(blocbuff).hexdigest()
                sizelist[blocname]=len(blocbuff)
                cuntlist[blocname]=nogenten(i)
                blocfile=open(blocname,"wb")
                blocfile.write(blocbuff)
                blocfile.close()
                print(str(cuntlist[blocname])+"\t"+str(blocname)+ " created!\t"+str(sizelist[blocname])+" bytes\t"+str(hashlist[blocname]))
            makeldgr(filename,hashlist,sizelist,cuntlist)
            print(Fore.GREEN+str(partcunt)+" parts have been created successfully! Ledger was created at "+filename+".ldg"+Style.RESET_ALL)
        elif partcunt>100 and partcunt<1000:
            print(Fore.GREEN+"FILE PARTS"+Style.RESET_ALL)
            for i in range(1,partcunt+1):
                blocname=filename+"."+nogenhun(i)
                blocbuff=actibuff[poselist[i-1]:poselist[i]]
                hashlist[blocname]=hashlib.sha512(blocbuff).hexdigest()
                sizelist[blocname]=len(blocbuff)
                cuntlist[blocname]=nogenhun(i)
                blocfile=open(blocname,"wb")
                blocfile.write(blocbuff)
                blocfile.close()
                print(str(cuntlist[blocname])+"\t"+str(blocname)+ " created!\t"+str(sizelist[blocname])+" bytes\t"+str(hashlist[blocname]))
            makeldgr(filename,hashlist,sizelist,cuntlist)
            print(Fore.GREEN+str(partcunt)+" parts have been created successfully! Ledger was created at "+filename+".ldg"+Style.RESET_ALL)
        elif partcunt>=1000 or partcunt<10:
            print(Fore.RED+"Parts count greater than or equal to 1000 or lesser than or equal to 10 is not recommended!"+Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED+"Splitting operation could not be initiated!"+Style.RESET_ALL+"\n"+\
              "The requested file is not accessible. Make sure that - \n"+\
              "- You have sufficient privileges to the directory \n"+
              "- The path you have provided is correct \n"+
              "- The file is indeed present in the given path")