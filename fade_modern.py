import hashlib, sqlite3, os, time
from colorama import init, Fore, Style

init()

class splmodel:
    def __init__(self, filename):
        try:
            actifile = open(filename, "rb")
            self.actibuff = actifile.read()
            actifile.close()
            self.filename = filename
            self.buffsize = len(self.actibuff)
        except FileNotFoundError:
            print(Fore.RED + "[ERROR OCCURRED]" + Fore.RESET + "\n" + \
                  "Splitting operation could not be initiated!\n" + \
                  "The requested file is not accessible. Make sure that - \n" + \
                  "- You have sufficient privileges to the directory \n" +
                  "- The path you have provided is correct \n" +
                  "- The file is indeed present in the given path")

    def nogenten(self, numvalue):
        strvalue = ""
        if numvalue < 10:
            strvalue = "0" + str(numvalue)
        else:
            strvalue = str(numvalue)
        return strvalue

    def nogenhun(self, numvalue):
        strvalue = ""
        if numvalue < 10:
            strvalue = "00" + str(numvalue)
        elif numvalue >= 10 and numvalue < 100:
            strvalue = "0" + str(numvalue)
        else:
            strvalue = str(numvalue)
        return strvalue

    def nogenthd(self,numvalue):
        strvalue = ""
        if numvalue < 10:
            strvalue = "000" + str(numvalue)
        elif numvalue >= 10 and numvalue < 100:
            strvalue = "00" + str(numvalue)
        elif numvalue >= 100 and numvalue < 1000:
            strvalue = "0" + str(numvalue)
        else:
            strvalue = str(numvalue)
        return strvalue

    def allcsize(self,partsize):
        sizelist, poselist = [], []
        partcunt = self.buffsize // partsize
        poselist.append(0)
        if self.buffsize % partsize == 0:
            genptsiz = self.buffsize // partcunt
            for i in range(0, partcunt):
                sizelist.append(genptsiz)
        else:
            genptsiz = self.buffsize // partcunt
            endptsiz = self.buffsize % partcunt
            for i in range(0, partcunt):
                sizelist.append(genptsiz)
            sizelist.append(endptsiz)
            partcunt+=1
        for i in range(1, partcunt+1):
            poselist.append(sum(sizelist[0:i]))
        return partcunt, poselist

    def allcbyte(self,partcunt):
        sizelist, poselist = [], []
        if self.buffsize % partcunt == 0:
            genptsiz = self.buffsize // partcunt
            for i in range(0, partcunt):
                sizelist.append(genptsiz)
        else:
            genptsiz = self.buffsize // partcunt
            endptsiz = self.buffsize % partcunt
            sizelist.append(genptsiz + endptsiz)
            for i in range(0, partcunt - 1):
                sizelist.append(genptsiz)
        poselist.append(0)
        for i in range(1, partcunt + 1):
            poselist.append(sum(sizelist[0:i]))
        return poselist

    def makeldgr(self, hashlist, sizelist, cuntlist, typesplt):
        ldgrname = self.filename + typesplt
        actifile = open(ldgrname, "wb")
        actifile.close()
        ldgrbase = sqlite3.connect(ldgrname)
        maketabl = "create table ldgrbase ("+\
                   "partnumb text primary key not null, "+\
                   "partname text not null, "+\
                   "partsize int not null, "+\
                   "sha512dg text not null);"
        ldgrbase.execute(maketabl)
        for i in hashlist.keys():
            querystr = "insert into ldgrbase (partnumb, partname, partsize, sha512dg) values ('" + \
                       str(cuntlist[i]) + "', '" + str(i) + "', " + str(sizelist[i]) + ", '" + str(hashlist[i]) + "')"
            ldgrbase.execute(querystr)
        ldgrbase.commit()
        ldgrbase.close()

    def spltsize(self,partsize):
        if partsize >= 1 and partsize < 8:
            partsize = partsize * 1048576
            if partsize > self.buffsize:
                print(Fore.RED + "[ERROR OCCURRED]" + Fore.RESET + "\n" + \
                      "Splitting operation could not be initiated!\n" + \
                      "The size per block is greater than the byte size of your file")
                return False
            else:
                partcunt = self.allcsize(partsize)[0]
                poselist = self.allcsize(partsize)[1]
                hashlist, sizelist, cuntlist, cuntdisp = {}, {}, {}, {}
                totlprog = 0
                print(Fore.CYAN + "[PROTEXON SPLITTER by t0xic0der]" + Fore.RESET + "\n" + \
                      "File name   : " + self.filename + "\n" + \
                      "File size   : " + str(self.buffsize) + " bytes\n" + \
                      "Block size  : " + str(partsize) + " bytes\n" + \
                      "Ledger name : " + self.filename + ".sbs\n")
                print(Fore.CYAN + "[STARTING SPLIT OPERATION]" + Fore.RESET)
                startsec = time.time()
                for i in range(1, partcunt + 1):
                    if partcunt >= 10 and partcunt <= 100:
                        blocname = self.filename + "." + self.nogenten(i)
                        cuntlist[blocname] = i
                        cuntdisp[blocname] = self.nogenten(i)
                    elif partcunt >= 100 and partcunt <= 1000:
                        blocname = self.filename + "." + self.nogenhun(i)
                        cuntlist[blocname] = i
                        cuntdisp[blocname] = self.nogenhun(i)
                    elif partcunt >= 1000 and partcunt < 10000:
                        blocname = self.filename + "." + self.nogenthd(i)
                        cuntlist[blocname] = i
                        cuntdisp[blocname] = self.nogenthd(i)
                    blocbuff = self.actibuff[poselist[i - 1]:poselist[i]]
                    hashlist[blocname] = hashlib.sha512(blocbuff).hexdigest()
                    sizelist[blocname] = len(blocbuff)
                    blocfile = open(blocname, "wb")
                    blocfile.write(blocbuff)
                    blocfile.close()
                    del(blocbuff)
                    totlprog = totlprog + (100 / partcunt)
                    print(str(cuntdisp[blocname]) + "\t"+  str(hashlist[blocname]) + "\t" + Style.DIM + \
                          str(totlprog)[0:4] + "% completed" + Style.RESET_ALL + "\t" + Style.DIM + \
                          str(sizelist[blocname]) + " bytes\t" + Style.RESET_ALL)
                self.makeldgr(hashlist, sizelist, cuntlist, ".sbs")
                endinsec = time.time()
                totatime = str(endinsec - startsec).split(".")[0] + "." + str(endinsec - startsec).split(".")[1][0:2]
                del(self.actibuff)
                print("\n" + Fore.CYAN + "[SPLIT OPERATION COMPLETED]" + Fore.RESET + "\n" + \
                      "Parts created  : " + str(partcunt) + " parts \n" + \
                      "Block size     : " + str(partsize) + " bytes \n" + \
                      "Ledger created : " + str(self.filename) + ".sbs \n" + \
                      "Time taken     : " + str(totatime) + " seconds \n")
                return True
        else:
            print(Fore.RED + "[ERROR OCCURRED]" + Fore.RESET + "\n" + \
                  "Splitting operation could not be initiated!\n" + \
                  "We do not recommend splitting into blocks of this size")
            return False

    def spltcunt(self,partcunt):
        if partcunt >= 10 and partcunt < 10000:
            if partcunt > self.buffsize:
                print(Fore.RED + "[ERROR OCCURRED]" + Fore.RESET + "\n" + \
                      "Splitting operation could not be initiated!\n" + \
                      "The number of parts is greater than the byte size of your file")
                return False
            else:
                poselist = self.allcbyte(partcunt)
                hashlist, sizelist, cuntlist, cuntdisp = {}, {}, {}, {}
                totlprog = 0
                print(Fore.CYAN + "[PROTEXON SPLITTER by t0xic0der]" + Fore.RESET + "\n" + \
                      "File name   : " + self.filename + "\n" + \
                      "File size   : " + str(self.buffsize) + " bytes\n" + \
                      "Part count  : " + str(partcunt) + " parts\n" + \
                      "Ledger name : " + self.filename + ".sbc\n")
                print(Fore.CYAN + "[STARTING SPLIT OPERATION]" + Fore.RESET)
                startsec = time.time()
                for i in range(1, partcunt + 1):
                    if partcunt >= 10 and partcunt <= 100:
                        blocname = self.filename + "." + self.nogenten(i)
                        cuntlist[blocname] = i
                        cuntdisp[blocname] = self.nogenten(i)
                    elif partcunt >= 100 and partcunt <= 1000:
                        blocname = self.filename + "." + self.nogenhun(i)
                        cuntlist[blocname] = i
                        cuntdisp[blocname] = self.nogenhun(i)
                    elif partcunt >= 1000 and partcunt < 10000:
                        blocname = self.filename + "." + self.nogenthd(i)
                        cuntlist[blocname] = i
                        cuntdisp[blocname] = self.nogenthd(i)
                    blocbuff = self.actibuff[poselist[i - 1]:poselist[i]]
                    hashlist[blocname] = hashlib.sha512(blocbuff).hexdigest()
                    sizelist[blocname] = len(blocbuff)
                    blocfile = open(blocname, "wb")
                    blocfile.write(blocbuff)
                    blocfile.close()
                    del(blocbuff)
                    totlprog = totlprog + (100 / partcunt)
                    print(str(cuntdisp[blocname]) + "\t" + str(hashlist[blocname]) + "\t" + Style.DIM + \
                          str(totlprog)[0:4] + "% completed" + Style.RESET_ALL + "\t" + Style.DIM + \
                          str(sizelist[blocname]) + " bytes\t" + Style.RESET_ALL)
                self.makeldgr(hashlist, sizelist, cuntlist, ".sbc")
                endinsec = time.time()
                totatime = str(endinsec - startsec).split(".")[0] + "." + str(endinsec - startsec).split(".")[1][0:2]
                del(self.actibuff)
                print("\n" + Fore.CYAN + "[SPLIT OPERATION COMPLETED]" + Fore.RESET + "\n" + \
                      "Parts created  : " + str(partcunt) + " parts \n" + \
                      "Ledger created : " + str(self.filename) + ".sbc \n" + \
                      "Time taken     : " + str(totatime) + " seconds \n")
                return True
        else:
            print(Fore.RED + "[ERROR OCCURRED]" + Fore.RESET + "\n" + \
                  "Splitting operation could not be initiated!\n" + \
                  "We do not recommend splitting in this many parts")
            return True

def fetcblck(self, blckordr, ledgname):
    database = sqlite3.connect(ledgname)
    acticurs = database.cursor()
    qurytext = "select * from ldgrbase where partnumb = '" + str(blckordr) + "'"
    rsltobjc = acticurs.execute(qurytext)
    rsltobjc = rsltobjc.fetchall()
    retndict = {
        "blckordr": rsltobjc[0],
        "blckname": rsltobjc[1],
        "bytesize": rsltobjc[2],
        "sha512dg": rsltobjc[3],
    }
    return retndict

class wrngldgr(Exception):
    def __init__(self,ldgrextn):
        self.ldgrextn=ldgrextn

class jinmodel:
    def __init__(self,ldgrname):
        namepart=ldgrname.split(".")
        self.ldgrname=ldgrname
        self.typesplt=namepart[-1]
        filename = namepart[0]
        for i in range(1,len(namepart) - 1):
            filename = filename + "." + namepart[i]
        self.filename = filename
        try:
            if self.typesplt=="sbc" or self.typesplt=="sbs":
                self.hashlist = {}
                self.sizelist = {}
                self.cuntlist = {}
                try:
                    ldgrbase = sqlite3.connect(ldgrname)
                    dbcursor = ldgrbase.execute("select * from ldgrbase")
                    for row in dbcursor:
                        self.cuntlist[row[1]] = row[0]
                        self.sizelist[row[1]] = row[2]
                        self.hashlist[row[1]] = row[3]
                    ldgrbase.close()
                except sqlite3.OperationalError:
                    print(Fore.RED + "[ERROR OCCURRED]" + Fore.RESET + "\n" + \
                          "The ledger could not be read properly!\n" + \
                          "Make sure you have \n" + \
                          "- Privileges to access the ledger file \n" + \
                          "- The ledger file present in the directory \n" + \
                          "- Been pointing towards to right location \n" + \
                          "- A valid ledger file stored there")
            else:
                raise wrngldgr(self.typesplt)
        except wrngldgr:
            print(Fore.RED + "[ERROR OCCURRED]" + Fore.RESET + "\n" + \
                  "The ledger provided is in wrong format!")

    def displdgr(self):
        if self.typesplt=="sbc" or self.typesplt=="sbs":
            print(Fore.CYAN + "[LEDGER CONTENTS]" + Fore.RESET)
            for i in self.cuntlist.keys():
                print("Part count  : " + str(self.cuntlist[i]) + "\n" + \
                      "Part name   : " + str(i) + "\n" + \
                      "Part size   : " + str(self.sizelist[i]) + "\n" + \
                      "SHA512 hash : " + str(self.hashlist[i]))
        else:
            print(Fore.RED + "[ERROR OCCURRED]" + Fore.RESET + "\n" + \
                  "Ledger contents could not be displayed!\n" + \
                  "The ledger format is not supported!")

    def pthealth(self):
        joinable = False
        if self.typesplt=="sbc" or self.typesplt=="sbs":
            failcunt, passcunt = 0, 0
            chekcunt, misscunt = 0, 0
            startsec = time.time()
            for i in self.cuntlist.keys():
                chekcunt += 1
                try:
                    actifile = open(i, "rb")
                    actibuff = actifile.read()
                    actifile.close()
                    preshash = hashlib.sha512(actibuff).hexdigest()
                    if preshash == self.hashlist[i]:
                        passcunt += 1
                    else:
                        failcunt += 1
                except FileNotFoundError:
                    misscunt += 1
            endinsec = time.time()
            totatime = str(endinsec - startsec).split(".")[0] + "." + str(endinsec - startsec).split(".")[1][0:2]
            if chekcunt == passcunt:
                joinable = True
            print(Fore.CYAN + "[BLOCK INTEGRITY CHECK]" + "\n" + Fore.RESET + \
                  "Total checks          : " + str(chekcunt) + "\n" + \
                  "Files with wrong hash : " + str(failcunt) + "\n" + \
                  "Files with match hash : " + str(passcunt) + "\n" + \
                  "Files missing         : " + str(misscunt) + "\n" + \
                  "Time taken for check  : " + str(totatime) + " seconds\n" + \
                  "Integrity result      : " + str(joinable) + "\n")
        else:
            print(Fore.RED + "[ERROR OCCURRED]" + Fore.RESET + "\n" + \
                  "Block integrity check could not be performed!\n" + \
                  "The ledger format is not supported!")
        return joinable

    def joincunt(self):
        if self.typesplt=="sbc" or self.typesplt=="sbs":
            totlpart = int(list(self.cuntlist.values())[-1])
            totlprog = 0
            if (self.pthealth()):
                print(Fore.CYAN + "[STARTING JOIN OPERATION]" + Fore.RESET)
                startsec = time.time()
                actibuff = b""
                for i in self.cuntlist.keys():
                    blocfile = open(i, "rb")
                    blocbuff = blocfile.read()
                    blocfile.close()
                    os.system("rm " + i)
                    actibuff += blocbuff
                    totlprog = totlprog + 100 / totlpart
                    print("Joined " + i + " to parent file " + Style.DIM + "(" + \
                          str(totlprog)[0:4] + "% completed)" + Style.RESET_ALL)
                actifile = open(self.filename, "wb")
                actifile.write(actibuff)
                actifile.close()
                os.system("rm " + self.ldgrname)
                endinsec = time.time()
                totatime = str(endinsec - startsec).split(".")[0] + "." + str(endinsec - startsec).split(".")[1][0:2]
                print("\n" + Fore.CYAN + "[JOIN OPERATION COMPLETED]" + Fore.RESET + "\n" + \
                      "Time taken : " + totatime + " seconds" + Fore.RESET)
            else:
                print(Fore.RED + "[ERROR OCCURRED]" + Fore.RESET + "\n" + \
                      "Join procedure could not be initiated!\n" + \
                      "Some parts are missing or corrupted - Download them again")
        else:
            print(Fore.RED + "[ERROR OCCURRED]" + Fore.RESET + "\n" + \
                  "Join procedure could not be initiated!\n" + \
                  "The ledger format is not supported")

    def joinsize(self):
        pass