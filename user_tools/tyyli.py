# -*- coding: utf-8 -*-
from tkSimpleDialog import askfloat as __askfloat
from tkColorChooser import askcolor as __askcolor
from cad_kernel import *
import  current
canvas = current.canvas

def viivan_paksuus():
    """viivan paksuus pikseleinä"""
    w = __askfloat("Muuta viivan leveys", "viivan leveys pikseleinä")
    current.line_style["width"] = int(w)
    


def viivan_color():
    """viivan paksuus pikseleinä"""
    c = __askcolor()[0]
    c = "#%02x%02x%02x" % c
    current.line_style["fill"] = c
