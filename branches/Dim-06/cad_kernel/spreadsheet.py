#!/usr/bin/env python

import sys, string, types, re
import rexec, Bastion
from math import *

Error="Spreadsheet error"

def yx2str(y,x):
    "Convert a coordinate pair like 1,26 to AA2"
    if x<26: s=chr(65+x)
    else:
	x=x-26
	s=chr(65+ (x/26) ) + chr(65+ (x%26) )
    s=s+str(y+1)
    return s

coord_pat = re.compile('^(?P<x>[a-zA-Z]{1,2})(?P<y>\d+)$')

def str2yx(s):
    "Convert a string like A1 to a coordinate pair like 0,0"
    match = coord_pat.match(s)
    if not match: return None
    y,x = match.group('y', 'x')
    x = string.upper(x)
    if len(x)==1: x=ord(x)-65
    else:
	x= (ord(x[0])-65)*26 + ord(x[1])-65 + 26
    return string.atoi(y)-1, x

# Some assertions to be sure that yx2str and str2yx are correct
assert yx2str(0,0) == 'A1'
assert yx2str(1,26) == 'AA2'
assert str2yx('AA2') == (1,26)
assert str2yx('B2') == (1,1)


class Formula:
    """A Formula instance has three attributes:
    formula -- the string entered by the human
    eval_str -- the formula, modified for evaluation: A1 -> CELL(self,'A1')
    value -- the actual value of this cell"""

    def __init__(self, formula):
	"""formula is a string containing the formula """  
	self.formula = formula
	self.value = 0.0

	# Modify the formula to be a string we can eval().  
	# Cell references are mutated to calls to the CELL constructor. 
	# Ex.: 'A1 + B2' becomes '(CELL(self, "A1") + CELL(self, "B2")'

	self.cells = []
	self.eval_str = re.sub(r"\b([A-Za-z]+[0-9]+)\b", 
			       self.__subfunc, formula)
	
	# Since we'll be comparing .cells lists, the lists have to be
	# in a canonical order
	self.cells.sort()		

    # Private function used in the substitution in the __init__ method
    def __subfunc(self, match):
	cell = match.group(1)
	t = str2yx(cell)
	if t not in self.cells: 
	    self.cells.append( t )
	return 'CELL(self, "%s")' % (cell,)

    def __repr__(self):
	return '<Formula: ' + self.formula + '>'

#    def clone(self):
#	"Return a copy of this formula object"
#	new = Formula(self.formula)
#	new.value = self.value
#	return new


# We need a CELL class to hold cell references; it must be possible to
# perform operations on this class, yet it must also be possible to
# get the coordinate to which the cell refers.  There are two ways in
# which it will be used:
#  A1 + A2 -> CELL(A1) + CELL(A2)
#  sum(A1, B4) -> sum( CELL(A1), CELL(B4) )

class CELL:
    def __init__(self, SS, key):
	self.SS = SS
	self.key = key
	if type(key) == types.TupleType: 
	    self.y, self.x = key
	elif type(key) == types.StringType:
	    self.y, self.x = str2yx(key)

	# We need to set the value of the instance, which could be
	# a formula or a Python data type.
	value = self.SS[self.y, self.x]
	if isinstance(value, Formula): value=value.value
	self.value = value

    def __add__(self, other):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if isinstance(other, CELL): other =  other.SS[other.key]
	if isinstance(other, Formula): other = other.value
	if myval is None or other is None:
	    raise ValueError, "Reference to empty cell"
	return myval+other

    __radd__ = __add__

    def __sub__(self, other):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if isinstance(other, CELL): other =  other.SS[other.key]
	if isinstance(other, Formula): other = other.value
	if myval is None or other is None:
	    raise ValueError, "Reference to empty cell"
	return myval - other

    def __rsub__(self, other):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if isinstance(other, CELL): other =  other.SS[other.key]
	if isinstance(other, Formula): other = other.value
	if myval is None or other is None:
	    raise ValueError, "Reference to empty cell"
	return other - myval

    def __mul__(self, other):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if isinstance(other, CELL): other =  other.SS[other.key]
	if isinstance(other, Formula): other = other.value
	if myval is None or other is None:
	    raise ValueError, "Reference to empty cell"
	return myval * other
    __rmul__ = __mul__

    def __div__(self, other):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if isinstance(other, CELL): other =  other.SS[other.key]
	if isinstance(other, Formula): other = other.value
	if myval is None or other is None:
	    raise ValueError, "Reference to empty cell"
	return myval / other

    def __rdiv__(self, other):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if isinstance(other, CELL): other =  other.SS[other.key]
	if isinstance(other, Formula): other = other.value
	if myval is None or other is None:
	    raise ValueError, "Reference to empty cell"
	return other / myval

    def __pow__(self, n, z=None):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if myval is None:
	    raise ValueError, "Reference to empty cell"
	return pow(myval, n, z)

    def __rpow__(self, base):
	return pow(base, self)

    def __neg__(self):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if myval is None:
	    raise ValueError, "Reference to empty cell"
	return -myval

    def __pos__(self):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if myval is None:
	    raise ValueError, "Reference to empty cell"
	return +myval

    def __abs__(self):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if myval is None:
	    raise ValueError, "Reference to empty cell"
	return abs(myval)

    def __int__(self):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if myval is None:
	    raise ValueError, "Reference to empty cell"
	return int(myval)

    def __long__(self):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if myval is None:
	    raise ValueError, "Reference to empty cell"
	return long(myval)

    def __float__(self):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if myval is None:
	    raise ValueError, "Reference to empty cell"
	return float(myval)

    def __nonzero__(self):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	if myval is None:
	    raise ValueError, "Reference to empty cell"
	return not (myval == 0)

    # String operations
    def __str__(self):
	myval = self.SS[self.key]
	if isinstance(myval, Formula): myval=myval.value
	return str(myval)
    def __getslice__(self, i,j):
	return str(self)[i:j]
    def __len__(self): 
	return len(str(self))

    def cos(self):
        myval = self.SS[self.key]
        if isinstance(myval, Formula): myval=myval.value
        return cos(radians(val))

    def sin(self):
        myval = self.SS[self.key]
        if isinstance(myval, Formula): myval=myval.value
        return sin(radians(val))
    
class Spreadsheet:
    """The Spreadsheet class can serve as a basis for developing
    Python spreadsheet-like applications, by writing logic to render
    its contents.  It's probably a bad idea to subclass it for this
    purpose, since that would make pickling difficult.  Formulas are
    evaluated in a restricted execution environment, though I'm not
    sure if pickle/unpickle provides a security risk.  

    Methods:
    __setitem__ -- The value can be a string, a number, or Formula instance.
    __getitem__ -- There are several different possible return values.
    	None : The cell has been given no value
	A string or number: The value stored in the cell
	A Formula instance F: F.value is the formula's value, and
	                      F.formula is a string containing the formula
    __delitem__ -- clear the cell at the given coordinate
    recalc() -- Recalculate the values of all formulas in the spreadsheet

    The keys can be either a tuple giving the y,x coordinates, like
    (2,0), or a string containing a cell reference, like "A3".
    """
    def __init__(self):
	self.dep = {}            # Dict for dependencies between cells
	self.data = []           # List of lists that will hold the data

	# This will hold a topologically sorted list of coordinates.
	# Initially the empty list is accurate
	self.__calc_cells = []   
	self.__calc_cells_accurate = 1


    def __setitem__(self, key, value):
	"""Set a cell to a new value.  
	key -- the cell's location, in either text or tuple format
	value -- the cell's new value, which can be either a simple
	     Python data type like a string or number, or 
	     a Formula instance.
        """
	#print key, value
	if type(key) == types.TupleType:
	    yp, xp = key			# Unpack the tuple
	elif type(key) == types.StringType:     
	    yp, xp = str2yx(key)
	else:
	    raise KeyError, "Unexpected key "+repr(key)

	oldvalue = self[yp,xp]

	if type(value) in [types.IntType, types.FloatType, 
			   types.LongType, types.ComplexType,
			   types.StringType]:
	    # The value doesn't need any special processing if it's a
	    # simple Python type.

	    # If overwriting a formula, we have to remove it from 
	    # the dependency dict
	    if isinstance(oldvalue, Formula): 
 	        self.__calc_cells_accurate = 0
	        del self.dep[yp,xp]

        elif isinstance(value, Formula):
	    # We're inserting a formula
	    # print value.cells
	    self.dep[yp,xp] = value.cells

	    # When setting a formula, we must invalidate the computed
	    # dependencies if either the old value was not a formula,
	    # or it was a formula which depended on different cells
	    # (and hence has a different .cells attribute).  This
	    # means we must also check for a circular reference.
	    # Otherwise, we can leave the dependencies alone.
	    if not (isinstance(oldvalue, Formula) and 
		    oldvalue.cells == value.cells):
	        # Do a breadth-first traversal of the cells which this
		# new formula depends on
		L = value.cells
		while len(L):
		    if (yp,xp) in L: 
			raise Error, ("Circular reference created by "
				      "formula:" +repr(value) + " at "
				      + key)
		    # Add the dependencies of this cell to L, and remove L
		    c = self[ L[0] ]
		    if isinstance(c, Formula): L=L + c.cells
		    L = L[1:]

	        self.__calc_cells_accurate = 0

	# If required, extend the data array for the new cell
	if len(self.data)<=yp: 
	    self.data = self.data + [None]*(yp-len(self.data) + 1)

	row = self.data[yp]
	if row is None:
	    self.data[yp] = [None] * (xp+1)
	elif len(row)<=xp: 
	    self.data[yp] = self.data[yp] + [None]*( xp - len(row) + 1 )

	# Set the cell to the new value
	row = self.data[yp]
	self.data[yp][xp] = value
	
    def __getitem__(self, key):
	"Get a cell's value"
	if type(key) == types.TupleType:
	    yp, xp = key			# Unpack the tuple
	elif type(key) == types.StringType:     
	    yp, xp = str2yx(key)
	else:
	    raise KeyError, "Unexpected key "+repr(key)

	if len(self.data)<=yp: value = None
	elif self.data[yp] is None or len(self.data[yp])<=xp:  value = None
	else: value = self.data[yp][xp]
	return value

    def __delitem__(self, key):
	"Clear a cell"
	if type(key) == types.TupleType:
	    yp, xp = key			# Unpack the tuple
	elif type(key) == types.StringType:     
	    yp, xp = str2yx(key)
	else:
	    raise KeyError, "Unexpected key "+repr(key)

	if len(self.data)<=yp: pass
	elif self.data[yp] is None or len(self.data[yp])<=xp:  pass
	else: 
	    self.data[yp][xp] = None
	    if self.dep.has_key( (yp,xp) ):
		del self.dep[ (yp,xp) ]

    def recalc(self):
	"Recalculate all formulas in the spreadsheet"
	if not self.__calc_cells_accurate:
	    # We need to compute a topological sort of formula cells,
	    # based on the dependency graph.
	    # This will loop forever if there's a cycle, but that
	    # shouldn't matter now, because __setitem__ won't let you
	    # create cycles.
	    L=[]			# Topologically sorted list of coords
	    output={}			# Keep track of cells output so far

	    # Loop until all the cells have been output
	    while len(output) < len(self.dep):
		# We loop over all the cells
		for k in self.dep.keys():
		    # If the cell has already been output, skip it
		    if output.has_key(k):
                        continue  
		    # Count the number of cells on which this cell
		    #depends, and that have not been output yet,
		    count = 0
		    for cell in self.dep[k]:
			if (self.dep.has_key(cell) and 
			    (not output.has_key(cell))):
			    count = count + 1
		    if count==0: 
			L.append(k) ; output[k] = None
	    self.__calc_cells_accurate = 1
	    self.__calc_cells  = L

	# Loop over all the cells holding Formula instance, and
	# compute new values for them
        from math import sin, cos
	for coord in self.__calc_cells:
	    formula = self[ coord ]
	    try: 
		value = eval(formula.eval_str)
	    except:
		raise Error, ("calculation raised exception", formula.eval_str)

	    if isinstance(value, CELL):
		formula.value = value.value
	    else:
		formula.value = value

    # Ensure that spreadsheets can be pickled 
    # (XXX is this safe?)
    def __getstate__(self):
	return self.data, self.dep
    
    def __setstate__(self, state):
	self.data, self.dep = state
	self.__calc_cells_accurate = 0
	self.restr_env = SpreadsheetRExec(self)

if __name__=='__main__':
	
	S = Spreadsheet()
	S['A1'] = Formula('cos(A2) * 22')
	S['A2'] = Formula('A3')
	S['A3'] = Formula('1')

	S.recalc()
	print S['A1'].value

	S['A3'] = 77
	S.recalc()
	print S['A1'].value
	
