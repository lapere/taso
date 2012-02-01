from Tkinter import *
import pickle


class iso3098_text:
    
    def __init__(self, master):
        self.letters = pickle.load(open('save.p'))
        
if __name__ == '__main__':
    root = Tk()
    c = Canvas(root, bg="white")
    i = iso3098_text(c)
    i = "AAA"
    c.pack()
    root.mainloop()
