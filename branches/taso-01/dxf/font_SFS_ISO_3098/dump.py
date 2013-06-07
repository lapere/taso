# -*- coding: utf-8 -*-

import pickle

letters = pickle.load(open('save.p'))
for kw in letters:
	print "\"%s\":%s," % (kw, letters[kw])
