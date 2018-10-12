class illustDetailNotFound(Exception):
    def __init__(self,message):
        self.message = message
    def __str__(self):
        return "illustDetailNotFound ," + self.message

class illustListNotFound(Exception):
    def __init__(self,message):
        self.message = message
    def __str__(self):
        return "illustListNotFound ," + self.message