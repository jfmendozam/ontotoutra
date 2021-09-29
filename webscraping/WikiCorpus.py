#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 11:48:59 2018

@author: Tom De Smedt (Computational Linguistics Research Group, University of Antwerp)
@url: https://www.cnts.ua.ac.be/pages/using-wikicorpus-nltk-to-build-a-spanish-part-of-speech-tagger
"""

from glob import glob
from collections import defaultdict
from codecs import open, BOM_UTF8

from nltk.tag import UnigramTagger
from nltk.tag import FastBrillTaggerTrainer
 
from nltk.tag.brill import SymmetricProximateTokensTemplate
from nltk.tag.brill import ProximateTokensTemplate
from nltk.tag.brill import ProximateTagsRule
from nltk.tag.brill import ProximateWordsRule

class WikiCorpus:
    """ Wiki spanish corpus """


    def __init__(self):
        """ Default constructor """

        self.corpusDirectory = "/run/media/jf/Datos/Tourist Text Mining/wikicorpus/tagged.es/"
        self.lexiconFilename = "es-lexicon.txt"
        self.contextFilename = "es-context.txt"
        self.words = 100000000
        self.topWords = 100000


    def getCorpus(self, start = 0):
        """ Reading the Spanish Wikicorpus """

        s = [[]]
        i = 0
        for f in glob(self.corpusDirectory + "*")[start:]:
            for line in open(f, encoding="latin-1"):
                if line == "\n" or line.startswith((
                  "<doc", "</doc>", "ENDOFARTICLE", "REDIRECT",
                  "Acontecimientos",
                  "Fallecimientos",
                  "Nacimientos")):
                    continue
                w, lemma, tag, x = line.split(" ")
                if tag.startswith("Fp"):
                    tag = tag[:3]
                elif tag.startswith("V"):  # VMIP3P0 => VMI
                    tag = tag[:3]
                elif tag.startswith("NC"): # NCMS000 => NCS
                    tag = tag[:2] + tag[3]
                else:
                    tag = tag[:2]
                for w in w.split("_"):
                    s[-1].append((w, tag)); i += 1
                if tag == "Fp" and w == ".":
                    s.append([])
                if i >= self.words:
                    return s[:-1]


    def getLexicon(self):
        """ Extracting a lexicon of known words """

        lexicon = defaultdict(lambda: defaultdict(int))

        for sentence in self.getCorpus():
            for w, tag in sentence:
                lexicon[w][tag] += 1

        top = []
        for w, tags in lexicon.items():
            freq = sum(tags.values())
            tag  = max(tags, key = tags.get)
            top.append((freq, w, tag))

        top = sorted(top, reverse = True)[:self.topWords]
        top = ["%s %s" % (w, tag) for freq, w, tag in top if w]

        open(self.lexiconFilename, "wb")\
            .write(BOM_UTF8 + "\n".join(top).encode("utf-8"))


    def getContextualRules(self):
        """ Extracting contextual rules using Brill's algorithm """

        sentences = self.getCorpus()
        ANONYMOUS = "anonymous"
        for s in sentences:
            for i, (w, tag) in enumerate(s):
                if tag == "NP": # NP = proper noun in Parole tagset.
                    s[i] = (ANONYMOUS, "NP")

        ctx = [ # Context = surrounding words and tags.
            SymmetricProximateTokensTemplate(ProximateTagsRule,  (1, 1)),
            SymmetricProximateTokensTemplate(ProximateTagsRule,  (1, 2)),
            SymmetricProximateTokensTemplate(ProximateTagsRule,  (1, 3)),
            SymmetricProximateTokensTemplate(ProximateTagsRule,  (2, 2)),
            SymmetricProximateTokensTemplate(ProximateWordsRule, (0, 0)),
            SymmetricProximateTokensTemplate(ProximateWordsRule, (1, 1)),
            SymmetricProximateTokensTemplate(ProximateWordsRule, (1, 2)),
            ProximateTokensTemplate(ProximateTagsRule, (-1, -1), (1, 1)),
        ]
        
        tagger = UnigramTagger(sentences)
        tagger = FastBrillTaggerTrainer(tagger, ctx, trace = 0)
        tagger = tagger.train(sentences, max_rules = 100)
        
        ctx = []
         
        for rule in tagger.rules():
            a = rule.original_tag
            b = rule.replacement_tag
            c = rule._conditions
            x = c[0][2]
            r = c[0][:2]
            if len(c) != 1: # More complex rules are ignored in this script. 
                continue
            if isinstance(rule, ProximateTagsRule):
                if r == (-1, -1): cmd = "PREVTAG"
                if r == (+1, +1): cmd = "NEXTTAG"
                if r == (-2, -1): cmd = "PREV1OR2TAG"
                if r == (+1, +2): cmd = "NEXT1OR2TAG"
                if r == (-3, -1): cmd = "PREV1OR2OR3TAG"
                if r == (+1, +3): cmd = "NEXT1OR2OR3TAG"
                if r == (-2, -2): cmd = "PREV2TAG"
                if r == (+2, +2): cmd = "NEXT2TAG"
            if isinstance(rule, ProximateWordsRule):
                if r == (+0, +0): cmd = "CURWD"
                if r == (-1, -1): cmd = "PREVWD"
                if r == (+1, +1): cmd = "NEXTWD"
                if r == (-2, -1): cmd = "PREV1OR2WD"
                if r == (+1, +2): cmd = "NEXT1OR2WD"
            ctx.append("%s %s %s %s" % (a, b, cmd, x))
         
        open(self.contextFilename, "wb")\
            .write(BOM_UTF8 + "\n".join(ctx).encode("utf-8"))
