class Tree:
    def __init__(self):
        self.key = None
        self.children = []
    
    #  Sets the key for node
    def setKey(self, k):
        self.key = k
    
    #  Returns the key
    def getKey(self):
        return self.key
    
    #  Appends a child to the list
    def addChild(self, child):
        self.children.append(child)
    
    #  Returns the children of the node
    def getChildren(self):
        return self.children