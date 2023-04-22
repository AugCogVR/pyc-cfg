# About this fork

This fork has been updated to work with Python 3 and clang 10. 

It has only been tested in the limited use case I have for it, so YMMV.

It assumes libclang.so (for clang 10) is in the repo's root folder (either a copy or link). I might have included my copy (for Ubuntu) in the repo.

Run "generateCFG.py" with a single command line argument of the source code filename. Use redirection to put the outputs into another file.

Thank you to the original author for this fine utility.

Original README follows...

---------------------------------

# pyc-cfg

Pyc-cfg is a pure python control flow graph builder for almost all Ansi C programming language. It works by building the CFG from the abstract syntax tree generated by [Clang](https://github.com/llvm-mirror/clang), and accessing it through its [python bindings](https://github.com/llvm-mirror/clang/tree/master/bindings/python) to libclang. I started this project back in 2015 as a way to learn more about compilers and static code analysis while studying my computer engineering career. Right now the code is being improved to be more pythonic and better comply with style rules, although there are some complex C language constructions that have not yet been implemented, their operation is adequate. I will be more than grateful to respond to any error report or problem you may encounter.

### What is a CFG?
In a few words and quoting wikipedia, 
> A control flow graph (CFG) in computer science is a representation, using graph notation, of all paths that might be traversed through a program during its execution.

Probably a more accurate and extensive definition can be found in the [Dragon Book](https://www.amazon.es/Compilers-Principles-Techniques-Tools-Gradiance/dp/0321547985/ref=sr_1_1?s=foreign-books&ie=UTF8&qid=1517056798&sr=1-1&keywords=compilers+principles%2C+techniques%2C+and+tools), which says the following:
> A Flow Graph is a graph representation of intermediate code. The representation is constructed as follows:  
 > 1. Partition  the  intermediate  code  into basic blocks, which  are  maximal  sequences  of consecutive  three-address  instructions  with  the  properties  that:  
> a) The  flow  of  control  can  only  enter  the  basic  block  through  the  first instruction  in  the  block.  That  is,  there  are  no jumps  into the  middle of  the  block.  
> b) Control will leave the block without halting or branching, except possibly  at  the  last  instruction  in  the  block.  
> 2. The  basic  blocks  become  the  nodes  of  a flow  graph, whose  edges  indicate which  blocks  can  follow  which  other  blocks.  

A Control Flow Graph can be used for many things, from the generation of source code, to the construction of a static source code analyzer.
### What are libclang and the python bindings?
As its [documentation](https://clang.llvm.org/doxygen/group__CINDEX.html) says:
> Libclang: The C Interface to Clang provides a relatively small API that exposes facilities for parsing source code into an abstract syntax tree (AST), loading already-parsed ASTs, traversing the AST, associating physical source locations with elements within the AST, and other facilities that support Clang-based development tools.

And the python bindings, as it says in [its code](https://github.com/llvm-mirror/clang/blob/master/bindings/python/clang/cindex.py):
> This module provides an interface to the Clang indexing library. It is a low-level interface to the indexing library which attempts to match the Clang API directly while also being "pythonic".
# Installation
The installation is relatively simple and the only step that can lead to complications is locating libclang.
```
apt-get install clang
pip install -r requirements.txt
```
At this point you must locate libclang and perform a symbolic link as it appears in the lower capture. I have found libclang in two positions within the file system in Debian operating systems, depending on whether it is x64 or x86:
* x64
```
ln -s /usr/lib/x86_64-linux-gnu/libclang* libclang.so
```
* x86
```
ln -s /usr/lib/llvm-4.0/lib/libclang* libclang.so
```
After this, you only have to indicate to the python bindings where the new symbolic link to libclang is located, to do this, you must open the **utils.py** file and modify the following line by entering the path where you have created the symbolic link:
```
Config.set_library_path('/usr/lib/llvm-4.0/lib') 
```
# Usage
* example.c
```
#include <stdio.h>

int addNumbers(int a, int b);

int main()
{
  int n1 = 0;
  int n2 = 1;
  int sum;  
  sum = addNumbers(n1, n2);
  printf("sum = %d",sum);
  return 0;
}

int addNumbers(int a,int b)
{
    int result;
    result = a+b;
    return result;
}

```
* cfg_builder.py
```
from utils import buildCFG

cfg = buildCFG('example.c', 'addNumbers')

print "[+] Size of the CFG:", str(cfg.size())
print cfg.printer()
```
Output:
```
[+] Size of the CFG: 2
[B0]
Preds (1): B1

[B1]
0: int result;
1: RefExpr: a
2: Implicit Cast
3: RefExpr: b
4: Implicit Cast
5:  a + b
6: RefExpr: r
7:  result = a + b
8: RefExpr: r
9: Implicit Cast
10:  return result
Preds (1): B2
Succs (1): B0

[B2]
Succs (1): B1

=>Entry: 2
<=Exit: 0
```
* cfg_builder2.py
```
from utils import buildCFG

cfgs = buildCFG('example.c')

for cfg in cfgs:
    print "\n[+] Function: ", cfg[0]
    print cfg[1].printer()
```
Output:
```
[+] Function:  main
[B0]
Preds (1): B1

[B1]
0: value: 0
1:  return 0
Preds (1): B2
Succs (1): B0

[B2]
0: RefExpr: s
1:  sum = addNumbers ( n1 , n2 )
2: RefExpr: p
3: Implicit Cast
4: printf
Preds (1): B3
Succs (1): B1

[B3]
0: value: 0
1: int n1;
2: value: 1
3: int n2;
4: int sum;
5: RefExpr: a
6: Implicit Cast
7: addNumbers
Preds (1): B4
Succs (1): B2

[B4]
Succs (1): B3

=>Entry: 4
<=Exit: 0


[+] Function:  addNumbers
[B0]
Preds (1): B1

[B1]
0: int result;
1: RefExpr: a
2: Implicit Cast
3: RefExpr: b
4: Implicit Cast
5:  a + b
6: RefExpr: r
7:  result = a + b
8: RefExpr: r
9: Implicit Cast
10:  return result
Preds (1): B2
Succs (1): B0

[B2]
Succs (1): B1

=>Entry: 2
<=Exit: 0
```
# Disclaimer
As I said before, I started this project back in 2015 as a way to learn about source code static analysis and compilers. When I wrote this code I was an initiate in Python, therefore, both the architecture and the syntax can be improved a lot. I will invest effort in improving all those things.
On the other hand, you can see how I have included the main file of the clang python-bindings in the project (```clang/cindex.py```). This is because Clang is in constant development and it may be that if you have a different version of python bindings, it is not compatible. Regardless of this, you can always delete that folder and access the python-bindings without making any changes to the code by installing the package ```pip install clang```.
