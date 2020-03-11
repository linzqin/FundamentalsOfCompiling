from graphviz import Digraph
class Tree:
    def __init__(self,id1,name1,id2,name2):
        self.parentid=id1
        self.parentname=name1
        self.nextid=id2
        self.nextname=name2

        
