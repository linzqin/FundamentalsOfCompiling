from myNFA import NFA
from myNode import Node
import numpy as np


def trydfa():
    dfa=NFA()
    mymap=[]
    node=Node()
    node.getadd('0','a','1')
    mymap.append(node)
    node=Node()
    node.getadd('0','b','2')
    mymap.append(node)
    node=Node()
    node.getadd('1','b','3')
    mymap.append(node)
    node=Node()
    node.getadd('2','b','3')
    mymap.append(node)

    dfa.GetNFA(mymap)

    return dfa

# 判断s是否在d中
def isin(s,d):
    flag=1
    if d==[]:
        flag=0
    else:
        
        for i in range(0,len(s)):
            
            if s[i] not in d:
                flag=0
    
    return flag

def add(part,m,n):
    x=[]
    x.append(n)
    
    if part==[]:
        for i in range(0,m):
            part.append([''])
        part.append(x)
    else:
        if m<len(part):
            if part[m]==['']:
                part[m]=x
            else:
                part[m]=part[m]+x
                
        else:
            y=m-len(part)
            for i in range(0,y):
                part.append([''])
            part.append(x)



            


def move(jihe,ch,map,num):
    s=[]
    x=['']
    for i in range(0,len(jihe)):
        for j in range(0,num):
            
            if i>=len(jihe):
                y=i-len(jihe)
                for k in range(0,y):
                    jihe.append(x)
                jihe.append(x)
            

            a=map[j].id
            b=jihe[i]
            c=map[j].input
            if map[j].id==jihe[i] and map[j].input==ch:
                s.append(map[j].nextid)
    
    if s==[]:
        s=["&"]
        return s
    else:
        return s


def divide(weight,map,part,N):
    #global part
    flag=2
    flag0=flag
    part0=[]
    x=[]
    for n in range(0,len(weight)):
        flagm=1
        m=0
        #for m in range(0,flag0):
        while flagm:
            for i in range(0,len(part[m])):
                p=part[m]
                ss=move(p[i],weight[n],map,N)
                j=0
                flagj=1
                #for j in range(0,flag):
                while flagj:
                    if isin(ss,part[j]):
                        p=part[m]
                        add(part0,j,p[i])

                            
                    if ss==['&']:
                        p=part[m]
                        add(part0,flag,p[i])
                        
                        break

                    j=j+1
                    if j>=flag:
                        flagj=0
            #for j in range(0,flag+1):
            flag1=1
            j=0
            while flag1:
                if j>=len(part0):
                    n=j-len(part0)
                    for x in range(0,n):
                        part0.append([''])
                    part0.append([''])
                    
                if part0[j]!=[''] and part0[j] !=part[m]:
                    
                    if flag<len(part):
                       part[flag]=part0[j]
                    else:
                        n=flag-len(part)
                        for x in range(0,n):
                            part.append([''])
                        part.append(part0[j])

                    flag=flag+1
                    l=[]
                    l.append('')
                    part0[j]=l
                    part[m]=l
                else:
                    l=[]
                    l.append('')
                    part0[j]=l
                j=j+1
                if j>flag:
                    flag1=0

            m=m+1
            if m>=flag0:
                flagm=0

        flag0=flag
        

    return flag

def Hebing(zijinum,weight,part,num,map):
    x=[]
    for i in range(0,zijinum):
        x.append('')
    letters=np.array(x)
    letter='A'
    for i in range(0,zijinum):
        if part[i] !=['']:
            letters[i]=letter
            letter=chr(ord(letter)+1)
    mymap=[]
    for i in range(0,zijinum):
        for j in range(0,len(weight)):
            ss=move(part[i],weight[j],map,num)
            
            if part[i] !=[''] and ss !=['&']:
                st=letters[i]
                input=weight[j]
                #print (letters[i]+" "+weight[j])
            for n in range(0,zijinum):
                if isin(ss[0],part[n]):
                    ed=letters[n]
                    s=letters[n]
                    #print(s)
                    node=Node()
                    node.getadd(st,input,ed)
                    mymap.append(node)
    
    return mymap

                




#if __name__=="__main__":
def mindfa(dfa):
    #子集
    part=[]
    #dfa=trydfa()
    mymap=dfa.map
    N=dfa.num
    in1=[]  #非终结状态
    for i in dfa.total:
        if i not in dfa.final:
            in1.append(i)
    part.append(in1)

    part.append(dfa.final)
    zijinum=divide(dfa.weight,mymap,part,N)
    # 输出子集划分
    print("最小划分子集：")
    for i in range(0,zijinum):
        if part[i] !=['']:
            s=''
            for ab in range(0,len(part[i])):
                s=s+part[i][ab]
            print(s)
    
    #print("用大写字母代替子集：")
    #for i in range(0,zijinum):
    #    if part[i] !='':
    #        print("{"+part[i]+"}")
    
    mymap=Hebing(zijinum,dfa.weight,part,N,dfa.map)
    min=NFA()
    min.GetNFA(mymap)
    min.PrintG("minDFA","test-output/minDFA.gv")
    print("minDFA构造完成")