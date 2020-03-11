## dfa,nfa的结构体

from graphviz import Digraph
from myNode import Node
class NFA:
    def __init__(self):
        self.total = []     # 所有状态
        self.initial = []     # 初始状态
        self.final = []     # 最终状态
        self.map=[]
        self.num=0  #边的条数
        self.weight = []     # 权重

    def GetNFA(self,mymap):
        num=0
        
        first=[]
        next=[]
        # 初始化权重
        for node in mymap:
            if node.input not in self.weight:
                if node.input !='-':
                    self.weight.append(node.input)
                    #print(node.input)
        # 获得所有字符集
        for node in mymap:
            if node.id not in self.total:
                self.total.append(node.id)
            if node.nextid not in self.total:
                self.total.append(node.nextid)

        # 获得first,next
        for node in mymap:
            if node.id not in first:
                first.append(node.id)
            if node.nextid not in next:
                next.append(node.nextid)
        
        # 获得initial
        for i in first:
            if i not in next:
                if i not in self.initial:

                    self.initial.append(i)

        #获得final
        for i in next:
            if i not in first:
                if i not in self.final:
                    self.final.append(i)
        

        #self.initial=start
        #self.final=fin
        # 获得所有的边
        for node in mymap:
            self.map.append(node)
            num=num+1
        # 获得边的个数
        self.num=num    

        a=self.total[0]
        if self.initial:
            self.num=num
        else:
            for i in range(0,len(self.total)):
                if self.total[i]<a:
                    a=self.total[i]
            self.initial.append(a)


        if self.final:
            self.num=num
        else:
            for i in range(0,len(self.total)):
                if self.total[i]>a:
                    a=self.total[i]

            self.final.append(a)

        print("DFA结构体完成\n共"+str(num))
        
    

    def PrintG(self,s,fname):
        dot = Digraph(comment=s)
        for ch in self.total:
            dot.node(ch,ch)
        for node in self.map:
            dot.edge(node.id, node.nextid, node.input)
        #dot.save(s+".gv")
        #dot.save(s+".gv.pdf")
        dot.render(fname, view=True)
        #dot.view()
        #print(dot.source)
        print(s+"图片完成")
        