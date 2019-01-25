try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

class point:
    x = None
    y = None

    @classmethod
    def from_c(cls, c_obj):
        self = cls() 
        self.x = c_obj.x 
        self.y = c_obj.y 

        return self 


class bbox:
    x = None
    y = None 
    width = None 
    height = None

    @classmethod
    def from_c(cls, c_obj):
        self = cls() 
        self.x = c_obj.ulx
        self.y = c_obj.uly
        self.width = c_obj.width
        self.height = c_obj.height

        return self 

    def center(self):
        center = point()
        center.x = self.x + (self.width / 2)
        center.y = self.y + (self.height / 2)

        return center
