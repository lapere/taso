       
class Level:

    cnt = 0

    def __init__(self, name, value):
        self.tag = name + str(Level.cnt)
        Level.cnt = Level.cnt + 1
        self.value = value
    
      
class _X(Level):

    def __init__(self, value):
        Level.__init__(self, "X", value)
        self.x = value
   
class _Y(Level):

    def __init__(self, value):
        Level.__init__(self, "Y", value)
        self.y = value
     
