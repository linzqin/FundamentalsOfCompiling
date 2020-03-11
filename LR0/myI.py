# 项目集结构表

class I:   
    def __init__(self,id):
        self.Id=id    #本身的标识  
        self.S=[]     # 项目集包含的项目 eg:["S->.aAcBe","A->.b",.....]
        self.nextI=dict()   #{'a':1} 遇见字符a,去往下个状态I1
        
    def addnextI(self,ch,id):    # 添加字典
        self.nextI.update({ch:id})
 




        