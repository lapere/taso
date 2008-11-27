# -*- coding: utf-8 -*-
# http://www.autodesk.com/techpubs/autocad/acadr14/dxf/
from Tkinter import *
from math import *
from helpers import *
import tkFont
import copy
from font_SFS-ISO_3098 import Arc

class DFACE:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		DFACE.cnt += 1
class DSOLID:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		DSOLID.cnt += 1
		
class ACAD_PROXY_ENTITY:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		ACAD_PROXY_ENTITY.cnt += 1
			
class ARC:
	cnt = 0
	def __init__(self, canvas, e, master=None):

            x = e.data["10"]
            y = e.data["20"]
            
            r = e.data["40"]
            start = e.data["50"]
            end = e.data["51"]
            
            if start < end:
                angle = end - start
            else:
                angle = 360 + end - start

            start_x = x + cos(radians(angle)) * r
            start_y = y + sin(radians(angle)) * r
            
            self.tag = Arc._arc(canvas.c, center=(x, y),
                                          radius=r,
                                          astart = start,
                                          angle = angle)
            
	    ARC.cnt += 1
class ATTDEF:
	cnt = 0
	def __init__(self, canvas, e, master=None):
                self.tag = None
		ATTDEF.cnt += 1
		
class ATTRIB:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		ATTRIB.cnt += 1
class BODY:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		BODY.cnt += 1
		
class CIRCLE:
	cnt = 0
	def __init__(self, canvas, e, master=None):

	    x = e.data["10"]
            y = e.data["20"]
            r = e.data["40"]

            #box_x0 = x - r
            #box_y0 = canvas.h - y - r
            #box_x1 = x + r
            #box_y1 = canvas.h - y + r

            box_x0 = x + r
            box_y0 = y - r
            box_x1 = x - r
            box_y1 = y + r
            
            self.tag = canvas.c.create_oval(box_x0, box_y0, box_x1, box_y1) 
	    CIRCLE.cnt += 1       
class DIMENSION:
	cnt = 0
	def __init__(self, canvas, e, master=None):
	    DIMENSION.cnt += 1
class ELLIPSE:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		ELLIPSE.cnt += 1
class HATCH:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		HATCH.cnt += 1
class IMAGE:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		IMAGE.cnt += 1
class INSERT:
    cnt = 0
    def __init__(self, canvas, e, master=None):
        self.e = e
        self.b_name = e.data["2"]
        self.tag = self.b_name
        block = canvas.blocks[self.b_name]

        self.x_off = e.data["10"]
        self.y_off = e.data["20"]

        if e.data.has_key('41'):
            x_scale = e.data['41']

        if e.data.has_key('42'):
            y_scale = e.data['42']

        if e.data.has_key("50"):
            self.rot = e.data["50"]
        else:
            self.rot = 0

        #if master:
        #    self.x_off = self.x_off + master.x_off
        #    self.y_off = self.y_off + master.y_off
        #    self.rot = self.rot + master.rot
                
        for entity in block.entities:
            print canvas.c.find_withtag(self.tag)
            f = funit[entity.type]
            i = f(canvas, entity, self)
            if i.tag:
                canvas.c.addtag_withtag(self.tag, i.tag)

        #rotate(canvas.c, self.tag, self.rot)
        canvas.c.move(self.tag, self.x_off, self.y_off)
            
	INSERT.cnt += 1
            
    def mouse_push(self, event):
        print "INSERT", self.tag,
        for kw in self.e.data:
            print kw, "=", self.e.data[kw]

class LEADER:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		LEADER.cnt += 1
class LINE:
    cnt = 0
    def __init__(self, canvas, e, master=None):
        self.e = e
        
        x0 = e.data["10"]
        y0 = e.data["20"]
        x1 = e.data["11"]
        y1 = e.data["21"]

        
        #y0 = canvas.h - y0
        #y1 = canvas.h - y1

        LINE.cnt += 1

        self.tag = canvas.c.create_line(x0, y0, x1, y1)
        
        canvas.c.tag_bind(self.tag, "<Button-1>", self.mouse_push)
        

    def mouse_push(self, event):
        print "LINE", self.tag
        print self.e.data
	
	
class LWPOLYLINE:
    cnt = 0
    def __init__(self, canvas, e, master=None):
        self.e = e

        arg = []
        
        for x,y in zip(e.data["10"], e.data["20"]):
            arg.append(x)
            arg.append(y)
            
        self.tag = canvas.c.create_line(arg)
        
        canvas.c.tag_bind(self.tag, "<Button-1>", self.mouse_push)
        
	LWPOLYLINE.cnt += 1

    def mouse_push(self, event):
        print "LWPOLYLINE", self.tag


class MLINE:
	cnt = 0
	def __init__(self, canvas, e, master=None):
            MLINE.cnt += 1
class MTEXT:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		MTEXT.cnt += 1
class OLEFRAME:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		OLEFRAME.cnt += 1
class OLE2FRAME:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		OLE2FRAME.cnt += 1
		
class POINT:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		POINT.cnt += 1
class POLYLINE:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		POLYLINE.cnt += 1
class RAY:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		RAY.cnt += 1
class REGION:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		REGION.cnt += 1
class SEQEND:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		SEQEND.cnt += 1
class SHAPE:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		SHAPE.cnt += 1
class SOLID:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		SOLID.cnt += 1
class SPLINE:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		SPLINE.cnt += 1
class TEXT:
	cnt = 0
	def __init__(self, canvas, e, master=None):

            # core fields
            h = int(e.data["40"])
            x = e.data["10"]
            y = e.data["20"] + (h / 2)
            txt = e.data["1"]
            
            # optional fields
            if e.data.has_key("72"):
                h_just = ("w", "", "e", "aligned", "middle", "fit")
                h_just = h_just[e.data["72"]]
            else:
                h_just = "w"
                
            if e.data.has_key("73"):
                v_just = ("s","s", "", "n")
                v_just = v_just[e.data["73"]]
            else:
                v_just = ""

            if h_just == "aligned":
                print "alig"
                return
            if h_just == "middle":
                #x2 = e.data["11"]
                #y2 = e.data["21"]
                #h_scale =  (y2 * scale - y) / (len(txt) * h) 
                #h *= h_scale 
                #h = int(h)
                h_just = ""
                return
            if h_just == "fit":
                print "fit"
                return

            if v_just+h_just == "":
                just = "center"
            else:
                just = v_just+h_just

            if e.data.has_key("41"):
                h /= e.data["41"]
                h = int(h)
            
            font = ("Helvetica", str(h))
            self.tag = canvas.c.create_text(x, y, font=font,
                                            text = txt,
                                            tags = str(h),
                                            anchor = just)
            canvas.font = h
	    TEXT.cnt += 1
class TOLERANCE:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		TOLERANCE.cnt += 1
class TRACE:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		TRACE.cnt += 1
class VERTEX:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		VERTEX.cnt += 1
class VIEWPORT:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		VIEWPORT.cnt += 1
class XLINE:
	cnt = 0
	def __init__(self, canvas, e, master=None):
		XLINE.cnt += 1
   
funit = dict({"3DFACE":DFACE,
                "3DSOLID":DSOLID,
                "ACAD_PROXY_ENTITY":ACAD_PROXY_ENTITY,
                "ARC":ARC,
                "ATTDEF":ATTDEF,
                "ATTRIB":ATTRIB,
                "BODY":BODY,
                "CIRCLE":CIRCLE,
                "DIMENSION":DIMENSION,
                "ELLIPSE":ELLIPSE,
                "HATCH":HATCH,
                "IMAGE":IMAGE,
                "INSERT":INSERT,
                "LEADER":LEADER,
                "LINE":LINE,
                "LWPOLYLINE":LWPOLYLINE,
                "MLINE":MLINE,
                "MTEXT":MTEXT,
                "OLEFRAME":OLEFRAME,
                "OLE2FRAME":OLE2FRAME,
                "POINT":POINT,
                "POLYLINE":POLYLINE,
                "RAY":RAY,
                "REGION":REGION,
                "SEQEND":SEQEND,
                "SHAPE":SHAPE,
                "SOLID":SOLID,
                "SPLINE":SPLINE,
                "TEXT":TEXT,
                "TOLERANCE":TOLERANCE,
                "TRACE":TRACE,
                "VERTEX":VERTEX,
                "VIEWPORT":VIEWPORT,
                "XLINE":XLINE})


if __name__ == '__main__':
    import dxf
