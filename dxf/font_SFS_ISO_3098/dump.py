# -*- coding: utf-8 -*-

import pickle

letters = pickle.load(open('save.p'))
print "chr = {",
for kw in letters:
    for line in letters[kw]:
        print "\"%s\":%s," % (kw, str(letters[kw]))
print "}"
