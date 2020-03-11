# Pl/0编译器使用说明

参考：https://github.com/King-Hell/pl-0-compiler-vm  
改进：增加报错和子程序传参，修改部分语法bug，如分号（;）只因出现在复合语句中间，end前一句应该没有

## 1.文件说明
    main.py为入口主程序，4.txt和test.txt为测试文件，getsym.py为词法分析，block.py为语法分析和语义分析（同时生产中间代码），symbol.py为类型号设置，table.py为符号表。

## 2.PL/0语言的BNF描述（扩充的巴克斯范式表示法）
> &lt;与虚拟> → program &lt;id>;&lt;block>  
&lt;block> → [&lt;condecl>][&lt;vardecl>][&lt;proc>]&lt;body>  
&lt;condecl> → const &lt;const>{,&lt;const>};  
&lt;const> → &lt;id>:=&lt;integer>  
&lt;vardecl> → var &lt;id>{,&lt;id>};  
&lt;proc> → procedure &lt;id>（[&lt;id>{,&lt;id>}]）;&lt;block>{;&lt;proc>}  
&lt;body> → begin &lt;statement>{;&lt;statement>}end  
&lt;statement> → &lt;id> := &lt;exp>                 
|if &lt;lexp> then &lt;statement>[else &lt;statement>]  
               |while &lt;lexp> do &lt;statement>  
               |call &lt;id>（[&lt;exp>{,&lt;exp>}]）  
               |&lt;body>  
               |read (&lt;id>{，&lt;id>})  
               |write (&lt;exp>{,&lt;exp>})  
&lt;lexp> → &lt;exp> &lt;lop> &lt;exp>|odd &lt;exp>  
&lt;exp> → [+|-]&lt;term>{&lt;aop>&lt;term>}  
&lt;term> → &lt;factor>{&lt;mop>&lt;factor>}  
&lt;factor>→&lt;id>|&lt;integer>|(&lt;exp>)  
&lt;lop> → =|<>|<|<=|>|>=  
&lt;aop> → +|-  
&lt;mop> → *|/  
&lt;id> → l{l|d}   （注：l表示字母）  
&lt;integer> → d{d}  
注释：  
&lt;prog>：程序 ；&lt;block>：块、程序体 ；&lt;condecl>：常量说明 ；&lt;const>：常量；&lt;vardecl>：变量说明 ；&lt;proc>：分程序 ； &lt;body>：复合语句 ；&lt;statement>：语句；&lt;exp>：表达式 ；&lt;lexp>：条件 ；&lt;term>：项 ； &lt;factor>：因子 ；&lt;aop>：加法运算符；&lt;mop>：乘法运算符； &lt;lop>：关系运算符。

## 3.PL/0编译程序的结构图
![image](https://github.com/Wlhang/pl-0-compiler/blob/master/picture/%E7%A8%8B%E5%BA%8F%E7%BB%93%E6%9E%84.png)

## 4.符号表设计
![image](https://github.com/Wlhang/pl-0-compiler/blob/master/picture/%E7%AC%A6%E5%8F%B7%E8%A1%A8.png)

## 5.指令功能表
![image](https://github.com/Wlhang/pl-0-compiler/blob/master/picture/%E6%8C%87%E4%BB%A4%E5%8A%9F%E8%83%BD%E8%A1%A8.png)
