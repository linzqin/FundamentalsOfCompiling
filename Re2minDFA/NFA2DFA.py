import operator
from myNFA import NFA
from myNode import Node
from RE2NFA import *
from myZijizu import ZijiZu
import numpy as np
def trynfa():
    
    nfa=NFA()
    node=Node()
    mymap=[]
    node.getadd('1','a','2')
    mymap.append(node)
    node=Node()
    node.getadd('1','b','1')
    mymap.append(node)
    node=Node()
    node.getadd('1','-','3')
    mymap.append(node)
    node=Node()
    node.getadd('2','a','1')
    mymap.append(node)
    node=Node()
    node.getadd('3','a','3')
    mymap.append(node)
    node=Node()
    node.getadd('3','b','4')
    mymap.append(node)
    node=Node()
    node.getadd('4','b','3')
    mymap.append(node)

    nfa.GetNFA(mymap)
    print("nfa获得")
    return nfa

def Sort(s,change):
    for j in range(0,Length(s)):
        for i in range(0,Length(s)-1):
            if s[i] in change and s[i+1] in change:
                if change.index(s[i]) > change.index(s[i+1]):
                    b=s[i]
                    s[i]=s[i+1]
                    s[i+1]=b

def isfalse(flag):
    flag2=1
    for ab in range(0,100):
        if flag[ab]==False:
            flag2=0
            break
    return flag2


def add(T,a):
    flag=0
    for i in range(0,100):
        if T[i]=='':
            flag=i
            break
    T[i]=a
    i=0

def Length(T):
    l=0
    for i in range(0,100):
        if T[i]!='':
            l=l+1
        else:
            if i!=99:
                if T[i+1] !='':
                    l=l+1

    return l

# 当前起始字符，T eclose包，N 总共包长度
def eclose(c,T,mymap,N):
    for i in range(0,N):
        if c==mymap[i].id:
            if mymap[i].input=='-':
                if mymap[i].nextid not in T:
                    add(T,mymap[i].nextid)
                    eclose(mymap[i].nextid,T,mymap,N)# 继续寻找下一个遇见空串


def move(he,m,mymap,N,change):
    len1=Length(he.T)
    len2=Length(he.jihe[m])
    for i in range(0,len1):
        for j in range(0,N):
            
            if change[m]==mymap[j].input[0] and he.T[i]==mymap[j].id[0]:
                if mymap[j].nextid not in he.jihe[m]:
                    add(he.jihe[m],mymap[j].nextid)
                    

    for i in range(0,len2):
        for j in range(0,N):
            
            if change[m]==mymap[j].input[0] and he.jihe[m][i]==mymap[j].input:
                if mymap[j].nextid not in he.jihe[m]:
                    add(he.jihe[m],mymap[j].nextid)
                    



    return 0

def Getmap(l,h,t,change):
    map1=[]
    node1=Node()
    '''
    s='I      '
    for i in range(0,l):
        s=s+'I'
        s=s+change[i]
        s=s+'        '
    print(s)
    print('---------------------------------------')
    '''
    for i in range(0,h):
        
        s=''
        m=Length(t[i].T)
        for j in range(0,m):
            s=s+t[i].T[j]
        st=s
        s=s+'          '
        #print(s)
        
        a=''
        
        for j in range(0,l):
            w=change[j]
            x=''
            for k in range(0,Length(t[i].jihe[j])):
                x=x+t[i].jihe[j][k]
            ed=x
            if ed!='':
            
                
                node1.getadd(st,w,ed)
                map1.append(node1)
                node1=Node()
            else:
                h=h-1
            
            
        
        #print(s)
    
    return map1

def Rename(map1):
    re=[]
    map2=[]
    node2=Node()
    re.append(map1[0].id)
    
    for i in range(0,len(map1)):
        if map1[i].id not in re:
            
            re.append(map1[i].id)
            
        if map1[i].nextid not in re:
            re.append(map1[i].nextid)

    for i in range(0,len(map1)):
        x=re.index(map1[i].id)
        y=re.index(map1[i].nextid)
        node2.getadd(str(x),map1[i].input,str(y))
        
        map2.append(node2)
        node2=Node()

    return map2



    





	
#if __name__=="__main__":
def nfa2dfa(nfa):
    #nfa=trynfa()
    mymap=nfa.map
    N=nfa.num
    t=[]
    c=ZijiZu()
    add(c.T,mymap[0].id)
    t.append(c)
    eclose(mymap[0].id,t[0].T,mymap,N)
    h=1
    i=0
    flag1=1
    flag2=True
    flag3=1
    #for i in range(0,h):
    while flag1:
        for j in range(0,Length(t[i].T)):
            for m in range(0,len(nfa.weight)):
                #x=[]
                #eclose(t[i].T[j],x,mymap,N)
                #if len(x)!=0:
                #    t[i].jihe.append(x)
                eclose(t[i].T[j],t[i].jihe[m],mymap,N)
                
        for k in range(0,len(nfa.weight)):
            move(t[i],k,mymap,N,nfa.weight)
            for j in range(0,Length(t[i].jihe[k])):
                eclose(t[i].jihe[k][j],t[i].jihe[k],mymap,N)
        for j in range(0,len(nfa.weight)):
            Sort(t[i].jihe[j],nfa.total)
            #for k in range(0,h):
            k=0
            flag3=1
            while flag3:
                flag=operator.eq(t[k].T,t[i].jihe[j])
                flag2=isfalse(flag)
                        
                if flag2:
                    break
                k=k+1
                if k>=h:
                    flag3=0
            if flag2==0 and Length(t[i].jihe[j]):
                c=ZijiZu()
                c.T=t[i].jihe[j]
                
                if (len(t)-1)<h:
                     t.append(c)
                else:
                    t[h]=c
                h=h+1
        i=i+1        
        if i>=h:
            flag1=0
        

    print("状态转换矩阵完成")
    map1=Getmap(len(nfa.weight),h,t,nfa.weight)
    print("重命名")
    map2=Rename(map1)
    dfa=NFA()
    dfa.GetNFA(map2)
    dfa.PrintG("DFA","test-output/DFA.gv")
    print("NFA装DFA完成")
    return dfa


    