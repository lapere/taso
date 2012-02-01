# -*- coding: utf-8 -*-

import os
from UserDict import *
from code import *
import imp

class ItemDB(IterableUserDict):
    
    def __init__(self):
        IterableUserDict.__init__(self)
        self.cnt = dict()
        self.tools = dict()
        self.load_tools()
                        
    def update_basetag(self, base_tag):           
        if self.cnt.has_key(base_tag):
            self.cnt[base_tag] = self.cnt[base_tag] + 1
        else:
            self.cnt[base_tag] = 1

    def load_tools(self):
        fp, pathname, description = imp.find_module("tools")  
        try:
            module = imp.load_module("tools", fp, pathname, description)
            self.tools.update(module.__dict__)
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()

    def add_item(self, item):
        self[item.tag] = item
        self.tools[item.tag] = item
        self.recalc()
        
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

        odict['tools'] = None
        
        return odict

class Item:
    
    def __init__(self, db, base_tag, formula):
        db.update_basetag(base_tag)
        self.tag = base_tag + str(db.cnt[base_tag])
        
        self.formula = formula
        self.value = None
        self.names = []
        self.db = db
        self.find_deps()
        db.add_item(self)
        
    def find_deps(self):
        self.code = compile_command(self.formula)
        for name in list(self.code.co_names):
            if not self.db.has_key(name):
                self.names.append(name)
                
        self.code = compile_command("self.value=" + self.formula)

    def new_formula(self, kaava):
        self.formula = kaava
        self.find_deps()
        self.calc()
        
    def calc(self):
        try:
            eval(self.code, dict(self.db.tools), locals())
        except:
            pass

    """
    def __call__(self, value = None):
        if value:
            if not self.names:
                self.new_formula(str(value))
                self.calc()
        else:
            return self.value     
    """
    
    def __otyp(self, other):
        if isinstance(other, Item):
            return other.value
        else:
            return other

    def __add__(self, other):
        return self.value + self.__otyp(other)

    __radd__ = __add__

    def __sub__(self, other):
	return self.value - self.__otyp(other)

    def __rsub__(self, other):
	return self.__otyp(other) - self.value

    def __mul__(self, other):
	return self.value * self.__otyp(other)

    __rmul__ = __mul__

    def __div__(self, other):
	return self.value / self.__otyp(other)

    def __rdiv__(self, other):
	return self.__otyp(other) / self.value

    def __pow__(self, n, z=None):
	return pow(self.value, n, z)

    def __rpow__(self, base):
	return pow(base, self.value)

    def __neg__(self):
	return -self.value

    def __pos__(self):
	return +self.value

    def __abs__(self):
	return abs(self.value)

    def __int__(self):
	return int(self.value)

    def __long__(self):
	return long(self.value)

    def __float__(self):
	return float(self.value)

    def __nonzero__(self):
	return not (self.value == 0)

    def __xor__(self, other):
        return pow(self.value, other)

    # String operations
    """
    def __str__(self):
	return str(self.value)
    def __getslice__(self, i,j):
	return str(self)[i:j]

    def __len__(self): 
	return len(str(self.value))
    """


if __name__ == '__main__':

    db = ItemDB()

    while True:
        raw = raw_input("PR:>")
        raw = raw.split("=")
        if len(raw) == 2:
            solu = raw[0].strip()
            kaava = raw[1].strip()
            if solu and kaava:
                if items.has_key(solu):
                    items[solu].new_formula(kaava)
                else:
                    Item(db, solu, kaava)
                db.recalc()
        for i in db:
            print i,"=",db[i].value,"  [",db[i].formula,"]",db[i]
        
        
        
