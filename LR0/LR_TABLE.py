#---------------构造LR(0)表代码--------------#
# 初始化分析表
def init_lr_table(Ilists,G,ACTION,GOTO):
    action_len = len(G.VT)             # 终结符长度
    goto_len   = len(G.VN)             # 非终结符长度
    for Ilists_len in range(len(Ilists)):
        ACTION.append([])
        GOTO.append([])
        for w1 in range(len(G.VT)):  
            ACTION[Ilists_len].append("  ")
        for w2 in range(len(G.VN)):
            GOTO[Ilists_len].append("  ")

# 将分析表保存到excel文件中
def print_lr(ACTION,GOTO,G,path):
    output = open(path,'w',encoding = 'utf-8')
    for i in range(len(ACTION)+2):
        for j in range(len(G.all)+1):
            if i == 0:
                output.write(' ')
                if j == 1:
                    output.write('ACTION')
                if j == len(G.VT)+1:
                    output.write('GOTO')
                output.write('\t')      # 相当于Tab，换下一个单元格
            

            if i ==  1:                
                if j == 0:
                    output.write(' ')
                    output.write('\t')      
                if j <= len(G.VT) and j != 0:
                    output.write(G.VT[j-1])
                    output.write('\t')      
                if j > len(G.VT):
                    output.write(G.VN[j-len(G.VT)-1])
                    output.write('\t')    
           
                          
            if i >  1:                
                if j == 0:
                    output.write(str(i-2))
                    output.write('\t')      
                if j <= len(G.VT) and j != 0:
                    output.write(ACTION[i-2][j-1])
                    output.write('\t')      
                if j > len(G.VT):
                    output.write(str(GOTO[i-2][j-len(G.VT)-1]))
                    output.write('\t')     
            
        output.write('\n')                  # 换行
    output.close()               
                
# 得到分析表
def GET_LR_TABLE(Ilists,G,ACTION,GOTO,path):
    init_lr_table(Ilists,G,ACTION,GOTO) # 初始化分析表    
    for Ilist in Ilists:                # 创建分析表
        for li in Ilist.S:
            x,y = li.split('.')
            
            if y == '':                 # 判断是否写入ACTION
                if li == "S'->S.":    
                    ACTION[Ilist.Id][len(G.VT)-1] = 'acc'             # 接受
                else:                   
                    for i in range(len(ACTION[Ilist.Id])):            # 归约到上一级
                        j = G.P.index(li.replace('.',''))                       
                        ACTION[Ilist.Id][i]="r"+str(j+1)

            else:                 
                if y[0] in G.VT:                                      # 判断是否写入ACTION                    
                    j = Ilist.nextI[y[0]]                    
                    ACTION[Ilist.Id][G.VT.index(y[0])] = "s" + str(j) 
                if y[0] in G.VN:                                      # 判断是否写入GOTO
                    j = Ilist.nextI[y[0]]
                    GOTO[Ilist.Id][G.VN.index(y[0])] = j
                
    print_lr(ACTION,GOTO,G,path)        # 输出分析表
    


                

    
