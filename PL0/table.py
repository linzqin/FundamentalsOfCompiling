from enum import Enum
KIND=Enum('KIND',('CONSTANT','VARIABLE','PROCEDURE'))
# print(list(KIND))
isConst=False
isVar=True
class Table:
    def __init__(self,parent=None):
        self.parent=parent
        self.entries={}
        self.dx=3
        if parent==None:
            self.level=0
        else:
            self.level=parent.level+1
    
    def add(self,entry):
        if entry.name in self.entries:
            return 1
        entry.level=self.level
        if entry.kind==KIND.VARIABLE:
            entry.adr=self.dx
            self.dx+=1
        self.entries[entry.name]=entry

    def getSize(self):
        return self.dx

    def find(self,name):#当标识符是变量时返回层差和地址Flag=1，当标识符是常量时返回层差和值Flag=0
        if name in self.entries:
            if self.entries[name].adr==None:#是常量
                return (0,self.entries[name].val,isConst)
            else:
                return (0,self.entries[name].adr,isVar)
        elif self.parent==None:
            return (0,0,0)
        else:
            (l,a,flag)=self.parent.find(name)
            return (1+l,a,flag)

    def __str__(self):
        msg='___________________________________________________________\n'
        for i in self.entries.keys():
            msg+=self.entries[i].__str__()+'\n'
        msg+='___________________________________________________________'
        return msg

class Entry:
    def __init__(self,name,kind,val=None):
        self.name=name
        self.kind=kind
        if kind!=KIND.CONSTANT and val!=None:
            print('非常量无法初始化值')
            return 1
        else:
            self.val=val
        self.level=None
        self.adr=None

    def __str__(self):
        msg='NAME:'+self.name+'\t\t'+self.kind.name+'\t\t'
        if self.val!=None:
            msg+='VAL:'+str(self.val)+'\t\t'
        else:
            msg+='LEVEL:'+str(self.level)+'\t\t'
        msg+='ADR:'+str(self.adr)
        return msg

