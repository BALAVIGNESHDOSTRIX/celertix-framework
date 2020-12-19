class Char:
    def __init__(self, string=None):
        self.string = string

    @property
    def data_type(self):
        return "VARCHAR"

    @property
    def fld_name(self):
        return str(self.string)


class Integer:
    def __init__(self, string=None):
        self.string = string

    @property
    def data_type(self):
        return "INTEGER"

    @property
    def fld_name(self):
        return str(self.string)

class Boolean:
    def __init__(self, string=None):
        self.string = string

    @property
    def data_type(self):
        return "BOOLEAN"

    @property
    def fld_name(self):
        return str(self.string)
    
class ForeignKey:
    def __init__(self, table):
        self.table = table  
        
        
#new fields
    
class Float:
    def __init__(self, string=None):
        self.string = string
        
    @property
    def fld_name(self):
        return str(self.string)
    
    @property
    def data_type(self):
        return "DECIMAL"
    
class Datetime:
    def __init__(self, string):
        self.string = string
        
    @property
    def fld_name(self):
        return str(self.string)
    
    @property
    def data_type(self):
        return "TIMESTAMP"
    
class Date:
    def __init__(self, string):
        self.string = string
        
    @property
    def fld_name(self):
        return str(self.string)
    
    @property
    def data_type(self):
        return "DATE"

