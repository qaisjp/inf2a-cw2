# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

from collections import defaultdict

class Lexicon:
    """stores known word stems of various part-of-speech categories"""

    def __init__(self):
        self.cat_stems = defaultdict(set)

    def add(self, stem, cat):
        self.cat_stems[cat].add(stem)

    def getAll(self, cat):
        return list(self.cat_stems[cat])

class FactBase:
    """stores unary and binary relational facts"""

    def __init__(self):
        self.unary_facts = defaultdict(list)
        self.binary_facts = defaultdict(list)

    def addUnary(self, pred, e1):
        # predicate, entity1??
        self.unary_facts[pred].append(e1)

    def addBinary(self, pred, e1, e2):
        # predicate, entity1??
        self.binary_facts[pred].append((e1, e2))

    def queryBinary(self, pred, e1, e2):
        return (e1, e2) in self.binary_facts[pred]

    def queryUnary(self, pred, e1):
        return e1 in self.unary_facts[pred]

import re
from nltk.corpus import brown 

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    global verb_stem_stream
    verb_stem_stream = -1

    verb = s # did not want to change the signature of verb_stem

    # 8. X"es" -> X"e", as long as `X` does not end with one of: i, o, s, x, z, ch, sh
    if verb.endswith("es") and not verb[:-2].endswith(("i", "o", "s", "x", "z", "ch", "sh")):
        verb_stem_stream = 8
        return verb[:-1]

    # 7. "has" -> "have"
    if verb == "has":
        verb_stem_stream = 7
        return "have"

    # 6. verb ends with "ses" or "zes", but not "sses" or "zzes"
    if verb.endswith(("ses", "zes")) and not verb.endswith(("sses", "zzes")):
        verb_stem_stream = 6
        return verb[:-1]

    # 5. X"es" -> X, as long as `X` does not end with one of: o,x,ch,sh,ss,zz
    if verb.endswith("es") and verb[:-2].endswith(("o", "x", "ch", "sh", "ss", "zz")):
        verb_stem_stream = 5
        return verb[:-2]

    # 4. X"ies" -> X"ie", where CHARACTER (not string) X is not a vowel
    #    (p.s. I know character is not a type in python)
    if len(verb) == 4 and verb.endswith("ies") and verb[0] not in "aeiou":
        verb_stem_stream = 4
        return verb[:-1]

    # 3. X"ies" -> X"y", where len(verb) >= 5, and X does not end with a vowel; snip off ies, append y
    if len(verb) >= 5 and verb.endswith("ies") and verb[-4] not in "aeiou":
        verb_stem_stream = 3
        return verb[:-3] + "y"

    # 2. X"ys" -> X"y", where X ends with a vowel; snip off s [ADDED PROTECTION FROM IndexError]
    if len(verb) >= 3 and verb.endswith("ys") and verb[-3] in "aeiou":
        verb_stem_stream = 2
        return verb[:-1]

    # 1. X"s" does not end with s,x,y,z,ch,sh, and X does not end with a vowel; snip off s
    if verb.endswith("s") and not verb[:-1].endswith(("s", "x", "y", "z", "ch", "sh", "a", "e", "i", "o", "u")):
        verb_stem_stream = 1
        return verb[:-1]

    return ""

def get_verb_stem_stream():
    return verb_stem_stream

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.

