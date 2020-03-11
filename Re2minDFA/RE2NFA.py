## 从正则表达式到NFA

from myStack import myStack
from myNode import Node
from myNFA import NFA
        
def Getmap(s):
    j=0
    expression=''
    expression=s
    mymap=[]
    node=Node()
    nowId=0
    s_st=myStack()
    s_ed=myStack()
    s_str=myStack()

    s_str.push('$')
    
    s_st.push(nowId)
    nowId=nowId+1
    s_ed.push(nowId)
    nowId=nowId+1

    for i in expression:
        
        ch=expression[j]
        if ch=='(':
            
            s_ed.push(nowId)
            nowId=nowId+1
            s_str.push('(')
        elif ch==')':
            ed=s_ed.top()
            st=s_st.top()
            node=Node()
            node.getadd(str(st),'-',str(ed))
            mymap.append(node)
            #print(str(st)+'-'+str(ed))
            ch=s_str.top()
            while ch != '(':
                nxt=s_st.top()
                s_st.pop()
                pre=s_st.top()
                if ch !='#':
                    node=Node()
                    node.getadd(str(pre),ch,str(nxt))
                    mymap.append(node)
                    #print(str(pre)+ch+str(nxt))
                s_str.pop()
                ch=s_str.top()
            s_str.pop()
            s_str.push('#')
            top_num=s_ed.top()
            s_st.push(top_num)
            s_ed.pop()
        elif ch=='|':
            ed=s_ed.top()
            st=s_st.top()
            node=Node()
            node.getadd(str(st),'-',str(ed))
            mymap.append(node)
            #print(str(st)+"-"+str(ed))
            ch=s_str.top()
            while ch !='(' and ch!='$':
                nxt=s_st.top()
                s_st.pop()
                pre=s_st.top()
                if ch !='#':
                    node=Node()
                    node.getadd(str(pre),ch,str(nxt))
                    mymap.append(node)
                    #print(str(pre)+ch+str(nxt))
                s_str.pop()
                ch=s_str.top()
        elif ch=='*':
            nxt=s_st.top()
            s_st.pop()
            pre=s_st.top()

            node=Node()
            node.getadd(str(pre),'-',str(nxt))
            mymap.append(node)
            #print(str(pre)+"-"+str(nxt))
            node=Node()
            node.getadd(str(nxt),'-',str(pre))
            mymap.append(node)
            #print(str(nxt)+"-"+str(pre))

            s_st.push(nxt)
        else:
            s_str.push(ch)
            
            s_st.push(nowId)
            nowId=nowId+1
        j=j+1

        
    ch=s_str.top()
    while ch!='$':
        nxt=s_st.top()
        s_st.pop()
        pre=s_st.top()
        if ch !='#':
            node=Node()
            node.getadd(str(pre),ch,str(nxt))
            mymap.append(node)
            #print(str(pre)+ch+str(nxt))
        s_str.pop()
        ch=s_str.top()
    
    return mymap


'''
def GetDFA(mymap):
    num=0
    nfa=NFA()
    first=[]
    next=[]
    # 初始化权重
    for node in mymap:
        if node.input not in nfa.weight:
            if node.input !='-':
                nfa.weight.append(node.input)
                #print(node.input)
    # 获得所有字符集
    for node in mymap:
        if node.id not in nfa.total:
            nfa.total.append(node.id)
        if node.nextid not in nfa.total:
            nfa.total.append(node.nextid)

    # 获得first,next
    for node in mymap:
        if node.id not in first:
            first.append(node.id)
        if node.nextid not in next:
            next.append(node.nextid)

    # 获得initial
    for i in first:
        if i not in next:
            nfa.initial.append(i)

    #获得final
    for i in next:
        if i not in first:
            nfa.final.append(i)

    # 获得所有的边
    for node in mymap:
        nfa.map.append(node)
        num=num+1
    # 获得边的个数
    nfa.num=num    
    print("DFA结构体完成\n共"+str(num))
    return nfa
'''
def re2NFA(fname):
    with open(fname) as f:
        line = f.readline()
        print("正则表达式为："+line)

    mymap=Getmap(line)
    #PrintNFA(mymap)
    nfa=NFA()
    nfa.GetNFA(mymap)
    nfa.PrintG("NFA","test-output/NFA.gv")
    print("获得NFA")
    return nfa

