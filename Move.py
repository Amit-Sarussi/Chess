class Move:
    def __init__(self, start, end, promotion=None):
        self.start = start
        self.end = end
        self.promotion = promotion
    
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.promotion == other.promotion

    
    def get(self):
        return self.start, self.end, self.promotion
        