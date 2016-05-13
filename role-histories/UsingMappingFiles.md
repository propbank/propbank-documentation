# Role Mappings for Propbank

These are basic files that we've used in the Propbank project to keep track of changes, and help with retrofitting and consistency.  Because not all changes are deterministic, we strongly encourage you to simply switch over to new Propbank 3.1 data when it is released, rather than to convert things yourself.  The primary value of these mappings is therefore historical, and for converting any resources that were built on top of prior Propbank annotations. 

### The Format

These mapping files are simple TSV files with the following format, from the "pb2_1_5_to_pb3_1.tsv" mapping.  
```
settlement-n	settlement.01	settlement	n	settle	settle.02	3:3	2:2	0:0	1:1
```

The first two columns define the starting point.  We are therefore talking about roleset "settlement.01", from the file "settlement-n.xml", in the 2.1.5 Propbank release.   The third and forth columns simply define the lemma and POS of the predicate, and can generally be extracted automatically from the frame file name with non-unified files.

The fifth and sixth columns are the frame file name and the roleset name in the newer format -- in this case, Propbank 3.1 -- that are being converted to. 

Finally, all columns beyond the sixth are simply mappings of the form "old argument":"new argument". Therefore ```2:2``` measn that "ARG2" of settlment.01 becomes "ARG2" in settle.02. 

A more complicated example would be:

```
ambulation-n	ambulation.01	ambulation	n	ambulate	ambulate.01	1:0	2:1	3:gol
```

That means that if you had an instance of "ambulation.01" in Propbank 2.1.5 with an ARG1, and ARG2, and ARG3, they would become ARG0, ARG1, and ARGM-GOL, respectively. 

### This is not one-to-one

Both the mappings from roleset to roleset and the mappings from argument to argument are potentially many-to-many mappings.  A few rolesets have been split. Moreover, some arguments might have multiple options -- you might see, for example, ``` 1:1	1:2```, which would mean that old ARG1 is now either ARG1 or ARG2, and needs to be manually disambiguated.


### Two kinds of deletion

Arguments labeled as "deletion" don't necessarily get literally deleted.  The "deletion" tag means that that argument should not exist for that sense, and therefore anything with that label is simply wrong and needs to be manually re-examined.  

A few rolesets are labeled as mapping to the '''DELETIONDELETION''' frame, which does not exist.  These are all rolesets that are actually non-predicative, but were framed erroneously in the past, such as "television". 

### Adjuncts never deterministically map to a numbered argument

We generally don't explicitly list ```mnr:mnr	gol:gol	cau:cau tmp:tmp ...```, but you can act like we did.  So a mapping like "cau:2" doesn't mean that all instances of ARGM-CAU arg converted into ARG2, but that they *might* get converted.  

