# -*- coding: utf-8 -*-
import current

def point():
    print "valitse siirrettävä piste"
    current.canvas.getPoint()
    id = current.canvas.current
    p = current.canvas.visuals[id]
    print p.tag
    print "valitse mihin siirretään"
    new_point = current.canvas.getPoint()
    p.new_formula(str(new_point))
    

