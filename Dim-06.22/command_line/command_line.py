#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
from code import *
import re
from types import *
import sys

class CommandLine(Text):
        
    def __init__(self, root, canvas, ic):
        Text.__init__(self, root, bg="white", bd=1,
                      height=5, relief=FLAT, font=("Fixed", "14", "bold"))

        self.cmd = ""
        self.commands = []
        self.selection = None
        self.points = dict()
        self.hit_targets = dict()
        self.tag_list = []
    	self.canvas = canvas
    	self.ic = ic
        #sys.stdout = self
        
    	self.canvas.current_item = None
    	
    	
    	self.bindings()
	self.parse_module_names()

    def write(self, data):
        self.insert(INSERT, data)
        
    def execute_cmd(self):
        return self.ic.runcode(self.cmd)

    def finish_item(self):
        self.cmd = self.get_last_line()
        print self.cmd
        self.execute_cmd()
        self.put_cmd(self.cmd)
        self.find_tuples()
        self.range_copy("endp", "startp")
        self.select_tag("endp")

    def mouse_press_text(self, event, p):
        self.select_tag(p)

    def p(self, s):
        return self.get_current_line_nro() + "." + str(s) 

    """    
    def roll_tag(self, p):
        self.tag_raise("sel")
        self.tag_config(self.tag_names()[-2], foreground="black")
        self.tag_lower(self.tag_names()[-2])

        self.tag_raise(p)
        self.tag_raise("sel")
        self.tag_config(p, foreground="red")
    """
    def select_tag(self, p=None):

        for tag in self.tag_names():
            self.tag_config(tag, foreground="black")
        self.tag_config(p, foreground="red")
        
        r = self.tag_ranges(p)

        c = r[0].split('.')[1]
        n = r[0].split('.')[0]
        index1 = n + "." + str(int(c) + 1)

        c = r[1].split('.')[1]
        n = r[1].split('.')[0]
        index2 = n + "." + str(int(c) - 1)

        self.tag_add(SEL, index1, index2)
        self.mark_set(INSERT, index1)

    def find_tuples(self):
        s = self.get_current_line()
        
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
            self.tag_list.append(s)
   
    def select_next_tuple(self):
        
        if len(self.tag_list) > 1:
            if self.tag_list[0] == "endp":
                #self.range_copy("endp", "startp")
                self.finish_item()
                return
            self.tag_list = [self.tag_list[-1]] + self.tag_list[:-1]
            self.select_tag(self.tag_list[0])

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
        c = self.get_current_line_nro()
        line = self.get(c+".0", INSERT)
        l = len(line)
        m = map(lambda x: x[:l], loc.keys())

        if line in m:
            for hit in loc.keys():                
                if hit[:len(line)] == line:
                    #print type(loc[hit]), callable(loc[hit]), hit,"=", loc[hit] 
                    self.delete(INSERT,END)
                    self.insert(INSERT, loc[hit][l:], SEL)
                    return True
        else:
            return False
        
    def get_last_line(self):
        line = self.index(END).split(".")[0]
        line = str(int(line) - 2)
        return self.get(line+".0", line+".end")

    def get_last_line_nro(self):
        line = self.index(END).split(".")[0]
        line = str(int(line) - 2)
        return line

    def get_current_line(self):
        line = self.index(INSERT).split(".")[0]
        return self.get(line+".0", line+".end")

    def get_current_line_nro(self):
        return self.index(INSERT).split(".")[0]
        
    def entry_type_words(self, event):
        if not event.keysym in ["BackSpace","Right", "Up", "Left", "Down"]:
            if self.handle_hit():
                self.find_tuples()
        
    def put_cmd(self, cmd):
        self.insert(END, cmd + "\n")
        self.mark_set(INSERT, self.get_last_line_nro() + ".0")
    
    def put_and_run(self, cmd):
        self.put_cmd(cmd)
        self.execute_cmd()

    def entry_enter(self, event):
        self.cmd = self.cmd + self.get_last_line()
        self.ret = self.execute_cmd()
         
        if not self.ret:
            self.cmd = ""
        else:
            pass
            #self['height'] = int(self['height']) + 1    
    
        
        #self.mark_set(INSERT, END)
        self.select_next_tuple() 
        #c = self.get("1.0", END)
        #c = c.replace("\n", '')
        #self.commands.append(c)
               
	#self.delete("1.0",END)
        #self.drawmode = False

    def entry_leave(self, event):
        pass
        #self.tag_remove(SEL, "1.0", END)


    # Mouse Canvas event handlers

    def mouse_press_canvas(self, event):        
        self.select_next_tuple()

    def mouse3_press_canvas(self, event):
        pass
    
    def mouse_move_canvas(self, event):
    
        cur_p = self.tag_list[0]
        ran = self.tag_ranges(cur_p)

        s = event.x, event.y

        self.delete(ran[0], ran[1])
        self.insert(ran[0], str(s), cur_p)
            
            
    def bindings(self):
        
        self.bind("<KeyRelease-Return>", self.entry_enter)
        self.bind("<KeyRelease>", self.entry_type_words)
        self.bind("<Leave>", self.entry_leave)
        
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

