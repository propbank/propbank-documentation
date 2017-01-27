import nltk, os, codecs

v1loc = '/home/tim/Data/BOLT/LDC2013E102_BOLT_Phase_1_English_Propbank_DF_Part_6_v2/data/source/'
v2loc = '/home/tim/Data/BOLT/BOLT-ETBpart6v1.1-LDC2013E50-20131114/data/translation-alternates-included/penntree/'
for afile in os.listdir(v1loc):
    print afile
    print "------------------"
    e = codecs.open(v1loc+afile).read().strip().split("\n\n")
    oldfile = [x for x in codecs.open(v2loc+afile.replace(".meta_removed","")) if not x.strip() == '']
    for sid, atree in enumerate(oldfile):
        #print sid, afile
        n1 = nltk.Tree.fromstring(atree)
        norg = nltk.Tree.fromstring(e[sid])
        if not " ".join([x[0] for x in n1.pos() if not x[1] == "-NONE-"]) == " ".join([x[0] for x in norg.pos() if not x[1] == "-NONE-"]):
            print n1.leaves()
            print norg.leaves()

