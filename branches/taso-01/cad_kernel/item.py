# -*- coding: utf-8 -*-
from code import *

class Item:
    
    def __init__(self, db, base_tag, formula):
        self.tag = db.update_basetag(base_tag)
        db.register_item(self)
        self.code = None
        self.value = None
        self.names = dict()
        self.slaves = dict()
        self.db = db
        if formula:
            if self.find_deps(formula):
                self.calc()
	else:
            self.formula = False

    
    def find_deps(self, formula):
        """etsii alkion muuttujat"""
        try:
            tmp_code = compile_command(formula)
        except SyntaxError, detail:
            print "Syntax error kohdassa:", detail.offset
            return False
        
        co_names = list(tmp_code.co_names)
        
        if self.tag in  co_names:
            print "Viittaus itseensä:", self.tag, co_names
            return False

        tmp_names = dict()
        for name in list(tmp_code.co_names):
            if self.db.has_key(name):
                tmp_names.update({name : self.db[name]})
                if self.db[name].names.has_key(self.tag):
                    print "Circular reference", name, self.tag
                    return False
                #else:
                    #    self.db[name].slaves.update({self.tag : self})
        
        # minä self, en ole enää vanhojen isäntien orja
        for name in self.names:
            if self.db[name].slaves.has_key(self.tag):
                self.db[name].slaves.pop(self.tag)
       
        # vaan uusien isäntien orja
        self.names = tmp_names
        for name in self.names:
            self.db[name].slaves.update({self.tag: self})
 
        self.formula = formula
        self.code = compile_command(self.tag + ".value = " + self.formula)
        return True
        
    def new_formula(self, kaava):
        "vaihtaa alkion kaavan"
        if self.find_deps(kaava):
            self.calc()
        
    def calc(self):
        "laskee alkion arvon"
        try:
            self.db.ic.runcode(self.code)
            for s in self.slaves:
                self.slaves[s].calc()
        except RuntimeError, detail:
            print detail
            for s in self.slaves:
                print s,
                self.slaves[s].calc()
        except  Exception, detail:
            print detail

    """matemaattiset operaattorit luokalle"""

    def __add__(self, other):
        return self.value + other 

    __radd__ = __add__

    def __sub__(self, other):
	return self.value - other

    def __rsub__(self, other):
	return other - self.value

    def __mul__(self, other):
	return self.value * other

    __rmul__ = __mul__

    def __div__(self, other):
	return self.value / float(other)

    def __rdiv__(self, other):
	return float(other) / self.value

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
    
    def __str__(self):
    	return str(self.value)

    def __len__(self): 
	return len(str(self.value))
        
    def __getstate__(self):    
        odict = self.__dict__.copy() # copy the dict since we change it    
        odict['code'] = None
        return odict

    def __setstate__(self, dicti):
        if dicti:
            self.__dict__.update(dicti)
        self.code = compile_command(self.tag + ".value = " + self.formula)
        
        
            
        
        
        
