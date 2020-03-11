#from enum import Enum
#FUN=Enum('FUN',('LIT','LOD','STO','CAL','INT','JMP','JPC','OPR'))

class PCode:
    def __init__(self,operate,l,a):
        self.f=operate
        self.l=l#层次差
        self.a=a