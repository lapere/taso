#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import Arc
import pickle
from kaari import *
from MenuFrame import MenuFrame


class FontEditor(Frame):
    def __init__(self, master, letter = None, tag=None):
        Frame.__init__(self, master)
        self.mb = MenuFrame(self)
        self.mb.addCommand("Tiedosto", self.save, "Tallenna")
        self.mb.addCommand("Tiedosto", self.quit, "Poistu")
        self.mb.addCommand("Muokkaa", self.delall, "Poista kaikki viivat")
        self.mb.pack(fill=X)
        self.master = master
        self.fat = False
        self.startx = 0
        self.starty = 0
        self.currx = 0
        self.curry = 0
        self.arc = []
        self.hint = StringVar(self)
        self.letter_name = StringVar(self)
        self.hint.set("Anna alkupiste")

        self.canvas = Canvas(self, height=160*3, width=150*3, bg="white")
        delete = Button(self, text="poista", command = self._del)
        arc_button = Button(self, text="kaari", command = self.do_arc)
        fat = Button(self, text="näytä", command = self.do_fat)
        hintbox = Label(self, textvariable=self.hint, font=("Fixed","18"))
        letter_name_box = Entry(self, textvariable=self.letter_name)
        self.org_cursor = self.canvas["cursor"]

        self.canvas.pack(expand=True, fill=BOTH)
        delete.pack(side=LEFT)
        arc_button.pack(side=LEFT)
        fat.pack(side=LEFT)
        letter_name_box.pack(side=LEFT)
        hintbox.pack(side=LEFT)
        
        for y in range(0,160*3,10*3):
            for x in range(0,150*3,10*3):

                #bigboxit
                self.canvas.create_rectangle(x+1,y+1, x+10*3-1,y+10*3-1,
                                              outline="black", fill="white", width=1, tags="tag")

                #valkoiset väliboxit kaarien päiden snapille
                self.canvas.create_rectangle(x-3+15, y-3, x+3+15, y+3,
                                              outline="", fill="white", width=2, tags="tag")
                self.canvas.create_rectangle(x-3, y-3+15, x+3, y+3+15,
                                              outline="", fill="white", width=2, tags="tag")
                
                self.canvas.tag_bind("tag", "<Enter>", self.enter)
                self.canvas.tag_bind("tag", "<Leave>", self.leave)

        

        self.canvas.bind("<Button-1>", self.rubber_start)
        self.canvas.bind("<Button-3>", self.rubber_stop)

        self.letters = pickle.load(open('save.p'))
	rl = []
	for l in self.letters:
		if type(l) != str:
			rl.append(l)
		if len(l) != 1:
			rl.append(l)
	for l in rl:
		self.letters.pop(l)
        self.do_letter_menus(self.letters)
        
        
    def do_letter_menus(self, letters):
        for letter in letters:
            if letter.islower():
                self.mb.addCommand("Pienet", lambda l=letter: self.do(l), letter)
            elif letter.isupper():
                self.mb.addCommand("Isot", lambda l=letter: self.do(l), letter)
            elif letter.isdigit():
                self.mb.addCommand("Numerot", lambda l=letter: self.do(l), letter)
            else:
                self.mb.addCommand("Muut", lambda l=letter: self.do(l), letter)

    def cmd_debug(self, letter):
        print 
        print letter + "*"*(80-len(letter)) 
        for l in self.letters[letter]:
            print l
        print "*"*80 
        print

    def do(self, letter):
        self.letter_name.set(letter)
        self.hint.set("Viivoja: %d" % len(self.letters[letter]))
        self.cmd_debug(letter)
        for line in self.letters[letter]:
            if type(line) == tuple:
                arg = []
                if len(line) == 3:
                    line = kaari(line[0], line[1], line[2])
                for point in line:
                    x = point[0] + 1.5
                    y = (13.5 - point[1])
                    arg.append(x)
                    arg.append(y)
                tag = self.canvas.create_line(arg, width="1m", capstyle="round", tags="l")
            else:
                tag = self.canvas.create_line(line, width="1m", capstyle="round", tags="l")
            self.canvas.tag_bind(tag, "<Enter>", self.enterl)
            self.canvas.tag_bind(tag, "<Leave>", self.leavel)
            self.canvas.scale(tag, 0, 0, 30, 30)
                
    def delall(self):
        self.canvas.delete("l")
        
    def save(self, event=None):
        self.canvas.delete("rub")
        name = self.letter_name.get()
        if name == "":
            self.hint.set("Mikä kirjain ?")
            return
        
        if not self.letters.has_key(name):
            self.do_letter_menus([name])

        self.canvas.scale("l", 0, 0, 1.0 / 30, 1.0 / 30)

        lst = []
        
        for tag in self.canvas.find_withtag("l"):
            coords = self.canvas.coords(tag)
            lst.append(coords)
        
        self.letters[name] = lst
        fd = open('save.p','w')
        pickle.dump(self.letters, fd)
        fd.close()
        self.canvas.scale("l", 0, 0, 30, 30)
        
        
    def delete_item(self, event):
        if self.canvas.type(CURRENT) != "rectangle":
            self.canvas.delete(CURRENT)
            
    def _del(self):
        self.rubber_stop(None)
        self.canvas["cursor"] = "pirate"
        self.canvas.bind("<Button-1>", self.delete_item)


    def draw_arc(self, event):
        if len(self.arc) <= 3:
            x, y = self.get_center()
            self.arc.append((x, y))
            if len(self.arc) == 2:
                self.canvas.bind("<Motion>", self.rubber)
            if len(self.arc) == 3:
                tag = Arc._arc(self.canvas, startp=self.arc[0], center=self.arc[1], endp=self.arc[2])
                self.canvas.tag_bind(tag, "<Enter>", self.enterl)
                self.canvas.tag_bind(tag, "<Leave>", self.leavel)
                self.canvas.addtag_withtag("l", tag)
                self.arc = []
                self.rubber_stop(None)
            
    def do_arc(self):
        self.arc = []
        self.canvas.bind("<Button-1>", self.draw_arc)
        

    def do_fat(self):
        if self.fat:
            self.canvas.itemconfigure("l", width=5)
            self.fat = False
        else:
            self.canvas.itemconfigure("l", width=30, capstyle="round")
            self.fat = True  

    def get_center(self):
        if len(self.canvas.coords(CURRENT)) > 4:
            return  self.currx,  self.curry
        else:
            x = (self.canvas.coords(CURRENT)[0] + self.canvas.coords(CURRENT)[2]) / 2
            y = (self.canvas.coords(CURRENT)[1] + self.canvas.coords(CURRENT)[3]) / 2
            return x, y

    def enter(self, event):
        self.canvas.itemconfigure(CURRENT, fill="red")
        self.currx, self.curry = self.get_center()

    def enterl(self, event):
        self.canvas.itemconfigure(CURRENT, fill="red")
        self.currx = event.x
        self.curry = event.y

    def leave(self, event):
        self.canvas.itemconfigure(CURRENT, fill="white")

    def leavel(self, event):
        self.canvas.itemconfigure(CURRENT, fill="black")
        
    def rubber(self, event):
        
        self.hint.set("Anna seuraava piste")

        if self.canvas.type(CURRENT) == "line":
            self.currx = event.x
            self.curry = event.y
        

        if len(self.arc) == 2:
            self.canvas.delete("rub")
            i = Arc._arc(self.canvas, startp=self.arc[0], center=self.arc[1],
                     endp=(self.currx, self.curry))
            self.canvas.addtag_withtag("rub", i)
        else:
            if self.currx > self.startx:
                x = self.currx - 2
            elif self.currx < self.startx:
                x = self.currx + 2
            else:
                x = self.currx 

            if self.curry > self.starty:
                y = self.curry - 2
            elif self.curry < self.starty:
                y = self.curry + 2
            else:
                y = self.curry
            self.canvas.delete("rub")
            self.canvas.create_line(self.startx, self.starty, x, y, width=1, tags="rub")

        #self.canvas.tag_lower("rub", "l")
        


    def rubber_next(self, event):
        if self.canvas.type(CURRENT) == "line":
            self.currx = event.x
            self.curry = event.y
        tag = self.canvas.create_line(self.startx, self.starty, self.currx, self.curry, width=5, tags="l")
        self.canvas.tag_bind(tag, "<Enter>", self.enterl)
        self.canvas.tag_bind(tag, "<Leave>", self.leavel)
        if self.canvas.type(CURRENT) == "line":
            self.startx = self.currx
            self.starty = self.curry
        else:
            self.startx,self.starty = self.get_center()
        
    def rubber_start(self, event):
        #snap on line or snap on box middlepoint
        if self.canvas.type(CURRENT) == "line":
            self.startx = event.x
            self.starty = event.y
        else:
            self.startx, self.starty = self.get_center()
            
        self.canvas.bind("<Button-1>", self.rubber_next)
        self.canvas.bind("<Motion>", self.rubber)
        
    def rubber_stop(self, event):
        self.canvas.bind("<Button-1>", self.rubber_start)
        self.canvas.unbind("<Motion>")
        self.canvas.delete("rub")
        self.arc = []
        self.canvas["cursor"] = self.org_cursor
        
   
if __name__ == '__main__':
    root = Tk()
    g = FontEditor(root)
    g.pack()
    #self.canvas.config(scrollregion=self.canvas.bbox("all"))
    root.mainloop()

