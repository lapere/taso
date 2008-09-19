# http://www.autodesk.com/techpubs/autocad/acadr14/dxf/
from Tkinter import *
from math import *
import tkFont
import copy

class DFACE:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		DFACE.cnt += 1
class DSOLID:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		DSOLID.cnt += 1
		
class ACAD_PROXY_ENTITY:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		ACAD_PROXY_ENTITY.cnt += 1
			
class ARC:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):

            x = e.data["10"] * scale + x_off 
            y = e.data["20"] * scale + y_off
            
            r = e.data["40"] * scale
            start = e.data["50"]
            end = e.data["51"]
            
            if start < end:
                angle = end - start
            else:
                angle = 360 + end - start

            box_x0 = x - r
            box_y0 = canvas.h - y - r
            box_x1 = x + r
            box_y1 = canvas.h - y + r
            
            self.tag = canvas.c.create_arc(box_x0, box_y0, box_x1, box_y1, 
                                    extent=angle, start=start, 
                                    style="arc")
	    ARC.cnt += 1
class ATTDEF:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		ATTDEF.cnt += 1
		
class ATTRIB:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		ATTRIB.cnt += 1
class BODY:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		BODY.cnt += 1
		
class CIRCLE:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):

	    x = e.data["10"] * scale + x_off 
            y = e.data["20"] * scale + y_off
            
            r = e.data["40"] * scale 
            

            box_x0 = x - r
            box_y0 = canvas.h - y - r
            box_x1 = x + r
            box_y1 = canvas.h - y + r
            
            self.tag = canvas.c.create_oval(box_x0, box_y0, box_x1, box_y1) 
	    CIRCLE.cnt += 1       
class DIMENSION:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
	    DIMENSION.cnt += 1
class ELLIPSE:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		ELLIPSE.cnt += 1
class HATCH:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		HATCH.cnt += 1
class IMAGE:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		IMAGE.cnt += 1
class INSERT:
    cnt = 0
    def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
        self.e = e
        self.b_name = e.data["2"]
        block = canvas.blocks[self.b_name]

       

        if e.data.has_key("10"):
            x_off = e.data["10"] * scale
        else:
            x_off = 0
            
        if e.data.has_key("20"):
            y_off = e.data["20"] * scale
        else:
            y_off = 0

        
        if e.data.has_key('41'):
            scale = e.data['41'] * scale

        if not scale:
            scale = canvas.scale

        INSERT.cnt += 1
        
        for entity in block.entities:
            entity = copy.deepcopy(entity) #make a deep copy because there is no ref and otherwise our f(funit) not work
            f = funit[entity.type]
            if (entity.type != "INSERT") or True:
            #rotate if needed    
                if e.data.has_key("50"):
                    alfa = radians(float(e.data["50"]))
                
                    for pnt in 10,11,12:
                        x_pnt = str(pnt)
                        y_pnt = str(pnt+10)
                        if entity.data.has_key(x_pnt):
                            if type(entity.data[x_pnt]) != list:
                                x = entity.data[x_pnt]
                                y = entity.data[y_pnt]
                                entity.data[x_pnt] = x * cos(alfa) - y * sin(alfa)
                                entity.data[y_pnt] = x * sin(alfa) + y * cos(alfa)
                                
                            else:
                                #TODO ei toimi kierto 
                                pass
                    if entity.type == "ARC":
                        for a in "50","51":
                                entity.data[a] = entity.data[a] + degrees(alfa)
                
                i = f(canvas, entity, scale = scale, x_off = x_off, y_off = y_off)
                #if entity.type == "LINE":
                #    canvas.c.tag_bind(i.tag, "<Button-1>", self.mouse_push)
            else:
                i = f(canvas, entity)
                
                       
            self.tag = self.b_name
	    INSERT.cnt += 1
            
    def mouse_push(self, event):
        print "INSERT", self.tag,
        for kw in self.e.data:
            print kw, "=", self.e.data[kw]

class LEADER:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		LEADER.cnt += 1
class LINE:
    cnt = 0
    def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
        self.e = e
        
        x0 = e.data["10"] * scale + x_off
        y0 = e.data["20"] * scale + y_off
        x1 = e.data["11"] * scale + x_off
        y1 = e.data["21"] * scale + y_off

        
        y0 = canvas.h - y0
        y1 = canvas.h - y1

        LINE.cnt += 1

        self.tag = canvas.c.create_line(x0, y0, x1, y1)
        
        canvas.c.tag_bind(self.tag, "<Button-1>", self.mouse_push)
        

    def mouse_push(self, event):
        print "LINE", self.tag
	
	
class LWPOLYLINE:
    cnt = 0
    def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
        self.e = e

        arg = []
        
        for x,y in zip(e.data["10"], e.data["20"]):
            arg.append(x * scale + x_off)
            y = y * scale + y_off
            arg.append(canvas.h - y)
            

        self.tag = canvas.c.create_line(arg)
        
        canvas.c.tag_bind(self.tag, "<Button-1>", self.mouse_push)
        
	LWPOLYLINE.cnt += 1

    def mouse_push(self, event):
        print "LWPOLYLINE", self.tag


class MLINE:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
            MLINE.cnt += 1
class MTEXT:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		MTEXT.cnt += 1
class OLEFRAME:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		OLEFRAME.cnt += 1
class OLE2FRAME:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		OLE2FRAME.cnt += 1
		
class POINT:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		POINT.cnt += 1
class POLYLINE:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		POLYLINE.cnt += 1
class RAY:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		RAY.cnt += 1
class REGION:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		REGION.cnt += 1
class SEQEND:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		SEQEND.cnt += 1
class SHAPE:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		SHAPE.cnt += 1
class SOLID:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		SOLID.cnt += 1
class SPLINE:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		SPLINE.cnt += 1
class TEXT:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):

            # core fields
            h = int(e.data["40"] * scale)
            x = e.data["10"] * scale
            y = e.data["20"] * scale + (h / 2)
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
            y = canvas.h - y
            self.tag = canvas.c.create_text(x, y, font=font,
                                            text = txt,
                                            tags = str(h),
                                            anchor = just)
            canvas.font = h
	    TEXT.cnt += 1
class TOLERANCE:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		TOLERANCE.cnt += 1
class TRACE:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		TRACE.cnt += 1
class VERTEX:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		VERTEX.cnt += 1
class VIEWPORT:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
		VIEWPORT.cnt += 1
class XLINE:
	cnt = 0
	def __init__(self, canvas, e, scale = 1, x_off = 0, y_off = 0):
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
