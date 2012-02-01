#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
from code import *
import re
from types import *
#import draw

class CommandLine(Text):
        
    def __init__(self, root, canvas, ic):
        Text.__init__(self, root, bg="white", bd=1, height=3, relief=FLAT, font=("Fixed", "14", "bold"))
        
        self.pnts_seq = []
        self.commands = []
        self.selection = None
        self.points = dict()
        self.drawmode = False
        self.hit_targets = dict()
        
    	self.canvas = canvas
    	self.ic = ic

    	self.canvas.current_item = None
    	#cmd = compile_command("from default_tools.draw import *")
    	#self.ic.runcode(cmd)
    	self.bindings()
	self.parse_module_names()
    
    def finish_item(self, ):
        self.canvas.current_item = None        
        
    def execute_cmd(self, ):
        cmd = compile_command(self.get("1.0", END))
        self.ic.runcode(cmd)

    def mouse_press_text(self, event, p):
        self.roll_tag(p)
        self.pnts_seq = list(self.tag_names()[0:-1])
        self.pnts_seq.reverse()
        self.select_tag(p)

    def p(self, s):
        return "1." + str(s) 
        
    def roll_tag(self, p):
        self.tag_raise("sel")
        self.tag_config(self.tag_names()[-2], foreground="black")
        self.tag_lower(self.tag_names()[-2])

        self.tag_raise(p)
        self.tag_raise("sel")
        self.tag_config(p, foreground="red")

    def select_tag(self, p=None):
        try:
            if not p:
                p = self.tag_names()[-2]
            r = self.tag_ranges(p)
            c = r[0].split('.')[1]
            index1 = "1."+ str(int(c) + 1)

            c = r[1].split('.')[1]
            index2 = "1."+ str(int(c) - 1)
            self.tag_add(SEL, index1, index2)
            self.mark_set(INSERT, index1)
        except:
            pass


    def find_tuples(self):

        s = self.get("1.0", END)
        self.pnts_seq = []
        
        for tag in self.tag_names():
            self.tag_delete(tag)
        
        p_name = re.finditer('\w+(?==\([\w ]*\,[ \w]*\))', s)
        p_value = re.finditer('(?<=)\([\w ]*\,[ \w]*\)', s)

        for m in zip(p_name, p_value):
            s = m[0].group()
            x, y = self.p(m[1].span()[0]), self.p(m[1].span()[1])
            self.tag_add(s, x, y)
     
            def h(event, s=s):
                return self.mouse_press_text(event, s)

            self.tag_bind(s, "<ButtonRelease-1>", h)
            self.pnts_seq.append(s)

        if self.pnts_seq:
            self.roll_tag(self.pnts_seq[0])
        #print self.tag_names()

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
        
        #print self.tag_names(), self.pnts_seq
        if len(self.pnts_seq) > 1:
            if self.tag_names()[-3] == self.pnts_seq[0]:
                self.finish_item()
                try:
                    self.range_copy("endp", "startp")
                except:
                    print "can't range_copy:", self.tag_names() 
                    pass
                #range_copy(self.pnts_seq[-1], self.pnts_seq[0])
                self.roll_tag(self.tag_names()[-3])
            self.roll_tag(self.tag_names()[-3])
        self.select_tag()

    def range_copy(self, pos1, pos2):
        
        ran1 = self.tag_ranges(pos1)
        ran2 = self.tag_ranges(pos2)

        s = self.get(ran1[0], ran1[1])

        self.delete(ran2[0], ran2[1])
        self.insert(ran2[0], str(s), pos2)   

    def range_replace(position, s):
    
        ran1 = current.entry.tag_ranges(position)

        current.entry.delete(ran1[0], ran1[1])
        current.entry.insert(ran1[0], str(s), position)       

    def parse_module_names(self):
        print "parsw"
        loc = self.ic.locals
        for k in loc:
            if callable(loc[k]):
                self.hit_targets.update({k:loc[k]})
            elif type(loc[k]) == ModuleType:
                for mf in loc[k].__dict__:
                    if callable(loc[k].__dict__[mf]):
                        self.hit_targets.update({k+"."+mf:k+"."+str(loc[k].__dict__[mf].__doc__)})
            
    def handle_hit(self, ):
        loc = self.hit_targets
        line = self.get("1.0", INSERT)
        l = len(line)
        m = map(lambda x: x[:l], loc.keys())

        if line in m:
            for hit in loc.keys():                
                if hit[:len(line)] == line:
                    #print type(loc[hit]), callable(loc[hit]), hit,"=", loc[hit] 
                    self.delete(INSERT,END)
                    self.insert(INSERT, loc[hit][l:], SEL)
                    self.drawmode = hit
                    return
        else:
            self.drawmode = False

        
    def entry_type_words(self, event):

        ks = event.keysym 
        if ks == "Up":
            self.delete("1.0", END)
            if self.commands:
                self.delete("1.0", END)
                self.insert("1.0", self.commands.pop())
                self.find_tuples()
                self.select_next_tuple()
                self.drawmode = True
                
        elif ks != "BackSpace":
            if ks == "Right":
                self.tag_remove(SEL, "1.0", END)
                self.select_next_tuple()
                #self.select_tag()
            elif ks == "Return":
                c = self.get("1.0", END)
                c = c.replace('\n', '')
                self.delete("1.0", END)
                self.insert("1.0", c)
                self.entry_enter(event)
        
            else:
                
                self.handle_hit()
                self.drawmode = True
                self.find_tuples()

    def put_cmd(self, cmd):
        self.delete("1.0", END)
        self.insert("1.0", cmd)

    def put_and_run(self, cmd):
        self.put_cmd(cmd)
        self.execute_cmd()
        
    def entry_enter(self, event):
    
        if self.canvas.current_item:
            self.canvas.delete(self.canvas.current_item)
    
        self.execute_cmd()
        self.mark_set(INSERT, END)
        self.select_next_tuple() 
        c = self.get("1.0", END)
        c = c.replace("\n", '')
        self.commands.append(c)
               
	self.delete("1.0",END)
        self.drawmode = False

    def entry_leave(self, event):
        pass
        #self.tag_remove(SEL, "1.0", END)


    # Mouse Canvas event handlers

    def mouse_press_canvas(self, event):
        
        if self.canvas.current_item:
            self.canvas.delete(self.canvas.current_item)
        try:
            self.execute_cmd()
        except:
            pass
        #if self.canvas.current_item:
        self.select_next_tuple()
        self.canvas.current_item = None


    def mouse3_press_canvas(self, event):
        
        if self.commands and not self.drawmode:
            self.insert("0.0", self.commands.pop())
            self.find_tuples()
            self.select_next_tuple()
            self.drawmode = True
        elif self.drawmode:
            if self.canvas.current_item:
                self.canvas.delete(self.canvas.current_item)
                self.canvas.current_item = None
            c = self.get("1.0", END)
            c = c.replace("\n", '')
            self.commands.append(c)
            self.delete("1.0",END)
            self.drawmode = False

    def mouse_move_canvas(self, event):
        
       if self.drawmode:
            cur_p = self.tag_names()[-2]
            ran = self.tag_ranges(cur_p)

            s = event.x, event.y

            self.delete(ran[0], ran[1])
            self.insert(ran[0], str(s), cur_p)
            
            if self.canvas.current_item:
                self.canvas.delete(self.canvas.current_item)
            self.execute_cmd()

    def bindings(self):
        
        #self.bind("<KeyPress-Return>", self.test_enter)
        self.bind("<KeyRelease>", self.entry_type_words)
        self.bind("<Leave>", self.entry_leave)
        #self.bind("<Button-1>", mouse_press_entry)
        #self.bind("<ButtonRelease-1>", mouse_release_entry)
        #self.bind("<B1-Motion>", mouse_drag_entry)

        self.canvas.bind("<Button-1>", self.mouse_press_canvas)
        self.canvas.bind("<ButtonRelease-3>", self.mouse3_press_canvas)
        self.canvas.bind("<Motion>", self.mouse_move_canvas)
     
if __name__ == '__main__':
    root = Tk()
    x,y = root.maxsize()
    root.geometry("%dx%d" % (x-400, y-400))
    ic = InteractiveConsole()
    a = CommandLine(root, None, ic)
    root.mainloop()

