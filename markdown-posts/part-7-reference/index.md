---
title: "Part VII: Quick Reference"
draft: false
date: "2021-12-20"
series: 
- Writing an X86–64 Assembly Language Program
tags:
- software engineering
- assembly language
- docker
- guides and tutorials
- programming
---

![](beach-sign.webp)

This guide is part seven of the series, [X86–64 Assembly Language Program](https://tonycodes.com/blog/series/writing-an-x8664-assembly-language-program/).

---

This article is more of a reference guide for those learning x86–64 Assembly Language. I hope you find the information and links at the bottom helpful.

# Registers

General-purpose registers — there are 16 general-purpose registers — `rax`, `rbx`, `rcx`, `rdx`, `rbp`, `rsp`, `rsi`, `rdi`, `r8`, `r9`, `r10`, `r11`, `r12`, `r13`, `r14`, `r15`

- `data`- section is used for declaring initialized data or constants
- `bss`- section is used for declaring non initialized variables
- `text`- section is used for code
- `rdi`- first argument
- `rsi`- second argument
- `rdx`- third argument
- `rcx`- fourth argument
- `r8`- fifth argument
- `r9`- sixth

The first six integer or pointer arguments are passed in registers `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9`. `r10` is used as a static chain pointer in the case of nested functions.

`rax` is used as the return value from a function.

The registers `rbx`, `rbp`, and `r12`– `r15` are preserved registers.

All other registers must be saved by the caller if it wishes to preserve its values.

# OPERATIONS

- `ADD`- integer add
- `SUB`- subtract
- `MUL`- unsigned multiply
- `IMUL`- signed multiply
- `DIV`- unsigned divide
- `IDIV`- signed divide
- `INC`- increment
- `DEC`- decrement
- `NEG`- negate

The initial number must be stored in `rax`. `rax` can be multiplied by a value in any of the other registers. The result will be stored in `rax`.

# Control Flow

- `JE` - jump if equal
- `JZ` - jump if zero
- `JNE` - jump if not equal
- `JNZ` - jump if not zero
- `JG` - jump if the first operand is greater than second
- `JGE` - jump if the first operand is greater or equal to second
- `JA` - the same that JG, but performs an unsigned comparison
- `JAE` - the same that JGE, but performs an unsigned comparison

# Date Types

The fundamental data types are bytes, words, doublewords, quadwords, and double quadwords.

- `byte` is eight bits
- `word` is two bytes
- `doubleword` is four bytes
- `quadword` is eight bytes
- `double quadword` is sixteen bytes (128 bits).

# .DATA Directive

Directives are commands that are part of the assembler syntax but are not related to the x86 processor instruction set. All assembler directives begin with a period (.).

The `.DATA` directive is used for setting values in memory.

## Syntax

The syntax within the `.DATA` directive is

`variable name` `define-directive` `initial-value`

There are five basic forms of the define directive −

```
+-----------+-------------------+-------------------+
| Directive |      Purpose      |   Storage Space   |
+-----------+-------------------+-------------------+
| DB        | Define Byte       | allocates 1 byte  |
| DW        | Define Word       | allocates 2 bytes |
| DD        | Define Doubleword | allocates 4 bytes |
| DQ        | Define Quadword   | allocates 8 bytes |
| DT        | Define Ten Bytes  | allocates 10 byte |
+-----------+-------------------+-------------------+
```

For example:

```nasm
choice		DB	'y'
number		DW	12345
```

# GDB

Display the value of `ecx` register which is a char pointer (in other words, print the string referred to):

```bash
display (char *) $ecx
```

Note, this will display the value at every break of the program execution, including each step if you are stepping through. To stop this behavior:

```bash
undisplay 1
```

Note that the number can be two, three, or something else if there are multiple variables in display mode.

# Further Resources

## Tutorial Links

**NASM**

- [NASM Tutorial](http://cs.lmu.edu/~ray/notes/nasmtutorial/)
- [NASM tutorial](http://cs.lmu.edu/~ray/notes/nasmtutorial/)
- [Running Assembly on OS X](https://lord.io/blog/2014/assembly-on-osx/)

**GDB**

- [GDB on OS X](https://lord.io/blog/2014/gdb-on-osx/)

**ASSEMBLY**

- [Say Hello to Assembly (Linux x64)](https://github.com/0xAX/asm)
- [Assembly — Basic Syntax](https://www.tutorialspoint.com/assembly_programming/assembly_basic_syntax.htm)
- [x86–64 Assembly](http://ian.seyler.me/easy_x86-64/)
- [Intro to x64 by Intel](https://software.intel.com/en-us/articles/introduction-to-x64-assembly)
- [Video Series on x86_64 Linux Assembly](https://www.youtube.com/watch?v=VQAKkuLL31g)

**Docker**

- [Why and How to Use Docker for Development](https://medium.com/travis-on-docker/why-and-how-to-use-docker-for-development-a156c1de3b24)

## Quick Reference Links

**NASM**

- [x86_64 NASM Assembly Quick Reference](https://www.cs.uaf.edu/2009/fall/cs301/support/x86_64/index.html)

**LD Linker**

- [ld Linker Man Page](https://github.com/kellyi/nasm-gcc-container)

**Assembly**

- [X86–64 Assembly Programming](https://www.engr.mun.ca/~anderson/teaching/8894/reference/x86-assembly/)
- [X86–64 w/ Ubuntu](http://www.egr.unlv.edu/~ed/assembly64.pdf)
- Intel® 64 and IA-32 Architectures Software Developer's Manual [Part 1](https://www.cs.uaf.edu/2009/fall/cs301/support/x86_64/instructionsAM.pdf), [Part 2](https://www.cs.uaf.edu/2009/fall/cs301/support/x86_64/instructionsNZ.pdf)
- [Calling Conventions](https://en.wikipedia.org/wiki/X86_calling_conventions)
- [Linux System Call Table](http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)

**Call Stack**

- [Wikipedia](https://en.wikipedia.org/wiki/Call_stack)

## Utilities

**Docker**

- [Docker container configured for writing NASM x86 Assembly & C](https://github.com/kellyi/nasm-gcc-container)