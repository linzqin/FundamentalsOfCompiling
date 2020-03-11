# 通过输入的文法，得到状态集合
from graphviz import Digraph
from myWenfa import WenFa
from myI import I
import numpy as np

li=[]   
Ilists=np.array(li)     #用于存放整个状态集

point=[]     # 所有的加点的产生式

def addPoint(gs):  #加点
    
    point.append("S'->.S")
    point.append("S'->S.")
    
    for p in gs.P:
        x=p.find("->")
        for i in range(len(p)-x-1):
            y=p[:x+2+i]+"."+p[x+2+i:]
            point.append(y)
    
    return point

def KuoChongDaiYue(next,gs):    # 扩充待约项目
    kuo=[]
    for n in next:
        if n not in kuo:
            kuo.append(n)        
        x,y=n.split(".")
        if y!="": 
            a=y[0]
            if a in gs.VN:  
                ne=getVNChanShengSi(a,point)
                for e in ne:
                    if e not in kuo:
                        kuo.append(e)
    return kuo

def FindNextI(llist,a,gs):     #状态list遇见a得到的集合
    next=[]
    for l in llist.S:   
        x,y=l.split(".")
        if y!="":     #.没有位于最后，还有移动空间
            if y[0]==a:    #.的后一位是输入字符a
                n=x+y[0]+"."+y[1:]    #.后移
                next.append(n)
    if (len(next)!=0):
        nextlist=KuoChongDaiYue(next,gs)
        return nextlist

def getVNChanShengSi(S,point):   #"找到S的产生式，即形如S->.aaa"
    l=[]
    for p in point:
        x=p.find("->") 
        if p[0]==S and p[x+2]==".":
            l.append(p)

    return l            
def Isexit(new,Ilists):     #判断状态集是否存在

    if new== None:
        return -1
    
    num=0
    n = set(new)
    for already in Ilists:
        a = set(already.S)
        if(n == a):
            return num
        num = num + 1

    return -1


def GetIlist(gs):
    point=addPoint(gs)  # 得到该文法的所有项目
    
    id=0  # 每个状态的序号
    
    #当前状态I0
    Ilist=I(id)
    s="S'->.S"
    Ilist.S.append(s)
    
    for s in Ilist.S:
        x=s[s.find(".")+1]   #获得.的下一个字母
        if x in gs.VN:  #是非终结符号
            chan=getVNChanShengSi(x,point)  #非终结符号的产生式列表

            for n in chan:
                if n not in Ilist.S:
                    Ilist.S.append(n)

    global Ilists    # 项目集规范组

    Ilists = np.append(Ilists, Ilist)
    
    # 开始寻找下一个状态集合
    flag=1
    num=0
    while flag:
        l=Ilists[num]
        old=l
        
        for a in gs.all:
            
            ne=FindNextI(l,a,gs)   

            if ne != None:
                if Isexit(ne,Ilists)==-1:
                    #将新生成的状态集合添加
                    id =id+1
                    newi=I(id)
                    newi.S=ne
                    Ilists = np.append(Ilists, newi)
                    # 给旧状态集合添加下一个状态
                    
                    old.addnextI(a,id)

        num=num+1
        oldid=l.Id
        Ilists[oldid]=old
        length=len(Ilists)
        if num>=length:
            flag=0

    return Ilists 


#  画出状态集合
def PrintI(Ilists,outname):
    dot = Digraph(comment="I")
    # 创建点
    for I in Ilists:
        s="I"+str(I.Id)+":"
        for c in I.S:
            s=s+str(c)
            s=s+","
        
        dot.node(str(I.Id),s)

    for I in Ilists:
        for key in I.nextI:
            dot.edge(str(I.Id), str(I.nextI[key]), key)
        
    
    dot.render(outname, view=True)
        #dot.view()
        #print(dot.source)
    print("状态集合图片完成")


def GS2I(fname,outname,gs):
    
    # 读入文件，获得基本的文法结构
    with open(fname, "r") as f:
        for line in f:
            line = line.replace('\n', "")
            gs.getP(line)
        f.close()
    
    gs.getV()

    # 获得状态列表

    GetIlist(gs)
    
    
    PrintI(Ilists,outname)
   
    print("状态集合完成！")

    return Ilists


