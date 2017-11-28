# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?
# tagset = ["P", "A", "Ns", "Np", "Is", "Ip", "Ts", "Tp", "BEs", "BEp", "DOs", "DOp", "AR", "AND", "WHO", "WHICH", "?"]

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    plurals = set()
    singular = set()
    with open("sentences.txt", "r") as f:
        for line in f:
            for tagged_word in line.split(" "):
                word, tag = tagged_word.split("|")
                if tag == "NN":
                    singular.add(word)
                elif tag == "NNS":
                    plurals.add(word)

    return list(singular.intersection(plurals))


unchanging_plurals_list = unchanging_plurals()

def noun_stem(s):
    """extracts the stem from a plural noun, or returns empty string"""    
    noun = s
    if noun in unchanging_plurals_list:
        return noun

    if noun.endswith("men"):
        return noun[:-3] + "man"

    return threes_stem(noun)

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    tags = set()

    # OK!
    for word, tag in function_words_tags:
        if word == wd:
            tags.add(tag)


    # PANTI: proper and adjectives
    for tag in "PA":
        if wd in lx.getAll(tag):
            tags.add(tag)

    # Lexicon only contains singular versions of nouns
    # So if this word is equal is equal to the one in the lexicon
    # we know this one is singular
    if wd in lx.getAll("N"):
        tags.add("Ns")

    # Lexicon only contains singular versions of nouns
    # so if the singular version of this word is in the lexicon
    # we know this one is plural (because noun_stem returns an empty string for singulars)
    if noun_stem(wd) in lx.getAll("N"):
        tags.add("Np")

    # Transitive verbs..
    verb_stem_wd = verb_stem(wd)
    for tag in "TI":
        tagged_words = lx.getAll(tag)
        if wd in tagged_words:
            tags.add(tag + "p")
        if verb_stem_wd in tagged_words:
            tags.add(tag + "s")

    return list(tags)



def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.