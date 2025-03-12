class Note:

    def __init__(self, code, text):
       self.code = code
       self.text = text
       self.time_stamp = None
    
    def create_note(code, text):
        return Note(code, text)
    
    def __repr__(self):
        return f"{self.code}, {self.text}"
    
    def __eq__(self, other):
        if other == None:
            return False
        if self.text != other:
            return False
        return True
    
    def set_note(self, code, text):
        self.code = code
        self.text = text
        return self