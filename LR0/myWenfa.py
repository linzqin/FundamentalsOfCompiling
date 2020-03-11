#整个G[S]相关的的参数

class WenFa:   
    def __init__(self):
        self.P=[]     # 文法规则 eg:["S->aAcBe","A->b",.....]
        self.VN=[]    # 非终结符号
        self.VT=[]    # 终结符号集
        self.dictVN=dict()   # 非终结字符对应的整型，方便LR(0)分析表的生成
        self.dictVT=dict()   ## 终结字符对应的整型
        self.all=[]

    def getP(self,s):    #由文件输入获得文法规则
        self.P.append(s)
    def getV(self):        # 由文法规则获得字母表，非终结符号和终结符号
        #获取终结，非终结
        if len(self.P)==0:
            print("文法规则为空")
        else:
            for p in self.P:
                x,y=p.split("->")
                if x not in self.VN:
                    self.VN.append(x)
                for a in y:
                    if a.isupper():
                        if a not in self.VN:
                            self.VN.append(a)
                    else:
                        if a not in self.VT:
                            self.VT.append(a)

        self.VT.append("#")

        #给每个符号对应的整数标识
        num=0
        for n in self.VN:
            self.all.append(n)
            self.dictVN.update({n:num})            
            num=num+1

        num=0
        for n in self.VT:
            self.all.append(n)
            self.dictVT.update({n:num})
            num=num+1
        print("文法结构体构造完成")
        print("得到非终结符集合："+ str(self.VN))
        print("得到终结符集合：" + str(self.VT))
        print("所有的符号集合" + str(self.all))
        
