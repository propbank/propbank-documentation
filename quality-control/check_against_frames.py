from bs4 import BeautifulSoup
import os
import sys
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(' pointer qc ')


parser = argparse.ArgumentParser()
parser.add_argument("framefiles", help="propbank frame file set")
parser.add_argument("--pointers", help="propbank pointers")
parser.add_argument("--projectdir", help="corrected data location")
parser.add_argument("--allprojects", help="propbank-data location")
args = parser.parse_args()

def check_basic_formatting(targetfile):
	logger.info("checking basic formatting for :"+ targetfile)
	prrbox = {}
	lvbbox = {}
	allpoints = {}
	allpreds = {}
	tfile = open(targetfile,'r')
	tbox = [x.strip() for x in tfile]
	tfile.close()
	for index, eachline in enumerate(tbox):
		if "  " in eachline:
			logger.warning("double spaces at line :"+ str(index)+ eachline)
		if " \n" in eachline:
			logger.warning("space before the newline at line :"+ str(index)+ eachline)
		ww= [int(x.split("ARG")[1]) for x in eachline.strip().split(" ")[7:] if "ARG" in x and x.split("ARG")[1].isdigit()]
		allargs = ["ARG"+x.split("ARG")[1] for x in eachline.strip().split(" ")[7:] if "ARG" in x]
		weirdargs = [x for x in allargs if not x in ["ARG0","ARG1", "ARG2","ARG3","ARG4","ARG5", "ARGM-LOC","ARGM-PRP", "ARGM-TMP", "ARGM-DSP", "ARGA", "ARGM-REC", "ARGM-MNR", "ARGM-ADV","ARGM-NEG","ARGM-EXT","ARGM-LVB","ARGM-PRR","ARGM-DIR","ARGM-ADJ","ARGM-GOL","ARGM-CXN","ARGM-CAU","ARGM-MOD","ARGM-PRD","ARGM-COM","ARGM-DIS"]]
		if len(weirdargs) > 0:
			logger.warning("weird argument :"+ str(" ".join(weirdargs))+"\n\t\t"+ eachline)
		if len([x for x in eachline.strip().split(" ")[7:] if "-rel" in x]) > 1:
			logger.warning("multiple rels :"+ aline)
		zz= [yy for yy in set(ww) if ww.count(yy) >1]
		if len(zz) > 0:
			logger.warning("multiple identical numbered arguments at :"+ str(index)+eachline)
			
			
			
		if "\n\n" in eachline:
			logger.warning("extra line at the end of the file at :"+ str(index)+eachline)
		if "\n\n" in eachline:
			logger.warning("extra line at the end of the file at :"+ str(index)+eachline)
		try:
			int(eachline.split(" ")[1])
		except:
			logger.warning("sentence number is not an integer"+ str(index)+eachline)
		try:
			int(eachline.split(" ")[2])
		except:
			logger.warning("token index is not an integer"+ str(index)+eachline)
		if not eachline.split(" ")[6] == "-----":
			logger.warning("spacer isn't ----- for line "+ str(index)+eachline)
		y = [x for x in eachline.split(" ")[7:] if '-rel' in x]
		if len(y) > 1:
			logger.warning("multiple rels on line "+ str(index)+eachline)
			#express(eachline)	
			
		elif len(y) ==0:
			logger.warning("no rel on line "+ str(index)+eachline)
		else:
			if "," in y[0]:
				www= [int(z.split(":")[0]) for z in y[0].split(",")]
			else:
				www= [int(y[0].split(":")[0])]
			if not int(eachline.split(" ")[2]) in www:
				logger.warning("wrong rel in "+ str(index)+eachline)
				#print eachline+"\n\n"
				#express(eachline)	
			

		if len([x for x in eachline.split(" ")[7:] if '-ARGM-PRR' in x]) == 1 and not '.LV' in  eachline.split(" ")[5]:
			logger.warning("PRR without an .LV sense on line "+ str(index)+eachline)
			t= eachline.split(" ")[:5]
			rsb = eachline.split(" ")[5].split(".")[0]+".LV"
		allpoints[" ".join(eachline.split(" ")[:2])] = allpoints.get(" ".join(eachline.split(" ")[:2]), []) + [eachline]
		allpreds[" ".join(eachline.strip().split(" ")[:3])] = allpreds.get(" ".join(eachline.strip().split(" ")[:3]), []) + [eachline.strip()]
		
		for arg in eachline.split(" ")[7:]:
			if "-ARGM-PRR" in arg:
				prrbox[" ".join(eachline.split(" ")[:2])]= prrbox.get(" ".join(eachline.split(" ")[:2]), {})
				prrbox[" ".join(eachline.split(" ")[:2])][arg.split("-")[0]]= prrbox[" ".join(eachline.split(" ")[:2])].get(arg.split("-")[0], eachline)
			if "-ARGM-LVB" in arg:
				lvbbox[" ".join(eachline.split(" ")[:2])]= lvbbox.get(" ".join(eachline.split(" ")[:2]), {})
				lvbbox[" ".join(eachline.split(" ")[:2])][arg.split("-")[0]]= lvbbox[" ".join(eachline.split(" ")[:2])].get(arg.split("-")[0], eachline)
	for term in allpreds:
		if len(allpreds[term]) > 1:
			logger.warning("redudnant annotations for "+ "\n\t\t".join(allpreds[term]))
	seen = set()
	for index, eachline in enumerate(sorted(list(set(tbox)))):
		if (" ".join(eachline.split(" ")[:2]) in lvbbox or " ".join(eachline.split(" ")[:2]) in prrbox): 
			if not (" ".join(eachline.split(" ")[:2]) in lvbbox and " ".join(eachline.split(" ")[:2]) in prrbox):
				if not " ".join(eachline.split(" ")[:2]) in seen:
					seen.add(" ".join(eachline.split(" ")[:2]))
					if " ".join(eachline.split(" ")[:2]) in lvbbox:
					
						logger.warning("no LV match for "+ "".join(lvbbox[" ".join(eachline.split(" ")[:2])].values())+"\n\t\t"+"\n\t\t".join(allpoints[" ".join(eachline.split(" ")[:2])]))
					else:
						logger.warning("no PRR match for "+ "".join(prrbox[" ".join(eachline.split(" ")[:2])].values())+"\n\t\t"+"\n\t\t".join(allpoints[" ".join(eachline.split(" ")[:2])]))


			


def check_against_frames(targetfile, framefiles, seenroles = {}):

	check_basic_formatting(targetfile)
	logger.info("checking against frames for :"+ targetfile)
	osl = os.listdir(framefiles)

	for aline in [x.strip() for x in open(targetfile)]:
		fr = aline.split(" ")[4]
		roleset = aline.split(" ")[5]
		arguments = aline.split(" ")[7:]
		rightroleset = False

		if roleset+"%%"+fr in seenroles:
			rightroleset = seenroles[roleset+"%%"+fr]
		else:
			if fr+".xml" in osl:
				y = BeautifulSoup(open(framefiles+"/"+fr+".xml"))
				for somers in y.find_all("roleset"):
					if roleset == somers['id']:
						rightroleset = somers
						seenroles[roleset+"%%"+fr] = somers
		if rightroleset:
			argbox= [x.split("ARG")[1] for x in arguments if "-ARG" in x and x.split("ARG")[1].isdigit()]
			valids = [anyrole['n'] for anyrole in rightroleset.find_all('role')]
			for eacharg in argbox:
				if not eacharg in valids:
					logger.error("role missing: "+eacharg+" in "+roleset+"\n\t\t("+aline+")")
		elif ".LV" in aline:
			pass
		else:
			logger.error("roleset missing: "+roleset+"\n\t\t("+aline+")")	
	return seenroles

framesloadedinmemory = {}
framefiles = args.framefiles
if args.pointers:
	targetfile = args.pointers
	check_against_frames(targetfile, framefiles)
elif args.projectdir:
	for eachfolder, __, filelist in os.walk(args.projectdir):
		for eachfile in filelist:
			targetfile = eachfolder+"/"+eachfile
			framesloadedinmemory = check_against_frames(targetfile, framefiles, framesloadedinmemory)
elif args.allprojects:
	for eachproject in os.listdir(args.allprojects+"/corrected-raw-gold/"):
		if os.path.exists(args.allprojects+"/corrected-raw-gold/"+eachproject+"/prop/"):
			for eachfile in os.listdir(args.allprojects+"/corrected-raw-gold/"+eachproject+"/prop/"):
				targetfile = args.allprojects+"/corrected-raw-gold/"+eachproject+"/prop/"+eachfile
				framesloadedinmemory = check_against_frames(targetfile, framefiles, framesloadedinmemory)
		