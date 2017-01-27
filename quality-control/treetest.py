import json, codecs, os, nltk

boltloc = "/home/tim/Data/BOLT/"

j = json.load(open('boltreleases.json'))
bolt = "/home/tim/Propbank/BOLT-Propbank-modified/data/annotations/"

for eachfolder, __, filelist in os.walk(bolt):
    if eachfolder.split("/")[-1].isdigit():
        print eachfolder
        name = 'bolt-'+eachfolder.split("/")[-2].lower()+"-"+str(int(eachfolder.split("/")[-1]))
        if not name == 'bolt-df-6':
            continue

        for propfile in filelist:
            havefile = False
            fileloc = False
            for afile in j[name]:
                q = boltloc +"/"+j[name]
                for folder, __, filelist in os.walk(q):
                    for f in filelist:
                        if f.endswith('.tree'):
                            #print "\t", f
                            if propfile.replace(".prop",".tree") == f:
                                #print "!!!", folder+"/"+f
                                havefile = True
                                fileloc = folder+"/"+f
                           
            
            if not havefile:
                print propfile, "???"
            else:
                sbox = {}
                poslist = {}
                leafbox = {}
                for sentenceid, aline in enumerate([x for x in codecs.open(fileloc) if not x.strip() == '']):
                    #print fileloc
                    #print aline
                    n = nltk.Tree.fromstring(aline)
                    for leafid, leaves in enumerate(n.leaves()):
                        sbox[sentenceid] = sbox.get(sentenceid, []) + [leafid]
                        poslist[sentenceid] = [x[1] for x in n.pos()]
                        leafbox[sentenceid] = n.leaves()
                for apointer in codecs.open(eachfolder+"/"+propfile):
                    sid = int(apointer.split(" ")[1])
                    pred = int(apointer.split(" ")[2])

                    for loc in [x.replace("-LINK","-ARG").replace("-rel","-ARG").split("-ARG")[0].replace(";","*").replace(",","*")  for x in apointer.strip().split(" ")[7:]]:
                        for line in loc.split("*"):
                            l = int(line.split(":")[0])
                            #print l, sid, pred
                            if not poslist[sid][pred] in ["NN", "VBD",'VB',"VBZ",'VBG',"VBZ","VBP","JJ","JJR", "VBN", "NNS","JJS", "NNP"]:
                                print "======================================"
                                print propfile
                                print poslist[sid][pred], " doesn't seem like a proper predicate form"
                                print apointer
                                print leafbox[sid]
                                print "END"
                            if sid in sbox:
                                if pred in sbox[sid]:
                                    pass
                                else:
                                    print "predicate out of range!!!"
                                if l in sbox[sid]:
                                    pass
                                else:
                                    print "argument out of range!!!"
                                    print loc
                            else:
                                print "no sentence with that index!"
                                print apointer
                                