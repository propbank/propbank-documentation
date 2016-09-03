import codecs, logging, os, nltk


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('conll formatting qc')

test =  '/home/tim/Propbank/propbank-corpus/data/google/questionbank/questionbank/00/QB-revised.v1.gold_skel'


conllformattedontonotes = "/home/tim/OthersCode/conllformattedontonotes/conll-formatted-ontonotes-5.0/conll-formatted-ontonotes-5.0/data/"
ONTOBOX = {}
for afolder, __, fileset in os.walk(conllformattedontonotes):

	for eachfile in fileset:
		if ".gold_skel" in eachfile:
			
			code = "ontonotes"+afolder.split("annotations")[1]+"/"+eachfile
			c = codecs.open(afolder+"/"+eachfile).read().strip().split("\n\n")
			ONTOBOX[code] = c


def treeline(conlllist, tree):
	u = ''
	treeleaves = [x[0] for x in tree.pos() if not x[1] == "-NONE-"]
	for index, term in enumerate(conlllist):
		u+= term.replace("*", " "+treeleaves[index]+" ")
	return u

class ConllSentence:
	def __init__(self, rawstring, ontoboxdoc=False):
		self.raw = rawstring.replace("(XX","(X")
		#print rawstring
		obo = {}
		if ontoboxdoc:

			conlltwelvedoc= "\n".join([x for x in ontoboxdoc.split("\n") if not x[0] == "#"])
			while "  " in conlltwelvedoc:
				conlltwelvedoc = conlltwelvedoc.replace("  "," ")
			conllparsebits = [arow.split(" ")[5] for arow in conlltwelvedoc.strip().split("\n")]
			conllposbits = [arow.split(" ")[4] for arow in conlltwelvedoc.strip().split("\n")]
			conllpreds = [(arow.split(" ")[2], arow.split(" ")[6]+"."+arow.split(" ")[7]) for arow in conlltwelvedoc.strip().split("\n") if not arow.split(" ")[7]=="-"]			
			#for eachpred, term in enumerate(conll)
			#obo = {}
			for pair in conllpreds:
				if not pair[1] == "-.-":
					obo[pair[0]]= (pair[1], len(obo))
			ocolumns = {}
			for eachc12row in [arow.split(" ")[11:-1] for arow in conlltwelvedoc.strip().split("\n")]:
				for c12index, eachc12column in enumerate(eachc12row):
					ocolumns[c12index] = ocolumns.get(c12index, []) + [eachc12column]
			#print ocolumns, obo
			#for term in obo:
				#print obo[term]
			#	print obo[term][0], ocolumns[obo[term][1]]
		while "  " in self.raw:
			self.raw = self.raw.replace("  "," ")
		self.rows = [x.strip().split(" ") for x in self.raw.strip("\n").split("\n")]
		self.columns = [[] for x in range(len(self.rows[0]))]
		for eachrow in self.rows:
			for columnindex, eachcolumn in enumerate(eachrow):
				try:
					self.columns[columnindex].append(eachcolumn)
				except:
					print(rawstring)
					raw_input('test')
		sentenceid= self.columns[1]
		filename = self.columns[0]
		if not len(list(set(sentenceid))) == 1:
			print("!!!!!!!!!!!!")
			logger.error("inconsistent sentence ids for sentence "+sentenceid[0]+ " file "+filename[0])
			logger.debug(str(self.raw))
		wordindices= self.columns[2]
		words =  self.columns[3]
		postags =  self.columns[4]
		temp = []
		for term in postags:
			if "-" in term:
				if term in ["-LRB-","-RRB-"]:
					temp.append(term)
				else:
					temp.append(term.split("-")[0])
			else:
				temp.append(term)
		postags = temp
		parsebits = self.columns[5]
		if ontoboxdoc and not (" ".join(parsebits) == " ".join(conllparsebits)) and not "(EDITED" in rawstring:
			logger.error("parsebits disagree with conll data  "+sentenceid[0]+ " file "+filename[0]+")\n")
			logger.debug(rawstring)
			logger.debug(eachcolumn)
			logger.debug(ontoboxdoc+"\n\n\n")
		if ontoboxdoc and (not (" ".join(postags) == " ".join(conllposbits))) and not "(EDITED" in rawstring:
			logger.error("pos tags disagree with conll data  "+sentenceid[0]+ " file "+filename[0]+")")
			logger.debug(rawstring)
			logger.debug(ontoboxdoc+"\n\n\n")
		framefiles = self.columns[6]
		rolesets = self.columns[7]
		allpredicates = self.columns[8:]

		if not map(int, wordindices) == range(min(map(int, wordindices)), max(map(int, wordindices))+1):
			logger.error("skipped or inconsistent tokens for sentence "+sentenceid[0]+ " file "+filename[0])
			logger.debug(str(self.raw))
			
		
		#print [len(x) for x in self.rows]
		if len(set([len(x) for x in self.rows])) > 1:
			logger.error("inconsistent formatting or merged rows for  "+sentenceid[0]+ " file "+filename[0])
			logger.debug(str(self.raw))
		for pid, eachcolumn in enumerate(allpredicates):
			code = "O"
			seenpred = False
			position = ""
			t = []
			sentence=''
			argbox = []
			#print eachcolumn
			for tokenid, eachtoken in enumerate(eachcolumn):
				starts = eachtoken.split("*")[0]
				ends = eachtoken.split("*")[1]
				t.append(eachtoken)
				if len(starts) > 0 and starts.count("(") > 1:
					logger.error("multiple labels on the same token in  "+sentenceid[0]+ " file "+filename[0])
					logger.debug(str(self.raw))
				elif code == "O" and len(starts) > 0:
					code = starts.replace("(","")
					argbox.append(code)
					if code == "V":
						seenpred = True
					position = "B_"
				elif len(starts) > 0 and not code == "O":
					
					logger.error("nested arguments in "+sentenceid[0]+ " file "+filename[0])
					logger.debug(str(self.raw))
					position = "B_"
					code = starts.replace("(","")
				if  position == "B_" and ends == ")":
					position = "S_"
				elif ends == ")" and position == "I_":
					position = "E_"
				elif ends == ")" and position == "":
					logger.error("extra closing bracket in  "+sentenceid[0]+ " file "+filename[0])
					logger.debug(str(self.raw))
				sentence += words[tokenid]+"/"+position+code+" "
				if position == "E_" or position == "S_":
					code = "O"
					position = ""
				if position == "B_":
					position = "I_"
				
			#print sentence
			
			if not len([x for x in argbox if x.replace("ARG","").isdigit()]) == len(list(set([x for x in argbox if x.replace("ARG","").isdigit()]))):
				print sentence
				logger.error("multiple same-named numbered args in  "+sentenceid[0]+ " file "+filename[0])
			if not seenpred:

				logger.error("missing or deleted verb for  "+sentenceid[0]+ " file "+filename[0]+" predicate #"+str(pid)+"("+" ".join(eachcolumn)+")")
				logger.debug(rawstring)
				logger.debug(eachcolumn)

		if ontoboxdoc:
			for eachc12pred in obo:
				hasmatch = False
				goodmatch = False
				#print obo[eachc12pred]
				#print rolesets[int(eachc12pred)]
				#print ocolumns[obo[eachc12pred][1]]
				predpoint = 0
				for rid, point in enumerate(rolesets):

					#print str(rid), point, predpoint
					if str(point) == "-":
						pass
					else:
						#print predpoint
						#print allpredicates
						#print rawstring\
						
						if str(rid) == eachc12pred:
							hasmatch = True
							other = " ".join(ocolumns[obo[eachc12pred][1]])
							current = " ".join(allpredicates[predpoint])
							if other == current:
								goodmatch = True
							elif " ".join(allpredicates[predpoint]) == " ".join(ocolumns[obo[eachc12pred][1]]).replace("(V*) *", "(V* *)"):
								logger.info("disagreeement due to dropped particle in conll12 recovered")
							elif " ".join(allpredicates[predpoint]) == " ".join(ocolumns[obo[eachc12pred][1]]).replace("(V*) (ARG1*) *", "(V*) (ARG1*) (C-V*)"):
								logger.info("disagreeement due to dropped discontinousu particle in conll12 recovered")
							elif " ".join(allpredicates[predpoint]) == " ".join(ocolumns[obo[eachc12pred][1]]).replace("(V*) (ARG1* *) *", "(V*) (ARG1* *) (C-V*)"):
								logger.info("disagreeement due to dropped discontinousu particle in conll12 recovered")
							elif " ".join(allpredicates[predpoint]) == " ".join(ocolumns[obo[eachc12pred][1]]).replace("(V*) (ARG2*) *", "(V*) (ARG2*) (C-V*)"):
								logger.info("disagreeement due to dropped discontinousu particle in conll12 recovered")
							else:
								#print other, "(conll12)"
								#print current, "(current)"
								itstree= codecs.open("/home/tim/Propbank/propbank-private-parse/ontonotes/parse/"+filename[0].replace("ontonotes/","")+".parse",'r','utf-8').read().split("\n\n")[int(sentenceid[0])]
								
								if False:
									try:
										print treeline(ocolumns[obo[eachc12pred][1]], nltk.Tree.fromstring(itstree))
										print treeline(allpredicates[predpoint], nltk.Tree.fromstring(itstree))
									except:
										print "probably an ascii encoding issue"
									print filename[0]+" "+ sentenceid[0]
									print "\n"
								#print " ".join(postags)
								#print goodmatch
								#print obo
								#print ocolumns
								#print rawstring

								#print "!!!!!!!!!!!!!"
						#print ocolumns[obo[eachc12pred][1]]
						predpoint +=1 
				if not hasmatch:
					pass
					#print obo
					#print ocolumns
					#print rawstring

								
			
			#print eachcolumn

def testfilename(test, ontoboxdoc=False):
	#print "testing ", testing
	for sid, cs in enumerate(codecs.open(test, 'r','utf-8').read().split("\n\n")):
		if cs.strip() != '':

			if ontoboxdoc and sid < len(ontoboxdoc):
				o = ontoboxdoc[sid]
			else:
				o = False
			ConllSentence(cs, o)

for anyfolder, __, fileset in os.walk("/home/tim/Propbank/propbank-corpus/data/"):
	if not "ontonotes/" in anyfolder:
		obox = False
	for eachfile in fileset:
		if ".gold_skel" in eachfile:
			code = anyfolder.split("propbank-corpus/data/")[1]+"/"+eachfile
			testfilename(anyfolder+"/"+eachfile, ONTOBOX.get(code, False))
		if ".gold_conll" in eachfile:
			code = anyfolder.split("propbank-corpus/data/")[1]+"/"+eachfile
			testfilename(anyfolder+"/"+eachfile, ONTOBOX.get(code, False))