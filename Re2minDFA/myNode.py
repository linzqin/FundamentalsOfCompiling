## 每条边的结构体
class Node:
    def __init__(self):
        self.id='-1'
        self.input=''
        self.nextid='-1'
    def getadd(self,st,ch,ed):
        self.id=st
        self.input=ch
        self.nextid=ed