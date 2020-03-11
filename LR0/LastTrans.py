from myWenfa import WenFa
import GS2I
from LR_TABLE import *

#----------定义变量-----------
location = 0  # 输入位置
StackStatus = []  # 状态栈
StackSymbol = []  # 符号栈
StateNow = ''  # 栈顶状态
CharIn = ''  # 栈顶字符
StepNow = 0  # 当前步骤

point=[]#加点后的文法

#-------------判断输入串是否结束-----------
def IsEnd(StrIn):
    if StrIn[location] == '#':     #如果待处理字符为#
        if StackSymbol[-1] == 'S' and StackSymbol[-2] == '#':#符号栈中最后一个元素为S，倒数第二个元素为#
            return True
        else:
            return False
    else:
        return False

    return True


# ----------------输出--------------------
def output(StrIn):
    global StepNow, StackStatus, StackSymbol,StateNow
    print('%d\t\t' % StepNow, end='')     #输出当前步骤序号
    StepNow += 1
    print('%-20s' % StackStatus, end='')   #输出当前状态栈
    print('%-50s' % StackSymbol, end='')   #输出当前符号栈
    print('%-30s' % StrIn[location:len(StrIn)], end='')  #输出待处理的输入串


# ------------确定回退位数------------------
def count_backnum(GramI):
    return len(GramI) - 3 #删去的3为非终结符，-，>；这样即可确定下来回退位数


#--------------规约与移进--------------------
def LastTrans(G,ACTION,GOTO,StrIn):
    # 根据LR(0)表进行规约

    global location
    print('----分析过程----')
    print("index\t\t", end='')
    print('%-20s' % 'Status', end='')
    print('%-50s' % 'Symbol', end='')
    print('%-30s' % 'Input', end='')
    print('Action')
    point=GS2I.addPoint(G)
    for i in range(len(point)):#带点的文法
        print('---', end='')
    print()
    StackSymbol.append('#')#虽然写作stack，但还是list形式。此处为向列表尾部加入一个新元素
    StackStatus.append(0)
    while not IsEnd(StrIn):
        StateNow = StackStatus[-1]#读取状态栈的最后一个字符
        CharIn = StrIn[location]#location指向了要移入的字符
        AllSymbol=G.all
        if(CharIn not in AllSymbol):# 所有的符号集合
            print("未知字符")
            return -1
        output(StrIn)
        operation = ACTION[StateNow][G.dictVT[CharIn]]#读取action中的操作
        #对于分析表来说，ACTION[1][2]中,[1]相当于表格的第一列，[2]相当于表格的第一行
        #得到的operation相当于Sn或rn

        if operation[0] == 's': # 进入action
            StackSymbol.append(CharIn)#符号栈读入要读的字符
            StackStatus.append(int(operation[1]))#状态栈读入n
            location += 1
            print('action[%s][%s]=s%s' % (StateNow, CharIn, operation[1]))

        elif operation[0] == 'r': # 进入goto
            num = int(operation[1])#读取n
            g = G.P[num - 1]#找到对应的文法语句
            backnum = count_backnum(g)#回退位数
            #print("\n%s"%g)
            for i in range(backnum):
                StackStatus.pop()
                StackSymbol.pop()
            StackSymbol.append(g[0])#符号栈输入归约结果
            StateNow = StackStatus[-1]
            symbol_ch = StackSymbol[-1]#读取新的列表尾
            operation = GOTO[StateNow][G.dictVN.get(symbol_ch, -1)]#如果指定值不存在，返回-1
            #返回GOTO表中对应的那个值
            if operation == -1:
                print('分析失败')
                return -1
            StackStatus.append(operation)
            print('%s' % g)
        else:
            return -1

    print("\n 完成")
    return 0
