#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
from code import *
import re
import draw

class PiPo:

    current = None
        
    def __init__(self, master=None):
        from cad_canvas import cad_canvas
        PiPo.current = self    
        self.canvas = None
        self.entry = None
    	self.ic = InteractiveConsole()
        self.item = None
        self.grid = (10,10)
        self.pnts_seq = []
        self.commands = []
        elements = dict(element0=set([]),element1=set([]))
        self.selection = None
        self.points = dict()
        self.drawmode = False

    	self.canvas = cad_canvas(root, bg="white", width=800, height=600,
                                 closeenough=5.0)
        self.canvas.items.ic = self.ic

    	self.entry = Text(root, bg="white", bd=1, height=1, relief=FLAT, font=("Fixed", "14", "bold"))

    	self.canvas.pack(expand=1, fill=BOTH)
    	self.entry.pack(fill=X)


    	cmd = compile_command("from draw import *")
    	self.ic.runcode(cmd)
    	self.bindings()
	
    def handle_grid(self, x, y):
        _x = x - self.grid[0] / 2.0
        _y = y - self.grid[1] / 2.0

        _x = divmod(_x, self.grid[0])[0] * self.grid[0] 
        _y = divmod(_y, self.grid[1])[0] * self.grid[1] 

        return int(_x + self.grid[0]), int(_y + self.grid[1])
        

    def finish_item(self, ):
        """
        tag_1, tag_2 = draw.get_tags(self.item)

        if self.points.has_key(tag_1):
            self.points[tag_1].append(self.item)
        else:
            self.points[tag_1] = [self.item]

        if self.points.has_key(tag_2):
            self.points[tag_2].append(self.item)
        else:
            self.points[tag_2] = [self.item]
        """
        self.item = None
        
     
        
    def execute_cmd(self, ):
        cmd = compile_command(self.entry.get("1.0", END))
        self.ic.runcode(cmd)

    def mouse_press_text(self, event, p):
        self.roll_tag(p)
        self.pnts_seq = list(self.entry.tag_names()[0:-1])
        self.pnts_seq.reverse()
        self.select_tag(p)

    def p(self, s):
        return "1." + str(s) 
        
    def roll_tag(self, p):
        self.entry.tag_raise("sel")
        self.entry.tag_config(self.entry.tag_names()[-2], foreground="black")
        self.entry.tag_lower(self.entry.tag_names()[-2])

        self.entry.tag_raise(p)
        self.entry.tag_raise("sel")
        self.entry.tag_config(p, foreground="red")

    def select_tag(self, p=None):
        if not p:
            p = self.entry.tag_names()[-2]
        r = self.entry.tag_ranges(p)
        c = r[0].split('.')[1]
        index1 = "1."+ str(int(c) + 1)

        c = r[1].split('.')[1]
        index2 = "1."+ str(int(c) - 1)
        self.entry.tag_add(SEL, index1, index2)
        self.entry.mark_set(INSERT, index1)


    def find_tuples(self):

        s = self.entry.get("1.0", END)
        self.pnts_seq = []
        
        for tag in self.entry.tag_names():
            self.entry.tag_delete(tag)
        
        p_name = re.finditer('\w+(?==\([\w ]*\,[ \w]*\))', s)
        p_value = re.finditer('(?<=)\([\w ]*\,[ \w]*\)', s)

        for m in zip(p_name, p_value):
            s = m[0].group()
            x, y = self.p(m[1].span()[0]), self.p(m[1].span()[1])
            self.entry.tag_add(s, x, y)
     
            def h(event, s=s):
                return self.mouse_press_text(event, s)

            self.entry.tag_bind(s, "<ButtonRelease-1>", h)
            self.pnts_seq.append(s)

        if self.pnts_seq:
            self.roll_tag(self.pnts_seq[0])
        #print self.entry.tag_names()

    def find_lists(self):

        s = current.entry.get("1.0", END)
        
        for tag in current.entry.tag_names():
            current.entry.tag_delete(tag)
        
        p_value = re.finditer('\[[\w,]+\]', s)

        for i, m in enumerate(p_value):
            s = "element" + str(i)
            x, y = p(m.span()[0]), p(m.span()[1])
            current.entry.tag_add(s, x, y)
     
            def h(self, event, s=s):
                return mouse_press_text(self, event, s)

            current.entry.tag_bind(s, "<Button-1>", h)

   
    def select_next_tuple(self):
        
        #print self.entry.tag_names(), self.pnts_seq
        if len(self.pnts_seq) > 1:
            if self.entry.tag_names()[-3] == self.pnts_seq[0]:
                self.finish_item()
                try:
                    
                    self.range_copy("endp", "startp")
                except:
                    print "can't range_copy:", self.entry.tag_names() 
                    pass
                #range_copy(self.pnts_seq[-1], self.pnts_seq[0])
                self.roll_tag(self.entry.tag_names()[-3])
            self.roll_tag(self.entry.tag_names()[-3])
        self.select_tag()

    def range_copy(self, pos1, pos2):
        
        ran1 = self.entry.tag_ranges(pos1)
        ran2 = self.entry.tag_ranges(pos2)

        s = self.entry.get(ran1[0], ran1[1])

        self.entry.delete(ran2[0], ran2[1])
        self.entry.insert(ran2[0], str(s), pos2)   

    def range_replace(position, s):
    
        ran1 = current.entry.tag_ranges(position)

        current.entry.delete(ran1[0], ran1[1])
        current.entry.insert(ran1[0], str(s), position)       

    def handle_hit(self, ):
        line = self.entry.get("1.0", INSERT)
        l = len(line)
        m = map(lambda x: x[:l], draw.fun_syntax.keys())

        print line,m
        if line in m:
            for hit in draw.fun_syntax.keys():
                if hit[:len(line)] == line:
                    self.entry.delete(INSERT,END)
                    self.entry.insert(INSERT, draw.fun_syntax[hit][l:], SEL)
                    self.drawmode = hit
                    return
        else:
            self.drawmode = False

        
    def entry_type_words(self, event):

        ks = event.keysym 
        if ks == "Up":
            self.entry.delete("1.0", END)
            if self.commands:
                self.entry.delete("1.0", END)
                self.entry.insert("1.0", self.commands.pop())
                self.find_tuples()
                self.select_next_tuple()
                self.drawmode = True
                
        elif ks != "BackSpace":
            if ks == "Right":
                self.entry.tag_remove(SEL, "1.0", END)
                self.select_next_tuple()
                #self.select_tag()
            elif ks == "Return":
                c = self.entry.get("1.0", END)
                c = c.replace('\n', '')
                self.entry.delete("1.0", END)
                self.entry.insert("1.0", c)
                self.entry_enter(event)
        
            else:
                
                self.handle_hit()
                self.drawmode = True
                self.find_tuples()

      
    def entry_enter(self, event):
    
        #if self.item:
        #    self.canvas.delete(self.item)
    
        self.execute_cmd()
        #self.entry.mark_set(INSERT, END)
        #self.select_next_tuple() 
        c = self.entry.get("1.0", END)
        c = c.replace("\n", '')
        self.commands.append(c)
               
	self.entry.delete("1.0",END)
        self.drawmode = False

    def entry_leave(self, event):
        pass
        #self.entry.tag_remove(SEL, "1.0", END)


    # Mouse Canvas event handlers    

    def mouse_selecet_elements(event):

        e_tag = current.entry.tag_names()[-2]
        _id = current.canvas.find_withtag(CURRENT)[0]#current.selection)[0]
        elements[e_tag].add(_id)
        s = str(list(elements[e_tag]))
        range_replace(e_tag, s)

    def mouse_press_canvas(self, event):
        
        if self.item:
            self.canvas.delete(self.item)
        self.execute_cmd()
        self.select_next_tuple()
        
        #def mouse_press_canvas_point(self, event):
        self.item = None


    def mouse3_press_canvas(self, event):
        
        if self.commands and not self.drawmode:
            self.entry.insert("0.0", self.commands.pop())
            self.find_tuples()
            self.select_next_tuple()
            self.drawmode = True
        elif self.drawmode:
            if self.item:
                self.canvas.delete(self.item)
                self.item = None
            c = self.entry.get("1.0", END)
            c = c.replace("\n", '')
            self.commands.append(c)
            self.entry.delete("1.0",END)
            self.drawmode = False

    def mouse_move_canvas(self, event):
        
       if self.drawmode:
            cur_p = self.entry.tag_names()[-2]
            ran = self.entry.tag_ranges(cur_p)

            if cur_p != "density":
                s = self.handle_grid(event.x, event.y)
            else:
                s = event.x, event.y

            self.entry.delete(ran[0], ran[1])
            self.entry.insert(ran[0], str(s), cur_p)
            
            if self.item: 
                self.item.move(s)
                self.canvas.repaint()
            else:
                self.execute_cmd()

    def bindings(self):
        
        #self.entry.bind("<KeyPress-Return>", self.test_enter)
        self.entry.bind("<KeyRelease>", self.entry_type_words)
        self.entry.bind("<Leave>", self.entry_leave)
        #self.entry.bind("<Button-1>", mouse_press_entry)
        #self.entry.bind("<ButtonRelease-1>", mouse_release_entry)
        #self.entry.bind("<B1-Motion>", mouse_drag_entry)

        self.canvas.bind("<Button-1>", self.mouse_press_canvas)
        self.canvas.bind("<ButtonRelease-3>", self.mouse3_press_canvas)
        self.canvas.bind("<Motion>", self.mouse_move_canvas)
     
if __name__ == '__main__':
    root = Tk()
    x,y = root.maxsize()
    root.geometry("%dx%d" % (x-400, y-400))
    a = PiPo()
    draw.current = a
    root.mainloop()

