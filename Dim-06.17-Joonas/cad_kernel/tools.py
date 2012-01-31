from math import *

def lev():
    for g in globals():
        if g[0] == "c":
            print g
    return 100 

def test():
    print "moi"
    return 10
    
