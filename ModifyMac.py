#!/usr/bin/env python
# — coding: utf-8 —
import codecs
import os
from pathlib import Path
import urllib.request

punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

print("Make sure you already install Montreal Forced Aligner. If not follow this links: https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html ")

#Input and Output Part Start
inputpath = ""
outputpath = ""
case = ""
while (inputpath==""):
    inputpath = input("Input Path: ")
    inputpath = inputpath.replace('"','')
    inputpath = Path(inputpath)
    if inputpath.exists():
        if inputpath.suffix == '.lab':
            filetype = "lab file"
            case = 1
        elif inputpath.suffix == '.txt':
            filetype = "txt file"
            case = 2
        elif inputpath.is_dir():
            for entry in inputpath.iterdir():
                if not (entry.suffix == '.lab' or entry.suffix == '.txt'):
                    inputpath=""
                    print("Invalid")
                break
            filetype = "directory"
            case = 3
    else : 
        print("Invalid")
        inputpath=""
while (outputpath==""):
    outputpath = input("Output Path: ")
    outputpath = outputpath.replace('"','')
    outputpath = Path(outputpath)
    if not outputpath.exists():
        outputpath.mkdir()

#Input file Generator 
words = []
uniquewords = []
if case == 1 :
    with codecs.open(inputpath, "r",encoding='utf-8-sig') as labfile:
        contents = labfile.read()
        contents = contents.split(" ")
        for i in range(len(contents)):
            if contents[i] not in punctuation:
                words.append(contents[i])
elif case == 2 :
    with codecs.open(inputpath, "r",encoding='utf-8-sig') as txtfile:
        for contents in txtfile:
            contents = contents.rstrip("\n")
            words.append(contents) 
elif case == 3 :
    for entry in inputpath.iterdir():
        if entry.suffix == '.lab':
            with codecs.open(entry, "r",encoding='utf-8-sig') as labfile:
                contents = labfile.read()
                contents = contents.split(" ")
                for i in range(len(contents)):
                    if contents[i] not in punctuation:
                        words.append(contents[i])
        elif entry.suffix == '.txt':
            with codecs.open(entry, "r",encoding='utf-8-sig') as txtfile:
                for contents in txtfile:
                    contents = contents.rstrip("\n")
                    words.append(contents) 
for word in words:
    if word not in uniquewords:
        uniquewords.append(word)
Uniquepath = str(outputpath)+ r"/UniqueWords.txt"
Uniquepath = Path(Uniquepath)
Unique = codecs.open(Uniquepath, "a","utf-8")
for j in range(len(uniquewords)):
    Unique.write(uniquewords[j]+"\n")
Unique.close()

#Check that you already have thai dict file in computer
dictcheck = ""
thaidictpath = ""
while dictcheck.lower() not in ['y','yes','n','no']:
    dictcheck = input("Already have Thai_Dict.txt in your computer? (Y)es or (n)o : ")   
if dictcheck.lower()=='y' or dictcheck.lower()=='yes':
    maxcount = 5
    while (thaidictpath==""):
        thaidictpath = input("ThaiDict path: ")
        thaidictpath = thaidictpath.replace('"','')
        thaidictpath = Path(thaidictpath)
        if not (thaidictpath.exists() and thaidictpath.suffix == '.txt'): 
            thaidictpath=""
            print("ThaiDict path invalid, %d time(s) remains (It'll download automatically if path failed)"%(maxcount))
            if maxcount == 0 :
                dictcheck = 'n'
                break
            maxcount-=1
if dictcheck.lower()=='n' or dictcheck.lower()=='no':
    thaidictpath = str(outputpath)+r"/Thai_Dict.txt"
    thaidictpath = Path(thaidictpath)
    url = "https://github.com/XoSinepZoX/Trainee/raw/master/Thai_Dict.txt"
    urllib.request.urlretrieve(url,thaidictpath) 

#Save thai dictionary into dict
dict = {}
with open(thaidictpath,"r",encoding='utf-8-sig') as dictfile :
    for dictword in dictfile:
        dictword = dictword.rstrip("\n")
        dword,dphone = dictword.split("\t")
        dict[dword] = dphone
dictfile.close()

#Seperate word into 2 files which are word that can be found in thai dict and can't
Foundpath = str(outputpath)+ r"/WordFound.txt"
Foundpath = Path(Foundpath)
NotFoundPath = str(outputpath)+ r"/WordNotFound.txt"
NotFoundPath = Path(NotFoundPath)
ans = codecs.open(Foundpath, "w","utf-8")
ans.close()
ans = codecs.open(NotFoundPath, "w","utf-8")
ans.close()
checklist=[]
for i in range(len(words)):
    if words[i] not in checklist:
        if words[i] in dict:
            phone = dict[words[i]]
            ans = codecs.open(Foundpath, "a","utf-8")
            ans.write(words[i]+"\t"+phone+"\n")
            ans.close()
            checklist.append(words[i])          
        else:  
            ans = codecs.open(NotFoundPath,"a","utf-8")
            ans.write(words[i]+"\n")
            ans.close()
            checklist.append(words[i])

#Save this word into found dict prepare for mapping
found = {}
with open(Foundpath,"r",encoding='utf-8-sig') as file1 :
    for f in file1:
        f = f.rstrip("\n")
        fword,fphone = f.split("\t")
        found[fword] = fphone
file1.close()

#Check that you already have mapping list or not
mapcheck = ""
mappath = ""
while mapcheck.lower() not in ['y','yes','n','no']:
    mapcheck = input("Already have Mapping.txt in your computer? (Y)es or (n)o : ")   
if mapcheck.lower()=='y' or mapcheck.lower()=='yes':
    maxcount = 5
    while (mappath==""):
        mappath = input("Mapping.txt path: ")
        mappath = mappath.replace('"','')
        mappath = Path(mappath)
        if not (mappath.exists() and mappath.suffix == '.txt'): 
            mappath=""
            print("Mapping.txt path invalid, %d time(s) remains (It'll download automatically if path failed)"%(maxcount))
            if maxcount == 0 :
                mapcheck = 'n'
                break
            maxcount-=1
if mapcheck.lower()=='n' or mapcheck.lower()=='no':
    mappath = str(outputpath)+r"/Mapping.txt"
    mappath = Path(mappath)
    if not mappath.exists():
        url = "https://github.com/XoSinepZoX/Trainee/raw/master/Mapping.txt"
        urllib.request.urlretrieve(url,mappath) 

#Save this into map dict
map = {}
with open(mappath,"r",encoding='utf-8-sig') as mapfile :
    for m in mapfile:
        m = m.rstrip("\n")
        mword,mphone = m.split("\t")
        map[mword] = mphone
mapfile.close()

#Mapping thai phone to global phone and also set z^ 0 1 2 3 4 to null
mapfound = {}
mapnotfound = []
for word in found:
    thaiphone = found[word]
    phone=""
    thaiphone = thaiphone.split()
    for i in range(len(thaiphone)):
        if thaiphone[i] in map:
            if map[thaiphone[i]] != "-":
                phone+=str(map[thaiphone[i]])+" "
        else:
            mapnotfound.append(word)
            break   
    if i == len(thaiphone)-1:
        mapfound[word] = phone

#Save the word that can map to MapFound.txt
mapfoundpath = str(outputpath)+r"/MapFound.txt"
mapfoundpath = Path(mapfoundpath)
mapf= codecs.open(mapfoundpath, "a","utf-8")
for i,j in mapfound.items():
    mapf.write(i+"\t"+j+"\n")    
mapf.close()

#Save the word that can't map to MapNotFound.txt
mapnotfoundpath = str(outputpath)+r"/MapNotFound.txt"
mapnotfoundpath = Path(mapnotfoundpath)
mapnf= codecs.open(mapnotfoundpath, "a","utf-8")
for i in mapnotfound:
    mapnf.write(i+"\n")
mapnf.close()

#Create Answer folder
answerpath = str(outputpath)+r"/Answer"
answerpath = Path(answerpath)
if not answerpath.exists():
    answerpath.mkdir()

#Check that you have thai_g2p model or not
modelcheck = ""
modelpath = ""
while modelcheck.lower() not in ['y','yes','n','no']:
    modelcheck = input("Already have thai_g2p.zip in your computer? (Y)es or (n)o : ")   
if modelcheck.lower()=='y' or modelcheck.lower()=='yes':
    maxcount = 5
    while (modelpath==""):
        modelpath = input("thai_g2p.zip path: ")
        modelpath = modelpath.replace('"','')
        modelpath = Path(modelpath)
        if not (modelpath.exists() and modelpath.suffix == '.zip'): 
            mappath=""
            print("thai_g2p.zip path invalid, %d time(s) remains (It'll download automatically if path failed)"%(maxcount))
            if maxcount == 0 :
                mapcheck = 'n'
                break
            maxcount-=1
if modelcheck.lower()=='n' or modelcheck.lower()=='no':
    modelpath = str(outputpath)+r"/thai_g2p.zip"
    modelpath = Path(modelpath)
    if not modelpath.exists():
        url = "http://mlmlab.org/mfa/mfa-models/g2p/thai_g2p.zip"
        urllib.request.urlretrieve(url,modelpath) 

#path to mfa folder
mfapath=""
while (mfapath==""):
        mfapath = input("montreal-forced-aligner path: ")
        mfapath = mfapath.replace('"','')
        mfapath = Path(mfapath)
        if not mfapath.exists():
            mfapath=""

#Generate dict for word that can't be found in thai dict by using g2p model
os.chdir(mfapath)
os.system(r'bin/mfa_generate_dictionary '+str(modelpath)+" "+str(NotFoundPath)+" "+ str(outputpath)+r"/G2pdict.txt")

#Additional Comment if do not want to g2p non mapped file
os.system(r'bin/mfa_generate_dictionary '+str(modelpath)+" "+str(mapnotfoundpath)+" "+ str(outputpath)+r"/MNFG2pdict.txt")
mnfg2p = {}
mnfg2ppath = str(outputpath)+r"/MNFG2pdict.txt"
mnfg2ppath = Path(mnfg2ppath)
with open(mnfg2ppath,"r",encoding='utf-8-sig') as mnfg2pfile :
    for mnfg in mnfg2pfile:
        mnfg = mnfg.rstrip("\n")
        mnfgword,mnfgphone = mnfg.split("\t")
        mnfg2p[mnfgword] = mnfgphone
mnfg2pfile.close()    

#Save into g2p dict
g2p = {}
g2ppath = str(outputpath)+r"/G2pdict.txt"
g2ppath = Path(g2ppath)
with open(g2ppath,"r",encoding='utf-8-sig') as g2pfile :
    for g in g2pfile:
        g = g.rstrip("\n")
        gword,gphone = g.split("\t")
        g2p[gword] = gphone
g2pfile.close()

#Generate Output1 (Word that can be found in thai dict and can also mapping to global phone)
Answer1 = []
for i in mapfound:
    Answer1.append([i,'tp','gp'])
for ansdict in Answer1:
    if ansdict[0] in mapfound:
        ansdict[1] = dict.get(ansdict[0])
        ansdict[2] = mapfound.get(ansdict[0])
        #print(ansdict)
ans1path = str(outputpath)+r"/Answer/Output1.txt"
ans1path = Path(ans1path)
dictanswer1 = codecs.open(ans1path, "w","utf-8")
dictanswer1.write("")
dictanswer1 = codecs.open(ans1path, "a","utf-8")
for i in Answer1:
    dictanswer1.write(i[0]+"\t"+i[1]+"\t"+i[2]+"\n")    
dictanswer1.close()

#Generate Output2 (Word that can be found in thai dict but can't be map)
Answer2 = []
for i in mapnotfound:
    Answer2.append([i,"tp"])
for ansdict2 in Answer2:
    if ansdict2[0] in dict:
        ansdict2[1] = dict.get(ansdict2[0])
ans2path = str(outputpath)+r"/Answer/Output2.txt"
ans2path = Path(ans2path)
dictanswer2 = codecs.open(ans2path, "w","utf-8")
dictanswer2.write("")
dictanswer2 = codecs.open(ans2path, "a","utf-8")
for i in Answer2:
    dictanswer2.write(i[0]+"\t"+i[1]+"\n")    
dictanswer2.close()

#Generate Output 3 (Word can't be found in thai dict)
Answer3 = []
for i in g2p:
    Answer3.append([i,"gp"])
for ansdict3 in Answer3:
    if ansdict3[0] in g2p:
        ansdict3[1] = g2p.get(ansdict3[0])

ans3path = str(outputpath)+r"/Answer/Output3.txt"
ans3path = Path(ans3path)
dictanswer3 = codecs.open(ans3path, "w","utf-8")
dictanswer3.write("")
dictanswer3 = codecs.open(ans3path, "a","utf-8")
for i in Answer3:
    dictanswer3.write(i[0]+"\t"+i[1]+"\n")    
dictanswer3.close()

#Generate Outputdict (global phone for every word in input text file )
Answer = {}
with open(Uniquepath, "r",encoding='utf-8-sig') as ansfile: 
    for ansf in ansfile:
        ansf = ansf.rstrip("\n")
        Answer[ansf] = " "
for ansdict in Answer:
    if ansdict in mapfound:
        Answer[ansdict] = mapfound[ansdict] 
    elif ansdict in g2p :
        Answer[ansdict] = g2p[ansdict]
    elif ansdict in mnfg2p :
        Answer[ansdict] = mnfg2p[ansdict]
    else : 
        Answer[ansdict] = " "
anspath = str(outputpath)+r"/Answer/OutputDict.txt"
anspath = Path(anspath)
dictanswer = codecs.open(anspath, "w","utf-8")
dictanswer.write("")
dictanswer = codecs.open(anspath, "a","utf-8")
for i,j in Answer.items():
    dictanswer.write(i+"\t"+j+"\n")    
dictanswer.close()