# -*- coding: utf-8 -*-
import os
from UserDict import *
from code import *
import imp
from item import Item

class ItemDB(IterableUserDict):
    
    def __init__(self, ic):
        "konstruktori"
        IterableUserDict.__init__(self)
        self.cnt = dict()
        self.ic = ic
                        
    def update_basetag(self, base_tag):
        "alkioiden automaattinen numerointi"
        if not self.cnt.has_key(base_tag):
            self.cnt[base_tag] = 1
            
        while True:
            tag = base_tag + str(self.cnt[base_tag])
            if not self.has_key(tag):
                return tag
            self.cnt[base_tag] = self.cnt[base_tag] + 1

    def register_item(self, item):
        "rekisteröi alkion tietokantaan"       
        self[item.tag] = item
        self.ic.locals[item.tag] = item
	
    def connect_to_canvas(self, canvas):
        self.user_vars.update(canvas.__dict__)

    def recalc(self):
        "Recalculate all formulas in the spreadsheet"
        # We need to compute a topological sort of formula cells,
        # based on the dependency graph.
        # This will loop forever if there's a cycle, but that
        # shouldn't matter now, because __setitem__ won't let you
        # create cycles.
        L=[]			# Topologically sorted list of coords
        output={}		# Keep track of cells output so far

        # Loop until all the cells have been output
        while len(output) < len(self):
            # We loop over all the cells
            for k in self.keys():
                # If the cell has already been output, skip it
                if output.has_key(k):
                    continue  
                # Count the number of cells on which this cell
                #depends, and that have not been output yet,
                count = 0
                for cell in self[k].names:
                    if (self.has_key(cell) and 
                        (not output.has_key(cell))):
                        count = count + 1
                if count==0: 
                    L.append(k)
                    output[k] = None
        

        # Loop over all the cells holding Formula instance, and
        # compute new values for them
        
        for tag in L:
            self[tag].calc()
    
    def __getstate__(self):    
        odict = self.__dict__.copy() # copy the dict since we change it            
        odict["ic"] = None
        return odict

    def __setstate__(self, dicti):
        if dicti:
            self.__dict__.update(dicti)
       




            
if __name__ == "__main__":
    ic = InteractiveConsole() 
    
    " Testipenkki ohjelmalle \n \
    PR:>a = 10 \n \
    a1 = 10   [ 10 ] \n \
    PR:>b = 20 \n \
    a1 = 10   [ 10 ] \n \
    b1 = 20   [ 20 ] \n \
    PR:>c = a1 + b1 * 0.1 \n \
    a1 = 10   [ 10 ] \n \
    c1 = 12.0   [ a1 + b1 * 0.1 ] \n \
    b1 = 20   [ 20 ] \n \
    PR:> \n \
    "
    
    db = ItemDB(ic)
    last = Item(db, "X", "100")
    for i in range(500):
        last = Item(db, "X", "%s + 1" % last.tag)            
    import pickle
    fn = "/tmp/koe"
    fd = open(fn,'w+')
    #pickle.dump(db, fd)
    #fd.close()
    
    
    #db = pickle.load(open(fn))
    #db.ic = ic
    #for i in db:
    #    db.ic.locals[i] = db[i]
        
    #db = ItemDB(InteractiveConsole())
    while True:
        raw = raw_input("PR:>")
        raw = raw.split("=")
        if len(raw) == 2:
            solu = raw[0].strip()
            kaava = raw[1].strip()
            if solu and kaava:
                if db.has_key(solu):
                    db[solu].new_formula(kaava)
                else:
                    Item(db, solu, kaava)
        elif len(raw) == 1:
            i = raw[0]
            if db.has_key(i):
        #for i in db:
                print i,"=",db[i].value, db[i].formula, db[i].slaves.keys()#, db[i].code # type(db[i].value),"  [",db[i].formula,"]", "names=",db[i].names 
                #for k in db.ic.locals:
                #    if k[0] == "s":
                #        print k
