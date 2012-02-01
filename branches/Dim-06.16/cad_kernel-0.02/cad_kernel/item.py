# -*- coding: utf-8 -*-
from code import *

class Item:
    
    def __init__(self, db, base_tag, formula):
        self.tag = db.update_basetag(base_tag)
        db.register_item(self)
        self.code = None
        self.value = None
        self.names = []
        self.db = db
        if formula != None:
            self.formula = str(formula)
            self.find_deps()
            self.calc()
	else:
            self.formula = None

    def has_circular_ref(self, names):
        "käy rekursiivisesti läpi viittaukset etsien takaisin viittauksia"
        pass
        """
        while len(names):
            if self.tag in names: 
                return True
            if self.db.has_key(names[0]):
                c = self.db[ names[0] ]
                names = names + c.names
            names = names[1:]
    
        return False
        """
    
    def find_deps(self):
        "etsii alkion riippuvuudet ts. muuttujat jotka sen arvoon vaikuttavat"
        self.code = compile_command(self.formula)
        tmp_names = []
        
        for name in list(self.code.co_names):     
            tmp_names.append(name)
            if self.db.has_key(name):
                tmp_names.extend(self.db[name].names)

        if self.has_circular_ref(tmp_names):
            print "Circular reference"
        else:
            self.names = tmp_names
            self.code = compile_command("self.value=" + self.formula)


    def new_formula(self, kaava):
        "vaihtaa alkion kaavan"
        self.formula = kaava
        self.find_deps()
        self.calc()
        
    def calc(self):
        "laskee alkion arvon"
        try:
            eval(self.code, dict(self.db.user_vars), locals())
        except:
            pass

    def __call__(self):
        return self

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
        
        
        
