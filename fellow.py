from UserDict  import *

class Fellow(IterableUserDict):

    def __init__(self):
        IterableUserDict.__init__(self)
        self.ends = dict()
        
    def new_fellow(self, fellow, other_end=None):
        self.update({fellow.tag : fellow})
        
        if other_end:
            self.ends.update({fellow.tag : other_end})

    def get_endpoint(self, tag):
        return self.ends[tag]

    def set_endpoint(self, tag, endpoint):
        self.ends[tag] = endpoint
