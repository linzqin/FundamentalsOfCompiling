from symbol import KEYWORDS,OPERATORS,DELIMITERS,SYM,ident,number,IDi,NUM,Position
from node import Node
from table import Table,Entry,isConst,KIND
from inst import Code
p = 0
pid=0
pnum=0
Error = 0
root=Node('<程序>')
table=Table()#table表
code=[]#CODE数组
startCode=Code('JMP',0,None)
code.append(startCode)
code.append(Code('JMP',0,2))
tableList=[]
def error(a = 0):  # 出错
    case = [
        '0 '
    ]
    # print("Error:",p)
    exit(-1)


def advance():
    global p
    p = p+1
    

def program():
    if SYM[p] == KEYWORDS['program']:
        Table, entry=G2(table)
    tableList.append(Table)
    entry = None
    block(root,table,entry)


def block(root,table,entry):#<程序>
    startAddr = B(root,table,entry)
    startCode.a = startAddr
    if Error == 1:
        error()
    elif p == len(SYM):
        print("目标代码已生成")
    else:
        x,y = Position[p][0],Position[p][1]
        print('({},{})执行语句未在begin…end中'.format(x-1,y))
        error()


def B(parent,table,enrty=None):#<分程序>
    global p
    if SYM[p] != KEYWORDS['const'] and SYM[p] != KEYWORDS['var'] and SYM[p] != KEYWORDS['procedure']and SYM[p] != KEYWORDS['begin']:
        print(Position[p], 'block中需要关键词const or var or procedure or begin')
        global Error
        Error = 1
        while p<len(SYM)-1 and SYM[p] != KEYWORDS['const'] and SYM[p] != KEYWORDS['var'] and SYM[p] != KEYWORDS['procedure']:
            p += 1
    child=Node('<分程序>')
    parent.add(child)
    Const(child,table)
    E(child,table)
    if SYM[p] == KEYWORDS['procedure']:
        F(child,table)
    startAddr=len(code)
    if enrty!=None:
        enrty.adr=startAddr
    code.append(Code('INT',0,table.getSize()))
    H(child,table)
    code.append(Code('OPR',0,0))
    return startAddr


def Const(parent, table): # <常量说明部分>
    if SYM[p] == KEYWORDS['const']:
        child=Node('<常量说明部分>')
        parent.add(child)
        child.add(Node('const'))
        advance()
        Define_const(child,table)
        while SYM[p] == DELIMITERS[',']:
            child.add(Node(','))
            advance()
            Define_const(child,table)
        if SYM[p] == DELIMITERS[';']:
            child.add(Node(';'))
            advance()
        else:
            print(Position[p],"行末缺少分号")
            global Error
            Error = 1


def Define_const(parent,table):#<常量定义>
    global Error
    child=Node('<常量定义>')
    parent.add(child)
    if SYM[p] != ident:
        print(Position[p], "常量定义类型错误，应为ident")
        Error = 1
    name=Ident(child,table)
    advance()
    if SYM[p] != OPERATORS[':=']:
        print(Position[p], "赋值号错误，赋值号为:=")
        Error = 1
    child.add(Node(':='))
    advance()
    if SYM[p] != number:
        print(Position[p], "常量赋值错误，只能用常数赋值")
        Error = 1
    val=W(child,table)
    advance()
    entry=Entry(name,KIND.CONSTANT,val)
    t = table.add(entry)
    if t == 1:
        print(Position[p],entry.name + ' 重定义')
        Error = 1


def E(parent,table):#<变量说明部分>
    global Error
    if SYM[p] == KEYWORDS['var']:
        child=Node('<变量说明部分>')
        parent.add(child)
        child.add(Node('var'))
        advance()
        if SYM[p] != ident:
            print(Position[p], "变量类型定义错误，只能是ident")
            Error = 1
        name=Ident(child,table)
        entry=Entry(name,KIND.VARIABLE)
        t = table.add(entry)
        if t == 1:
            print(Position[p], entry.name + ' 重定义')
            Error = 1
        advance()
        while SYM[p] == DELIMITERS[',']:
            child.add(Node(','))
            advance()
            if SYM[p]!=ident:
                print(Position[p], "变量类型定义错误，只能是ident")
                Error = 1
            name=Ident(child,table)
            entry=Entry(name,KIND.VARIABLE)
            t = table.add(entry)
            if t == 1:
                print(Position[p], entry.name + ' 重定义')
                Error = 1
            advance()
        if SYM[p] == DELIMITERS[';']:
            child.add(Node(';'))
            advance()
        else:
            print(Position[p], "行末缺少分号")
            Error = 1


def F(parent,table):#<过程说明部分>
    child=Node('<过程说明部分>')
    parent.add(child)
    (childTable,entry)=G(child,table)
    tableList.append(childTable)
    B(child,childTable,entry)
    #table.entries[name].adr=len(code)
    while SYM[p] == DELIMITERS[';']:
        child.add(Node(';'))
        advance()
        if SYM[p] == KEYWORDS['procedure']:
            F(child,table)
        else:
            error()


def G(parent,table):#<过程首部>
    global Error
    if SYM[p] == KEYWORDS['procedure']:
        child=Node('<过程首部>')
        parent.add(child)
        child.add(Node('procedure'))
        advance()
        if SYM[p] != ident:
            print(Position[p],'procedure后面缺少ident')
            Error = 1
        name=Ident(child,table)
        entry=Entry(name,KIND.PROCEDURE)
        t = table.add(entry)
        if t == 1:
            print(Position[p], entry.name + ' 重定义')
            Error = 1
        childTable=Table(table)
        advance()
        if SYM[p] != DELIMITERS['(']:
            print(Position[p],"procedure后面缺少()")
            Error = 1
        advance()
        while (SYM[p] == ident):
            name = Ident(child, table)
            entry1 = Entry(name, KIND.VARIABLE)
            childTable.add(entry1)
            advance()
            while SYM[p] == DELIMITERS[',']:
                child.add(Node(','))
                advance()
                if SYM[p] == ident:
                    name = Ident(child, table)
                    entry1 = Entry(name, KIND.VARIABLE)
                    childTable.add(entry1)
                    advance()
                else:
                    print(Position[p],"传参只能传ident")
                    Error = 1
        if SYM[p] == DELIMITERS[')']:
            advance()
        else:
            print(Position[p],"缺少‘)’")
            Error = 1
        if SYM[p]==DELIMITERS[';']:
            child.add(Node(';'))
            advance()
            return childTable,entry
        else:
            print(Position[p], "缺少分号")
            Error = 1
    else:
        print(Position[p],"递归错误！")
        Error = 1
        error()
    

def G2(table):#<过程首部>
    global Error
    if SYM[p] != KEYWORDS['program']:
        print(Position[p], "缺少程序开始标志program")
        exit(-1)
    advance()
    if SYM == '(':
        print(Position[p],'program后面缺少ident')
        Error = 1
    elif SYM[p] != ident:
        print(Position[p], "类型错误program后面定义为ident类型")
        Error = 1
    child1 = Node('program')
    name=Ident(child1,table)
    entry=Entry(name,KIND.PROCEDURE)
    t = table.add(entry)
    if t == 1:
        print(Position[p], entry.name + ' 重定义')
        Error = 1
    advance()
    if SYM[p]==DELIMITERS[';']:
        child1.add(Node(';'))
        advance()
        return table,entry
    else:
        child1.add(Node(';'))
        print(Position[p],"行末缺少分号")
        Error = 1
        return table, entry


def H(parent,table):#<语句>
    child=Node('<语句>')  
    if SYM[p]==ident:
        I(child,table)
    elif SYM[p]==KEYWORDS['if']:
        R(child,table)
    elif SYM[p]==KEYWORDS['while']:
        T(child,table)
    elif SYM[p]==KEYWORDS['call']:
        S(child,table)
    elif SYM[p]==OPERATORS['read']:
        U(child,table)
    elif SYM[p]==OPERATORS['write']:
        V(child,table)
    elif SYM[p]==KEYWORDS['begin']:
        J(child,table)
    else:
        return
    parent.add(child)


def I(parent,table):#<赋值语句>
    global Error
    if SYM[p] == ident:
        child=Node('<赋值语句>')
        parent.add(child)
        name=Ident(child,table)
        advance()
        if SYM[p] != OPERATORS[':=']:
            print(Position[p],"赋值号错误！")
            Error = 1
        child.add(Node(':='))
        advance()
        L(child,table)
        (l,a,flag)=table.find(name)
        if a == 0:
            print(Position[p], '错误，未定义的标识符', name)
            Error = 1
        if flag==isConst:
            print(Position[p],'对常量的非法赋值:'+name)
            Error = 1
        else:
            code.append(Code('STO',l,a))
    else:
        print(Position[p],'递归错误')
        error()


def J(parent,table):#<复合语句>
    child=Node('<复合语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['begin']:
        child.add(Node('begin'))
        advance()
        H(child,table)
        while SYM[p] == DELIMITERS[';'] or SYM[p] == ident or SYM[p] == KEYWORDS['if']or SYM[p] == KEYWORDS['begin']or SYM[p] == OPERATORS['read']or SYM[p] == OPERATORS['write']or SYM[p] == KEYWORDS['call']:
            if SYM[p] == DELIMITERS[';']:
                child.add(Node(';'))
                advance()
                H(child, table)
            else:
                print(Position[p], "行末缺少分号")
                global Error
                Error = 1
                child.add(Node(';'))
                H(child, table)
        if SYM[p] == KEYWORDS['end']:
            child.add(Node('end'))
            advance()
        else:
            print(Position[p],"begin后面缺少end")
            Error = 1
    else:
        print(Position[p],"递归错误!")
        error()


def K(parent,table):#<条件>
    child=Node('<条件>')
    parent.add(child)
    if SYM[p] == OPERATORS['+'] or SYM[p] == OPERATORS['-'] or SYM[p] == ident or SYM[p] == number or SYM[p] == DELIMITERS['(']:
        L(child,table)
        opr=Q(child,table)
        L(child,table)
        code.append(Code('OPR',0,opr))
    elif SYM[p] == OPERATORS['odd']:
        child.add(Node('odd'))
        advance()
        L(child,table)
        code.append(Code('OPR',0,OPERATORS['odd']))
    else:
        print(Position[p],"无法识别的条件判断")
        global Error
        Error = 1


def L(parent,table):#<表达式>
    child=Node('<表达式>')
    parent.add(child)
    if SYM[p] == OPERATORS['+']:
        child.add(Node('+'))
        advance()
        M(child,table)
    elif SYM[p] == OPERATORS['-']:
        child.add(Node('-'))
        advance()
        M(child,table)
        code.append(Code('LIT',0,-1))
        code.append(Code('OPR',0,OPERATORS['*']))#如果是-号做取负运算
    else:
        M(child,table)
    while SYM[p]==OPERATORS['+'] or SYM[p]==OPERATORS['-']:
        # print('符号',SYM[p])
        opr=SYM[p]
        O(child,table)
        M(child,table)
        code.append(Code('OPR',0,opr))


def M(parent,table):#<项>
    child=Node('<项>')
    parent.add(child)
    N(child,table)
    while SYM[p]==OPERATORS['*'] or SYM[p]==OPERATORS['/']: # 先乘除，后加减
        opr=SYM[p]
        P(child,table)
        N(child,table)
        code.append(Code('OPR',0,opr))


def N(parent,table): # <因子>
    global Error
    child=Node('<因子>')
    parent.add(child)
    if SYM[p] == ident:
        name=Ident(child,table)
        advance()
        (l,a,flag)=table.find(name)
        if a == 0:
            print(Position[p], '错误，未定义的标识符', name)
            Error = 1
        if flag==isConst:#常量
            code.append(Code('LIT',0,a))
        else:#变量
            code.append(Code('LOD',l,a))
    elif SYM[p] == number:
        val=W(child,table)        
        advance()
        code.append(Code('LIT',0,val))
    elif SYM[p] == DELIMITERS['(']:
        child.add(Node('('))        
        advance()
        L(child,table)
        if SYM[p] == DELIMITERS[')']:
            child.add(Node(')'))        
            advance()
        else:
            print(Position[p],'缺少右括号)')
            Error = 1
    else:
        print(Position[p],"缺少括号")
        Error = 1


def O(parent,table):#<加减运算符>
    child=Node('<加减运算符>')
    parent.add(child)
    if SYM[p] == OPERATORS['+']:
        child.add(Node('+'))        
        advance()
    elif SYM[p] == OPERATORS['-']:
        child.add(Node('-'))        
        advance()
    else:
        print(Position[p],"只能是+或—运算符")
        global Error
        Error = 1


def P(parent,table):#<乘除运算符>
    child=Node('<乘除运算符>')
    parent.add(child)
    if SYM[p] == OPERATORS['*']:
        child.add(Node('*'))        
        advance()
    elif SYM[p] == OPERATORS['/']:
        child.add(Node('/'))        
        advance()
    else:
        print(Position[p],"只能是*或/运算符")
        global Error
        Error = 1


def Q(parent,table):#<关系运算符>
    child=Node('<关系运算符>')
    parent.add(child)
    if SYM[p] == OPERATORS['='] or SYM[p] == OPERATORS['<>'] or SYM[p] == OPERATORS['<'] or SYM[p] == OPERATORS['<='] or SYM[p] == OPERATORS['>'] or SYM[p] == OPERATORS['>=']:
        opr=SYM[p]
        child.add(Node(list(OPERATORS.keys())[list(OPERATORS.values()).index(SYM[p])]))
        advance()
        return opr
    else:
        print(Position[p],"不存在的关系运算符")
        global Error
        Error = 1


def R(parent,table):#<条件语句>
    child=Node('<条件语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['if']:
        child.add(Node('if')) 
        advance()
        K(child,table)
        ret=Code('JPC',0,None)
        code.append(ret)
        if SYM[p] != KEYWORDS['then']:
            child.add(Node('then'))
            H(child, table)
            ret.a = len(code)
            print(Position[p],"缺少then")
            global Error
            Error = 1
        else:
            child.add(Node('then'))
            advance()
            H(child,table)
            ret.a=len(code)
        # while :
    else:
        print(Position[p],"递归错误")
        Error = 1


def S(parent,table):#<过程调用语句>
    global Error
    child=Node('<过程调用语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['call']:
        child.add(Node('call'))
        advance()
        if SYM[p] == ident:
            name1=Ident(child,table)
            advance()
            if SYM[p] == DELIMITERS['(']:
                child.add(Node('('))
                advance()
                if SYM[p] == ident or SYM[p] == number:
                    temp = 3
                    L(child, table)
                    code.append(Code('OPR', temp, 29))
                    while SYM[p] == DELIMITERS[',']:
                        advance()
                        temp += 1
                        L(child, table)
                        code.append(Code('OPR', temp, 29))
                    if SYM[p] == DELIMITERS[')']:
                        child.add(Node(')'))
                        advance()
                    else:
                        print(Position[p],"缺少右括号")
                        Error = 1
                elif SYM[p] == DELIMITERS[')']:
                    child.add(Node(')'))
                    advance()
                else:
                    print(Position[p], "缺少右括号")
                    Error = 1
            else:
                print(Position[p], "call后面缺少括号")
                Error = 1
            (l,a,_)=table.find(name1)
            if a == 0:
                print(Position[p],'错误，未定义的标识符',name1)
                Error = 1
            code.append(Code('CAL',l,a))
        else:
            print(Position[p],"call后面缺少ident")
            Error = 1
    else:
        print(Position[p],"递归错误！")
        exit(-1)


def T(parent,table):#<当型循环语句>
    child=Node('<当型循环语句>')
    parent.add(child)
    if SYM[p] == KEYWORDS['while']:
        child.add(Node('while'))
        advance()
        ret=len(code)
        K(child,table)
        fret=Code('JPC',0,None)
        code.append(fret)
        
        if SYM[p] == KEYWORDS['do']:
            child.add(Node('do'))
            advance()
            H(child,table)
            code.append(Code('JMP',0,ret))
            fret.a=len(code)
        else:
            print(Position[p],"while后面缺少do")
            global Error
            Error = 1
    else:
        print(Position[p],"递归错误")
        error()


def U(parent,table):#<读语句>
    global Error
    child=Node('<读语句>')
    parent.add(child)
    if SYM[p] == OPERATORS['read']:
        child.add(Node('read'))
        advance()
        if SYM[p] == DELIMITERS['(']:
            child.add(Node('('))
            advance()
            if SYM[p] == ident:
                name=Ident(child,table)
                advance()
                code.append(Code('OPR',0,OPERATORS['read']))
                (l,a,flag)=table.find(name)
                if a == 0:
                    print(Position[p],'错误，未定义的标识符',name)
                    Error = 1
                if flag==isConst:
                    print(Position[p],'对常量的非法赋值:'+name)
                    Error = 1
                else:
                    code.append(Code('STO',l,a))
                while SYM[p] == DELIMITERS[',']:
                    child.add(Node(','))
                    advance()
                    if SYM[p] == ident:
                        name=Ident(child,table)
                        advance()
                        code.append(Code('OPR',0,OPERATORS['read']))
                        (l,a,flag)=table.find(name)
                        if a == 0:
                            print(Position[p], '错误，未定义的标识符', name)
                            Error = 1
                        if flag==isConst:
                            print(Position[p],'对常量的非法赋值:'+name)
                            Error = 1
                        else:
                            code.append(Code('STO',l,a))
                    else:
                        print(Position[p],'读操作只能对变量进行')
                        Error = 1
                if SYM[p] == DELIMITERS[')']:
                    child.add(Node(')'))
                    advance()
                else:
                    print(Position[p],"缺少右括号")
                    Error = 1
            else:
                print(Position[p], '读操作只能对变量进行')
                Error = 1
        else:
            print(Position[p], "read后缺少括号")
            Error = 1
    else:
        print(Position[p], "递归错误")
        error()


def V(parent,table):#<写语句>
    child=Node('<写语句>')
    parent.add(child)
    if SYM[p] == OPERATORS['write']:
        child.add(Node('write'))
        advance()
        if SYM[p] == DELIMITERS['(']:
            child.add(Node('('))
            advance()
            L(child,table)
            code.append(Code('OPR',0,OPERATORS['write']))
            while SYM[p] == DELIMITERS[',']:
                child.add(Node(','))
                advance()
                L(child,table)
                code.append(Code('OPR',0,OPERATORS['write']))
            if SYM[p] == DELIMITERS[')']:
                child.add(Node(')'))
                advance()
            else:
                print(Position[p], "缺少右括号")
                global Error
                Error = 1
        else:
            print(Position[p], "write后缺少括号")
            Error = 1
    else:
        print(Position[p], "递归错误")
        error()


def W(parent,table):#<无符号整数>
    global pnum
    child=Node('<无符号整数>')
    parent.add(child)
    val=NUM[pnum]
    child.add(Node(str(val)))
    pnum+=1
    return val


def Ident(parent,table):#<标识符>
    global pid
    child=Node('<标识符>')
    parent.add(child)
    name=IDi[pid]
    child.add(Node(name))
    pid+=1
    return name