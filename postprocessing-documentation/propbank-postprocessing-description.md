## Post-processing

This document purely explains the difference between what is manually annotated in Propbank and what is produced as "post-processed" Propbank pointers.


#### Following all treebank coreference indices

We assume that an annotator is annotating the argument that is within the scope of the predicate.  In many cases this is an empty argument: for example, one might annotate the ```(NP-SBJ (-NONE- *T*-2)``` 
below as the "ARG0" of make below:

```
(TOP (S (NP-SBJ (NP (NNP Lorillard)
                    (NNP Inc.))
                (, ,)
                (NP (NP (NP (DT the)
                            (NN unit))
                        (PP (IN of)
                            (NP (ADJP (NML (NNP New)
                                           (NNP York))
                                      (HYPH -)
                                      (VBN based))
                                (NNP Loews)
                                (NNP Corp.))))
                    (SBAR (WHNP-2 (WDT that))
                          (S (NP-SBJ (-NONE- *T*-2))
                             (VP (VBZ makes)
                                 (NP (NNP Kent)
                                     (NNS cigarettes))))))
                (, ,))
        (VP (VBD stopped)
            (VP (VBG using)
                (NP (NN crocidolite))
                (PP-LOC-CLR (IN in)
                            (NP (PRP$ its)
                                (NN Micronite)
                                (NN cigarette)
                                (NNS filters)))
                (PP-TMP (IN in)
                        (NP (CD 1956)))))
        (. .)))
```
In early forms of Propbank, annotators also would then manually link to ```(WHNP-2 (WDT that)``` and up to the NP "the unit of New York-basesd Loews Corp.".  Post-processing is done using a variant of the clearnlp "PBpostprocess"
script, and automatically makes those links, adds those Treebank locations to the pointer, and adds a LINK-SLC chain which shows links between relative clauses and their modified elements.  

The post-processing scripts also automatically fill in links between reduced relative clause empty categories and their modified heads, such as the link between ```(NP (-NONE- *))``` and "A form of asbestos" in:
```
(TOP (S (S-TPC-1 (NP-SBJ (NP (NP (DT A)
                                 (NN form))
                             (PP (IN of)
                                 (NP (NN asbestos))))
                         (VP (ADVP-TMP (RB once))
                             (VBN used)
                             (NP (-NONE- *))
                             (S-CLR (NP-SBJ (-NONE- *PRO*))
                                    (VP (TO to)
                                        (VP (VB make)
                                            (NP (NNP Kent)
                                                (NN cigarette)
                                                (NNS filters)))))))

```

In addition, the post-processing adds links included by other Treebank empty categories, as in *RNR*, *ICH*, and *EXP* elements.   



#### Corrections

Certain kinds of annotations were automatically corrected, which are assumed to be both invalid and correctable.  For example, arguments which are lower than expected on an annotation are promoted to 
have a shorter path.  Nested arguments are flagged and may be removed as well; during quality control, annotations are checked for nested arguments and corrected if necessary.


