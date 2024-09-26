class Tree:
    def __init__(self):
        self.key = None
        self.val = None
        self.children = []
    
    #  Sets the key for node
    def setKey(self, k):
        self.key = k
    
    #  Returns the key
    def getKey(self):
        return self.key
    
        #  Sets the key for node
    def setVal(self, v):
        self.val = v
    
    #  Returns the key
    def getVal(self):
        return self.val
    
    #  Appends a child to the list
    def addChild(self, child):
        self.children.append(child)
    
    #  Returns the children of the node
    def getChildren(self):
        return self.children