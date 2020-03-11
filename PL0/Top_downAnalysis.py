from symbol import Key,Operation,Border,MYSYM,ident,number,MYID,MYNUM,Location
from node import Node
from table import Table,Entry,isConst,KIND
from pcode import PCode
from tree import Tree
treeid=0
treelist=[]

p = 0
IndetId=0
ChangShuId=0
Error = 0
root=Node('<The program>',0)    # 语法树
table=Table()#table表
code=[]#CODE数组
startCode=PCode('JMP',0,None)
code.append(startCode)
code.append(PCode('JMP',0,2))
tableList=[]



def error(a = 0):  # 出错
    case = [
        '0 '
    ]
    # print("Error:",p)
    exit(-1)


def GoNext():    # 获得下一个单词
    global p
    p = p+1
    

def SyntaxandSemanticAnalysis():
    #if MYSYM[p] == Key['program']:
    #    Table, entry=G2(table)
    #tableList.append(Table)
    entry = None
    block(root,table,entry)


def block(root,table,entry):#<程序>
    global treeid
    startAddr = AddSonProgramNode(root,table,entry)
    startCode.a = startAddr
    if Error == 1:
        error()
    elif p == len(MYSYM):
        print("目标代码已生成")
    else:
        x,y = Location[p][0],Location[p][1]
        print('({},{})执行语句未在begin…end中'.format(x-1,y))
        error()


def AddSonProgramNode(parent,table,enrty=None):#<分程序>
    global p,treeid
    if MYSYM[p] != Key['const'] and MYSYM[p] != Key['var'] and MYSYM[p] != Key['procedure']and MYSYM[p] != Key['begin']:
        print(Location[p], 'block中需要关键词const or var or procedure or begin')
        global Error
        Error = 1
        while p<len(MYSYM)-1 and MYSYM[p] != Key['const'] and MYSYM[p] != Key['var'] and MYSYM[p] != Key['procedure']:
            p += 1
    treeid=treeid+1
    child=Node('<分程序>',treeid)
    
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,treeid,"<block>")
    treelist.append(t)

    if MYSYM[p] == Key['const']: 
        AddConstNode(child,table)  # 分程序有const
    if MYSYM[p] == Key['var']:
        AddVarNode(child,table)     # 分程序是否定义变量
    if MYSYM[p] == Key['procedure']:    # 是否是一个函数
        AddprocedureNode(child,table)
    startAddr=len(code)
    if enrty!=None :
        enrty.adr=startAddr
    code.append(PCode('INT',0,table.getSize()))
    AddStatementNode(child,table)
    code.append(PCode('OPR',0,0))
    return startAddr


def AddConstNode(parent, table): # <常量说明部分>
    global treeid   # 分析树的标识符   
    treeid=treeid+1
    child=Node('<常量说明部分>',treeid)
    parent.AddChild(child)
    # 添加树节点
    t=Tree(parent.treeid,parent.Name,treeid,'<Description of constants>')
    treelist.append(t)
    # <常量说明部分> -> const
    treeid=treeid+1
    child.AddChild(Node('const',treeid))
    t=Tree(child.treeid,child.Name,treeid,'const')
    treelist.append(t)
    GoNext()
    # 添加 <常量定义>
    AddDefine_constNode(child,table)
    while MYSYM[p] == Border[',']:
        # 添加,
        treeid=treeid+1
        child.AddChild(Node(',',treeid))
        t=Tree(child.treeid,child.Name,treeid,',')
        treelist.append(t)
        GoNext()
        AddDefine_constNode(child,table)
    if MYSYM[p] == Border[';']:
        treeid=treeid+1
        child.AddChild(Node(';',treeid))
        t=Tree(child.treeid,child.Name,treeid,';')
        treelist.append(t)
        GoNext()
    else:
        print("缺少分号")
        global Error
        Error = 1


def AddDefine_constNode(parent,table):#<常量定义>  
    global Error,treeid
    treeid=treeid+1
    child=Node('<常量定义>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,treeid,'<Constants defined>')
    treelist.append(t)
    if MYSYM[p] != ident:  # const 后面需要跟着标识符
        print( "<常量定义>错误，缺少标识符")
        exit(-1)
    name=AddIdentNode(child,table)     # 添加<标识符>节点
    GoNext()
    if MYSYM[p] != Operation[':=']:  # 标识符后面需要跟着 :=   
        print(Location[p],"缺少赋值符号")
        exit(-1)   
    treeid=treeid+1
    child.AddChild(Node(':=',treeid))
    t=Tree(child.treeid,child.Name,treeid,':=')
    treelist.append(t)
    GoNext()
    if MYSYM[p] != number:    # := 后面需要跟着 <常数>节点
        print(Location[p], "常量赋值错误，只能用常数赋值")
        Error = 1
    val=AddUnintNode(child,table)    # 添加<常数>节点
    GoNext()
    entry=Entry(name,KIND.CONSTANT,val)       # 新增常量或者变量的时候需要在字符表中新增一条目录
    t = table.add(entry)     # 目录entry添加到字符表的时候需要进行判断是否重定义
    if t == 1:
        print(Location[p],entry.name + ' 重定义')
        Error = 1


def AddVarNode(parent,table):#<变量说明部分>
    global Error,treeid
    
    treeid=treeid+1
    child=Node('<变量说明部分>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,treeid,'<Variable description>')
    treelist.append(t)

    treeid=treeid+1
    child.AddChild(Node('var',treeid))
    t=Tree(child.treeid,child.Name,treeid,'var')
    treelist.append(t)

    GoNext()
    if MYSYM[p] != ident:
        print(Location[p], "变量类型定义错误，只能是ident")
        Error = 1
    name=AddIdentNode(child,table)
    entry=Entry(name,KIND.VARIABLE)
    t = table.add(entry)
    if t == 1:
        print(Location[p], entry.name + ' 重定义')
        Error = 1
    GoNext()
    while MYSYM[p] == Border[',']:
        treeid=treeid+1
        child.AddChild(Node(',',treeid))
        t=Tree(child.treeid,child.Name,treeid,',')
        treelist.append(t)

        GoNext()
        if MYSYM[p]!=ident:
            print(Location[p], "变量类型定义错误，只能是ident")
            Error = 1
        name=AddIdentNode(child,table)
        entry=Entry(name,KIND.VARIABLE)
        t = table.add(entry)
        if t == 1:
            print(Location[p], entry.name + ' 重定义')
            Error = 1
        GoNext()
    if MYSYM[p] == Border[';']:
        treeid=treeid+1
        child.AddChild(Node(';',treeid))
        t=Tree(child.treeid,child.Name,treeid,';')
        treelist.append(t)
        GoNext()
    else:
        print(Location[p], "行末缺少分号")
        Error = 1


def AddprocedureNode(parent,table):#<过程说明部分>
    global treeid
    treeid=treeid+1
    child=Node('<过程说明部分>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,treeid,'<Process description>')
    treelist.append(t)

    (childTable,entry,table)= AddprocedureHeadNode(child,table)
    tableList.append(table)
    tableList.append(childTable)
    AddSonProgramNode(child,childTable,entry)
    #table.entries[name].adr=len(code)
    while MYSYM[p] == Border[';']:
        treeid=treeid+1
        child.AddChild(Node(';',treeid))
        t=Tree(child.treeid,child.Name,treeid,';')
        treelist.append(t)
        GoNext()
        if MYSYM[p] == Key['procedure']:
            AddprocedureNode(child,table)
        else:
            error()


def AddprocedureHeadNode(parent,table):#<过程首部>!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    global Error,treeid
    if MYSYM[p] == Key['procedure']:
        treeid=treeid+1
        child=Node('<过程首部>',treeid)
        parent.AddChild(child)
        t=Tree(parent.treeid,parent.Name,treeid,'<The process first>')
        treelist.append(t)


        treeid=treeid+1
        child.AddChild(Node('procedure',treeid))
        t=Tree(child.treeid,child.Name,treeid,'procedure')
        treelist.append(t)

        GoNext()
        if MYSYM[p] != ident:
            print(Location[p],'procedure后面缺少ident')
            Error = 1
        name=AddIdentNode(child,table)
        entry=Entry(name,KIND.PROCEDURE)
        t = table.add(entry)
        if t == 1:
            print(Location[p], entry.name + ' 重定义')
            Error = 1
        childTable=Table(table)      # level 加1
        GoNext()
        '''
        if MYSYM[p] != Border['(']:
            print(Location[p],"procedure后面缺少()")
            Error = 1
        GoNext()
        while (MYSYM[p] == ident):
            name = AddIdentNode(child, table)
            entry1 = Entry(name, KIND.VARIABLE)
            childTable.add(entry1)
            GoNext()
            while MYSYM[p] == Border[',']:
                treeid=treeid+1
                child.AddChild(Node(',',treeid))
                t=Tree(child.treeid,child.Name,treeid,',')
                treelist.append(t)

                GoNext()
                if MYSYM[p] == ident:
                    name = AddIdentNode(child, table)
                    entry1 = Entry(name, KIND.VARIABLE)
                    childTable.add(entry1)
                    GoNext()
                else:
                    print(Location[p],"传参只能传ident")
                    Error = 1
        if MYSYM[p] == Border[')']:
            GoNext()
        else:
            print(Location[p],"缺少‘)’")
            Error = 1
            '''
        if MYSYM[p]==Border[';']:
            treeid=treeid+1
            child.AddChild(Node(';',treeid))
            t=Tree(child.treeid,child.Name,treeid,';')
            treelist.append(t)

            GoNext()
            return childTable,entry,table
        else:
            print(Location[p], "缺少分号")
            Error = 1
    else:
        print(Location[p],"递归错误！")
        Error = 1
        error()
    
'''
def G2(table):#<过程首部>
    global Error
    if MYSYM[p] != Key['program']:
        print(Location[p], "缺少程序开始标志program")
        exit(-1)
    GoNext()
    if MYSYM[p] == '(':
        print(Location[p],'program后面缺少ident')
        Error = 1
    elif MYSYM[p] != ident:
        print(Location[p], "类型错误program后面定义为ident类型")
        Error = 1
    child1 = Node('program')
    name=AddIdentNode(child1,table)
    entry=Entry(name,KIND.PROCEDURE)
    t = table.add(entry)
    if t == 1:
        print(Location[p], entry.name + ' 重定义')
        Error = 1
    GoNext()
    if MYSYM[p]==Border[';']:
        child1.AddChild(Node(';'))
        GoNext()
        return table,entry
    else:
        child1.AddChild(Node(';'))
        print(Location[p],"行末缺少分号")
        Error = 1
        return table, entry
'''

def AddStatementNode(parent,table):#添加<语句>节点
    global treeid
    treeid=treeid+1
    child=Node('<语句>',treeid)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<statements>')
    treelist.append(t)

    if MYSYM[p]==ident:
        AddGiveValueNode(child,table)
    elif MYSYM[p]==Key['if']:
        AddIfNode(child,table)
    elif MYSYM[p]==Key['while']:
        AddWhileNode(child,table)
    elif MYSYM[p]==Key['call']:
        AddCallNode(child,table)
    elif MYSYM[p]==Operation['read']:
        AddReadNode(child,table)
    elif MYSYM[p]==Operation['write']:
        AddWriteNode(child,table)
    elif MYSYM[p]==Key['begin']:
        AddComplexNode(child,table)
    else:
        return
    parent.AddChild(child)
    


def AddGiveValueNode(parent,table):#添加<赋值语句>节点

    global Error,treeid
    if MYSYM[p] == ident:
        treeid=treeid+1
        child=Node('<赋值语句>',treeid)

        parent.AddChild(child)
        t=Tree(parent.treeid,parent.Name,child.treeid,'<Assignment statement>')
        treelist.append(t)


        name=AddIdentNode(child,table)
        GoNext()
        if MYSYM[p] != Operation[':=']:
            print(Location[p],"赋值号错误！")
            Error = 1
        treeid=treeid+1
        child.AddChild(Node(':=',treeid))
        t=Tree(child.treeid,child.Name,treeid,':=')
        treelist.append(t)

        GoNext()
        AddexpNode(child,table)
        (l,a,flag)=table.find(name)
        if a == 0:
            print(Location[p], '未定义的标识符', name)
            exit(-1)
        if flag==0:
            print(Location[p],'对常量的非法赋值:'+name)
            exit(-1)
        if flag==2:
            print(Location[p],'对函数名的非法赋值:'+name)
            exit(-1)
        if flag==1:
            code.append(PCode('STO',l,a))
    else:
        print(Location[p],'递归错误')
        error()


def AddComplexNode(parent,table):#添加<复合语句>节点
    global treeid
    treeid=treeid+1
    child=Node('<复合语句>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<Compound statement>')
    treelist.append(t)


    if MYSYM[p] == Key['begin']:
        treeid=treeid+1
        child.AddChild(Node('begin',treeid))
        t=Tree(child.treeid,child.Name,treeid,'begin')
        treelist.append(t)

        GoNext()
        AddStatementNode(child,table)
        while MYSYM[p] == Border[';'] or MYSYM[p] == ident or MYSYM[p] == Key['if']or MYSYM[p] == Key['begin']or MYSYM[p] == Operation['read']or MYSYM[p] == Operation['write']or MYSYM[p] == Key['call']:
            if MYSYM[p] == Border[';']:
                treeid=treeid+1
                child.AddChild(Node(';',treeid))
                t=Tree(child.treeid,child.Name,treeid,';')
                treelist.append(t)

                GoNext()
                AddStatementNode(child, table)
            else:
                print(Location[p], "行末缺少分号")
                global Error
                Error = 1
                treeid=treeid+1
                child.AddChild(Node(';',treeid))
                t=Tree(child.treeid,child.Name,treeid,';')
                treelist.append(t)

                AddStatementNode(child, table)
        if MYSYM[p] == Key['end']:
            treeid=treeid+1
            child.AddChild(Node('end',treeid))
            t=Tree(child.treeid,child.Name,treeid,'end')
            treelist.append(t)
            GoNext()

        else:
            print(Location[p],"begin后面缺少end")
            Error = 1
    else:
        print(Location[p],"递归错误!")
        error()


def AddConditionNode(parent,table):#添加<条件>节点
    global treeid
    treeid=treeid+1
    child=Node('<条件表达式>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<Conditional expression>')
    treelist.append(t)

    parent.AddChild(child)
    if MYSYM[p] == Operation['+'] or MYSYM[p] == Operation['-'] or MYSYM[p] == ident or MYSYM[p] == number or MYSYM[p] == Border['(']:
        AddexpNode(child,table)
        opr=AddRelationNode(child,table)
        AddexpNode(child,table)
        code.append(PCode('OPR',0,opr-7))
    elif MYSYM[p] == Operation['odd']:
        treeid=treeid+1
        child.AddChild(Node('odd',treeid))
        t=Tree(child.treeid,child.Name,treeid,'odd')
        treelist.append(t)
        GoNext()
        AddexpNode(child,table)
        code.append(PCode('OPR',0,Operation['odd']))
    else:
        print(Location[p],"无法识别的条件判断")
        global Error
        Error = 1


def AddexpNode(parent,table):#添加<表达式>节点
    global treeid
    treeid=treeid+1
    child=Node('<表达式>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<expression>')
    treelist.append(t)

    if MYSYM[p] == Operation['+']:
        treeid=treeid+1
        child.AddChild(Node('+',treeid))
        t=Tree(child.treeid,child.Name,treeid,'+')
        treelist.append(t)

        GoNext()
        AdditemNode(child,table)

    elif MYSYM[p] == Operation['-']:
        treeid=treeid+1
        child.AddChild(Node('-',treeid))
        t=Tree(child.treeid,child.Name,treeid,'-')
        treelist.append(t)

        GoNext()
        AdditemNode(child,table)
        code.append(PCode('LIT',0,-1))
        code.append(PCode('OPR',0,Operation['*']))#如果是-号做取负运算
    else:
        AdditemNode(child,table)
    while MYSYM[p]==Operation['+'] or MYSYM[p]==Operation['-']:
        # print('符号',MYSYM[p])
        opr=MYSYM[p]-8 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!opr应该是2
        AddAdd_subtractNode(child,table)
        AdditemNode(child,table)
        code.append(PCode('OPR',0,opr))


def AdditemNode(parent,table):#添加<项>节点
    global treeid
    treeid=treeid+1
    child=Node('<项>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<item>')
    treelist.append(t)

    AddfactorNode(child,table)

    while MYSYM[p]==Operation['*'] or MYSYM[p]==Operation['/']: # 先乘除，后加减
        opr=MYSYM[p]
        Addmultiply_divideNode(child,table)
        AddfactorNode(child,table)
        code.append(PCode('OPR',0,opr-8))


def AddfactorNode(parent,table): # 添加<因子>节点
    global Error,treeid
    treeid=treeid+1
    child=Node('<因子>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<factor>')
    treelist.append(t)


    
    if MYSYM[p] == ident:
        name=AddIdentNode(child,table)
        GoNext()
        (l,a,flag)=table.find(name)
        if a == 0:         #####################################################3#3 a=Node
            print(Location[p], '错误，未定义的标识符', name)
            Error = 1
        if flag==isConst:#常量
            code.append(PCode('LIT',0,a))
        else:#变量
            code.append(PCode('LOD',l,a))
    elif MYSYM[p] == number:
        val=AddUnintNode(child,table)        
        GoNext()
        code.append(PCode('LIT',0,val))
    elif MYSYM[p] == Border['(']:
        treeid=treeid+1
        child.AddChild(Node('(',treeid))
        t=Tree(child.treeid,child.Name,treeid,'(')
        treelist.append(t)  

        GoNext()
        AddexpNode(child,table)
        if MYSYM[p] == Border[')']:
            treeid=treeid+1
            child.AddChild(Node(')',treeid))
            t=Tree(child.treeid,child.Name,treeid,')')
            treelist.append(t)        
            GoNext()

        else:
            print(Location[p],'缺少右括号)')
            Error = 1
    else:
        print(Location[p],"缺少括号")
        Error = 1


def AddAdd_subtractNode(parent,table):#添加<加减运算符>节点
    global treeid
    treeid=treeid+1
    child=Node('<加减运算符>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<Add and subtract operators>')
    treelist.append(t)

    
    if MYSYM[p] == Operation['+']:
        treeid=treeid+1
        child.AddChild(Node('+',treeid))
        t=Tree(child.treeid,child.Name,treeid,'+')
        treelist.append(t) 
           
        GoNext()
    elif MYSYM[p] == Operation['-']:
        treeid=treeid+1
        child.AddChild(Node('-',treeid))
        t=Tree(child.treeid,child.Name,treeid,'-')
        treelist.append(t)
              
        GoNext()
    else:
        print(Location[p],"只能是+或—运算符")
        global Error
        Error = 1


def Addmultiply_divideNode(parent,table):#添加<乘除运算符>节点
    global treeid
    treeid=treeid+1
    child=Node('<乘除运算符>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<Multiplication and division operators>')
    treelist.append(t)


    if MYSYM[p] == Operation['*']:
        treeid=treeid+1
        child.AddChild(Node('*',treeid))
        t=Tree(child.treeid,child.Name,treeid,'*')
        treelist.append(t)
     
        GoNext()
    elif MYSYM[p] == Operation['/']:

        treeid=treeid+1
        child.AddChild(Node('/',treeid))
        t=Tree(child.treeid,child.Name,treeid,'/')
        treelist.append(t)
           
        GoNext()
    else:
        print(Location[p],"只能是*或/运算符")
        global Error
        Error = 1


def AddRelationNode(parent,table):#添加<关系运算符>节点
    global treeid
    treeid=treeid+1
    child=Node('<关系运算符>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<Relational operator>')
    treelist.append(t)


    if MYSYM[p] == Operation['='] or MYSYM[p] == Operation['<>'] or MYSYM[p] == Operation['<'] or MYSYM[p] == Operation['<='] or MYSYM[p] == Operation['>'] or MYSYM[p] == Operation['>=']:
        opr=MYSYM[p]
        treeid=treeid+1
        child.AddChild(Node(list(Operation.keys())[list(Operation.values()).index(MYSYM[p])],treeid))
        if list(Operation.keys())[list(Operation.values()).index(MYSYM[p])]=='=':
            s='='
        if list(Operation.keys())[list(Operation.values()).index(MYSYM[p])]=='<>':
            s='<>'
        if list(Operation.keys())[list(Operation.values()).index(MYSYM[p])]=='<':
            s='<'
        if list(Operation.keys())[list(Operation.values()).index(MYSYM[p])]=='<=':
            s='<='
        if list(Operation.keys())[list(Operation.values()).index(MYSYM[p])]=='>':
            s='>'
        if list(Operation.keys())[list(Operation.values()).index(MYSYM[p])]=='>=':
            s='>='
        
        t=Tree(child.treeid,child.Name,treeid,s)
        treelist.append(t)

        GoNext()
        return opr
    else:
        print(Location[p],"不存在的关系运算符")
        global Error
        Error = 1


def AddIfNode(parent,table):#添加<条件语句>节点
    global treeid
    treeid=treeid+1
    child=Node('<条件语句>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<Conditional statements>')
    treelist.append(t)

    if MYSYM[p] == Key['if']:
        treeid=treeid+1
        child.AddChild(Node('if',treeid))
        t=Tree(child.treeid,child.Name,treeid,'if')
        treelist.append(t)

        GoNext()
        AddConditionNode(child,table)
        ret=PCode('JPC',0,None)
        code.append(ret)
        if MYSYM[p] != Key['then']:
            treeid=treeid+1
            child.AddChild(Node('then',treeid))
            t=Tree(child.treeid,child.Name,treeid,'then')
            treelist.append(t)
            
            child.AddChild(Node('then'))
            AddStatementNode(child, table)
            ret.a = len(code)
            print(Location[p],"缺少then")
            global Error
            Error = 1
        else:
            treeid=treeid+1
            child.AddChild(Node('then',treeid))
            t=Tree(child.treeid,child.Name,treeid,'then')
            treelist.append(t)
            
            GoNext()
            AddStatementNode(child,table)
            ret.a=len(code)
        # while :
    else:
        print(Location[p],"递归错误")
        Error = 1


def AddCallNode(parent,table):# 添加<CALL语句>节点

    global Error,treeid
    treeid=treeid+1
    child=Node('<过程调用语句>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<Procedure call statement>')
    treelist.append(t)
    
    if MYSYM[p] == Key['call']:
        treeid=treeid+1
        child.AddChild(Node('call',treeid))
        t=Tree(child.treeid,child.Name,treeid,'call')
        treelist.append(t)
        GoNext()
        if MYSYM[p] == ident:
            name1=AddIdentNode(child,table)
            GoNext()
            '''
            if MYSYM[p] == Border['(']:
                treeid=treeid+1
                child.AddChild(Node('(',treeid))
                t=Tree(child.treeid,child.Name,treeid,'(')
                treelist.append(t)

                GoNext()
                if MYSYM[p] == ident or MYSYM[p] == number:
                    temp = 3
                    AddexpNode(child, table)
                    code.append(PCode('OPR', temp, 29))
                    while MYSYM[p] == Border[',']:
                        GoNext()
                        temp += 1
                        AddexpNode(child, table)
                        code.append(PCode('OPR', temp, 29))
                    if MYSYM[p] == Border[')']:
                        treeid=treeid+1
                        child.AddChild(Node(')',treeid))
                        t=Tree(child.treeid,child.Name,treeid,')')
                        treelist.append(t)
                       
                        GoNext()
                    else:
                        print(Location[p],"缺少右括号")
                        Error = 1
                elif MYSYM[p] == Border[')']:
                    treeid=treeid+1
                    child.AddChild(Node(')',treeid))
                    t=Tree(child.treeid,child.Name,treeid,')')
                    treelist.append(t)
                    
                    GoNext()
                else:
                    print(Location[p], "缺少右括号")
                    Error = 1
            else:
                print(Location[p], "call后面缺少括号")
                Error = 1
            '''
            (l,a,flag)=table.find(name1)
            if a == 0:
                print(Location[p],'错误，未定义的标识符',name1)
                Error = 1
            if flag!=2:
                print(Location[p],'调用非函数名',name1)
                Error = 1
            code.append(PCode('CAL',l,a))
        else:
            print(Location[p],"call后面缺少ident")
            Error = 1
    else:
        print(Location[p],"递归错误！")
        exit(-1)


def AddWhileNode(parent,table): # 添加<WHILE型循环语句>节点
    global treeid
    treeid=treeid+1
    child=Node('<当型循环语句>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<While type loop statement>')
    treelist.append(t)

    
    if MYSYM[p] == Key['while']:
        treeid=treeid+1
        child.AddChild(Node('while',treeid))
        t=Tree(child.treeid,child.Name,treeid,'while')
        treelist.append(t)

        
        GoNext()
        ret=len(code)
        AddConditionNode(child,table)
        fret=PCode('JPC',0,None)
        code.append(fret)
        
        if MYSYM[p] == Key['do']:
            treeid=treeid+1
            child.AddChild(Node('do',treeid))
            t=Tree(child.treeid,child.Name,treeid,'do')
            treelist.append(t)
            
            GoNext()
            AddStatementNode(child,table)
            code.append(PCode('JMP',0,ret))
            fret.a=len(code)
        else:
            print(Location[p],"while后面缺少do")
            global Error
            Error = 1
    else:
        print(Location[p],"递归错误")
        error()


def AddReadNode(parent,table):# 添加<READ语句>节点

    global Error,treeid
    treeid=treeid+1
    child=Node('<读语句>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<Read the statements>')
    treelist.append(t)

    
    if MYSYM[p] == Operation['read']:
        treeid=treeid+1
        child.AddChild(Node('read',treeid))
        t=Tree(child.treeid,child.Name,treeid,'read')
        treelist.append(t)

        GoNext()
        if MYSYM[p] == Border['(']:
            treeid=treeid+1
            child.AddChild(Node('(',treeid))
            t=Tree(child.treeid,child.Name,treeid,'(')
            treelist.append(t)
            
            GoNext()
            if MYSYM[p] == ident:
                name=AddIdentNode(child,table)
                GoNext()
                code.append(PCode('OPR',0,Operation['read']-7)) ################33#OPR 0 16
                (l,a,flag)=table.find(name)
                if a == 0:
                    print(Location[p],'错误，未定义的标识符',name)
                    Error = 1
                if flag==isConst:
                    print(Location[p],'对常量的非法赋值:'+name)
                    Error = 1
                else:
                    code.append(PCode('STO',l,a))
                while MYSYM[p] == Border[',']:
                    treeid=treeid+1
                    child.AddChild(Node(',',treeid))
                    t=Tree(child.treeid,child.Name,treeid,',')
                    treelist.append(t)

                    
                    GoNext()
                    if MYSYM[p] == ident:
                        name=AddIdentNode(child,table)
                        GoNext()
                        code.append(PCode('OPR',0,Operation['read']))
                        (l,a,flag)=table.find(name)
                        if a == 0:
                            print(Location[p], '错误，未定义的标识符', name)
                            Error = 1
                        if flag==isConst:
                            print(Location[p],'对常量的非法赋值:'+name)
                            Error = 1
                        else:
                            code.append(PCode('STO',l,a))
                    else:
                        print(Location[p],'读操作只能对变量进行')
                        Error = 1
                if MYSYM[p] == Border[')']:
                    treeid=treeid+1
                    child.AddChild(Node(')',treeid))
                    t=Tree(child.treeid,child.Name,treeid,')')
                    treelist.append(t)
                    
                    GoNext()
                else:
                    print(Location[p],"缺少右括号")
                    Error = 1
            else:
                print(Location[p], '读操作只能对变量进行')
                Error = 1
        else:
            print(Location[p], "read后缺少括号")
            Error = 1
    else:
        print(Location[p], "递归错误")
        error()


def AddWriteNode(parent,table): #添加<WRITE>节点
    global treeid
    treeid=treeid+1
    child=Node('<写语句>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<Written statement>')
    treelist.append(t)

    
    if MYSYM[p] == Operation['write']:
        treeid=treeid+1
        child.AddChild(Node('write',treeid))
        t=Tree(child.treeid,child.Name,treeid,'write')
        treelist.append(t)

        GoNext()
        if MYSYM[p] == Border['(']:
            treeid=treeid+1
            child.AddChild(Node('(',treeid))
            t=Tree(child.treeid,child.Name,treeid,'(')
            treelist.append(t)

            GoNext()
            AddexpNode(child,table)
            code.append(PCode('OPR',0,Operation['write']-8))
            while MYSYM[p] == Border[',']:
                treeid=treeid+1
                child.AddChild(Node(',',treeid))
                t=Tree(child.treeid,child.Name,treeid,',')
                treelist.append(t)

                GoNext()
                AddexpNode(child,table)
                code.append(PCode('OPR',0,Operation['write']))

            if MYSYM[p] == Border[')']:
                treeid=treeid+1
                child.AddChild(Node(')',treeid))
                t=Tree(child.treeid,child.Name,treeid,')')
                treelist.append(t)

                GoNext()
            else:
                print(Location[p], "缺少右括号")
                global Error
                Error = 1
        else:
            print(Location[p], "write后缺少括号")
            Error = 1
    else:
        print(Location[p], "递归错误")
        error()


def AddUnintNode(parent,table):# 添加<常数>节点,返回常数的值 eg <常数>->10 return 10
    global ChangShuId,treeid

    treeid=treeid+1
    child=Node('<数字>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<digital>')
    treelist.append(t)
    
    val=MYNUM[ChangShuId]

    treeid=treeid+1
    child.AddChild(Node(str(val),treeid))
    t=Tree(child.treeid,child.Name,treeid,str(val))
    treelist.append(t)


    ChangShuId +=1
    return val


def AddIdentNode(parent,table):#  添加<标识符>节点,返回标识符的值 eg <标识符>->a return a 
    global IndetId,treeid

    treeid=treeid+1
    child=Node('<标识符>',treeid)
    parent.AddChild(child)
    t=Tree(parent.treeid,parent.Name,child.treeid,'<identifier>')
    treelist.append(t)

    
    name=MYID[IndetId]
    
    treeid=treeid+1
    child.AddChild(Node(name,treeid))
    t=Tree(child.treeid,child.Name,treeid,name)
    treelist.append(t)

    
    IndetId+=1
    return name