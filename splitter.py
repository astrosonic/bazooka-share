import hashlib

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

def spltcunt(filename,partcunt):
    actifile=open(filename,"rb")
    actibuff=actifile.read()
    actifile.close()
    poselist=allcbyte(actibuff,partcunt)
    buffsize=len(actibuff)
    hashlist,sizelist,cuntlist={},{},{}
    if partcunt>10 and partcunt<100:
        for i in range(1,partcunt+1):
            blocname=filename+"."+nogenten(i)
            blocbuff=actibuff[poselist[i-1]:poselist[i]]
            hashlist[blocname]=hashlib.sha512(blocbuff).hexdigest()
            sizelist[blocname]=len(blocbuff)
            cuntlist[blocname]=nogenten(i)
            blocfile=open(blocname,"wb")
            blocfile.write(blocbuff)
            blocfile.close()
    elif partcunt>100 and partcunt<1000:
        for i in range(1,partcunt+1):
            blocname=filename+"."+nogenhun(i)
            blocbuff=actibuff[poselist[i-1]:poselist[i]]
            hashlist[blocname]=hashlib.sha512(blocbuff).hexdigest()
            sizelist[blocname]=len(blocbuff)
            cuntlist[blocname]=nogenhun(i)
            blocfile=open(blocname,"wb")
            blocfile.write(blocbuff)
            blocfile.close()
    elif partcunt>1000:
        print("Parts count greater than 1000 is not recommended!")
    print("LZMA SPLITTER [by t0xic0der]\n"+\
          "File name  : "+filename+"\n"+\
          "File size  : "+str(buffsize)+" bytes\n"+\
          "Part count : "+str(partcunt)+" parts")
    for i in hashlist.keys():
        print(str(cuntlist[i])+"\t"+str(i)+"\t\t"+str(sizelist[i])+" bytes\t"+str(hashlist[i]))
