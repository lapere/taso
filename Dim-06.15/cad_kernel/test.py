from db import ItemDB
from item import *
d = ItemDB()

last = Item(d, "X", "100")
for i in range(1000):
    last = Item(d, "X", "%s + 1" % last.tag)    

print "old", d["X1"].value

d["X1"].new_formula("200")
d.recalc()
print "new", d["X998"].value
