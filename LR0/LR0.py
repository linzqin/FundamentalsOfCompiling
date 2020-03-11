from GS2I import *
from myI import I
from myWenfa import WenFa
from LR_TABLE import *
from LastTrans import LastTrans

if __name__=="__main__":
    G =  WenFa() 
    ACTION = []
    GOTO   = []
    Ilists=GS2I("1.txt","test-output/I.gv",G)
    GET_LR_TABLE(Ilists,G,ACTION,GOTO,"test-output/lr_table.xls")
    print("LR(0)文法完成")
    StrIn = "abbcde#"  # 待分析字符串
    last = LastTrans(G,ACTION,GOTO,StrIn) 
    if(last == 0):
        print("\n %s 符合文法规则" % StrIn)
    else:
        print("\n %s 不符合文法规则" % StrIn)
    
