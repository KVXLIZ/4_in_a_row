class Tree:
    def __init__(self, cols):
        self.key = None
        self.val = 0.0
        self.children = [None for _ in range(cols)]
    
    