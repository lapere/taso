# -*- coding: utf-8 -*-

import pickle

letters = pickle.load(open('save.p'))
print "chr = {",
for kw in letters:
    print "\"%s\":%s," % (kw, str(letters[kw]))
print "}"
