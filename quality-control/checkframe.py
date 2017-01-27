from bs4 import BeautifulSoup
import os
import sys

import lxml
import sys
from lxml import etree
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("floc", help="Where the frames are located")
parser.add_argument("dtd", help="Where the dtd for those frames is located")
args = parser.parse_args()

CHECKCONTIGUITYOFROLESETS = False
CHECKFORMISSINGARGMS = False
CHECKFORMISSINGEXAMPLERELS =  False
floc = args.floc
dtd = args.dtd
dtd2 = etree.DTD(open(dtd))
aliasbox = {}

for afile in sorted(os.listdir(floc)):
    if '.dtd' in afile or '.gitignore' in afile:
        continue
    if not '<!DOCTYPE frameset SYSTEM "frameset.dtd">' in open(floc+afile).read():
        print "!!!!!!!!"+afile+" doesn't have the dtd declaration"
    b = BeautifulSoup(open(floc+afile))
    rsbox = []
    for apredicate in b.find_all("predicate"):
        
        for aroleset in apredicate.find_all("roleset"):
            rsbox.append(aroleset['id'].split(".")[1])

            if not apredicate['lemma'] == aroleset['id'].split(".")[0]:
                print("predicate mismatch: ",  apredicate['lemma'], aroleset['id'])
            r = []

            for arole in aroleset.find_all("role"):
                if arole['n'].isdigit():
                    r.append(int(arole['n']))
                if len(arole['descr']) ==0:

                    print "empty role:", aroleset['id']
                    print arole
            #print(aroleset['name'])
            if len(aroleset['name']) ==0:
                print "empty name:", aroleset['id']
            if len(r) > len(set(r)):
                print "redundant arguments!!!!!", aroleset['id'], r
            if CHECKCONTIGUITYOFROLESETS:
                if len(r) > 0:

                    #print(r)
                    #print range(min(r),max(r)+1)
                    if not len(r) == len(range(min(r),max(r)+1)):
                        print "noncontiguous numbered args:", aroleset['id'], r
            for example in aroleset.find_all("example"):
                y = []
                for rel in example.find_all("rel"):
                    y.append(rel.text)
                if len(y) ==0:
                    if CHECKFORMISSINGEXAMPLERELS:
                        print ("missing rel in example in ",aroleset['id'])

                for arg in example.find_all('arg'):
                    if arg['n'].isdigit() and not int(arg['n']) in r:
                        print "example arg ", arg['n'], " not in set"
                        print aroleset['id'], r
                    elif not arg['n'].isdigit():
                        if not arg['f'].lower() in ['mnr', 'dir', 'tmp','loc','adv', 'prp', 'neg','mod','lvb', 'slc','cau','adj','dis','ext','gol','prd','cxn', 'pnc','rcl', 'com','dsp', 'prr','rec']:
                            if len(arg['f'].lower()) == 0:
                                if CHECKFORMISSINGARGMS:
                                    print "no argf ", aroleset['id'], arg
                                pass
                            else:
                                #pass
                                print "suspicious example argf ", aroleset['id'], arg
            arolesetlemma= aroleset['id'].split(".")[0]
            haslem = False
            for alias in aroleset.find_all("alias"):
                aliasbox[alias.text] = aliasbox.get(alias.text, set())
                aliasbox[alias.text].add(afile)
                if len(aliasbox[alias.text]) > 1:
                    print "overlapping aliases!!!!", aliasbox[alias.text]
                if alias.text == arolesetlemma:
                    haslem = True
            if not haslem:
                print "no alias corresponding to name: ", aroleset['id']
    if len(rsbox) > len(set(rsbox)):
        print("multiple rolesets with id", afile)


    try:
        #print afile    
        its_file = open(floc+"/"+afile).read()
        xm = etree.XML(its_file)

        tval = dtd2.validate(xm)
        if not tval:
            #pass

            print "DTD", afile
            #ed.write("DTD issue:"+afile+"\n")
    except:

        print afile
        #ed.write(afile+"\n")