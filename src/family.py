class Family:
    def __init__(self, xref_id):
        self.xref_id = xref_id
        self.husb = None
        self.wife = None
        self.children = []
        self.data = {}
        
    def add_data(self, tag, value):
        if tag not in self.data:
            self.data[tag] = []
        self.data[tag].append(value)
        
    def __repr__(self):
        return f"Family({self.xref_id}, husb={self.husb}, wife={self.wife}, children={self.children})"
