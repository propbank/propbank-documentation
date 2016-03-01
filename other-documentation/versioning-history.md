### Propbank versioning

Propbank has often been annotated in a rolling manner, so this is a bit of a post-hoc versioning of prior work.  

MAJOR version number changes express full systemic changes that include formatting differences; they require not just retraining but perhaps recoding. There are only three:
* **1.x** The "Verbs" era: Propbank 1 releases in which everything is a verb by default (no encoding of POS). 
* **2.x** Part-of-Speech separation era: Frame files have a -n, -j, or -v suffix which encodes their part of speech.
* **3.x** Unification era: Frame files have "unified" rolesets representing multiple lemmas, and "alias" fields which encode those lemmas and their parts of speech.

#### Propbank 2.0 (Ontonotes/BOLT)
Within 2.0, we had many many different releases of frames. 
* 2.0 Anything released before Ontonotes
* 2.1 Ontonotes propbank annotation
 * Ontonotes versions 1,2,3,4,5 are therefore (2.1.1, 2.1.2, 2.1.3, 2.1.4, and 2.1.5)
 * for reference: AMR Phase 1 was annotated using the verbal frames in 2.1.4. 
* 2.2. BOLT annotation
 * 2.2.1 BOLT DF 1 release
 * 2.2.2 BOLT DF 2 release
 ...
 * 2.2.8 BOLT SMS 1 release
 * 2.2.9 BOLT SMS 2 release

#### Propbank 3.0 (Unification)
Around the release of BOLT SMS 2, we started the giant overhaul into "Unification" frames. 
* 3.0 Everything before the big Ontonotes re-release
 * AMR Phase 2 is now in line with Propbank 3.0.
* 3.1 Ontonotes unified release.  
 * After 3.1, PATCH releases will simply add frames or arguments, and MINOR releases will add or change arguments. 
