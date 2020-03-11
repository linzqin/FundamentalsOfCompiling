##主函数

from RE2NFA import *
from NFA2DFA import *
from minDFA import *
if __name__=="__main__":
    nfa=re2NFA("data.txt")
    dfa=nfa2dfa(nfa)
    min=mindfa(dfa)
    print("Successful")
    
