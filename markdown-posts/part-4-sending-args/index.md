---
title: "Part IV: Sending Function Arguments and Receiving a Return Value"
draft: false
date: "2021-10-25"
series: 
- Writing an X86–64 Assembly Language Program
tags:
- software engineering
- assembly language
- docker
- guides and tutorials
- programming
---

This guide is part four of the series, [X86–64 Assembly Language Program](https://tonycodes.com/blog/series/writing-an-x8664-assembly-language-program/).

--- 

# Sending Function Arguments and Returning a Result

In the previous post of this series, we saw how to define and call functions in x86–64 Assembly.

Now I wanted to know how to provide arguments to a function and return values. In other words, when this is done in a higher-level language, how is it translated at the Assembly code level?

The answer is pretty straightforward. In x86–64 Assembly, there is a convention defining which registers should be used for the first argument, second argument, and so forth.


```
+-----------------+----------+
| Argument number | Register |
+-----------------+----------+
| Arg 1           | $ rdi    |
| Arg 2           | $ rsi    |
| Arg 3           | $ rdx    |
| Arg 4           | $ rcx    |
| Arg 5           | $ r8     |
| Arg 6           | $ r9     |
| Arg 7           | stack    |
+-----------------+----------+
```

All further arguments are pushed onto the stack.

Return values are expected to be stored in the register $rax.

Here is an example of code that utilizes the conventional registers to pass arguments and results in order to print out the command-line arguments

```nasm
section .data
section .text
    global _start
_start:
  call .getNumberOfArgs   ; expects return value in $rax
  mov rdi, rax
  call .printNumberOfArgs ; expects value to be in 1st argument, i.e. $rdi
  call .exit
.getNumberOfArgs:
  pop rbx         ; this is the address of the calling fxn. Remove it from the stack for a moment
  pop rax         ; get argc from stack
  push rbx        ; return address of calling fxn to stack
  ret
; expects value to be in 1st argument, i.e. $rdi
.printNumberOfArgs:
  pop rbx         ; this is the address of the calling fxn. Remove it from the stack for a moment
  add rdi, 48     ; convert number of args to ascii (only works if < 10)
  push rdi        ; push the ascii converted argc to stack
  mov rsi, rsp    ; store value of rsp, i.e. pointer to ascii argc to param2 of sys_write fxn
  mov rdx, 8      ; param3 of sys_write fxn is the number of bits to print
  push rbx        ; return the address of the calling fxn to top of stack.
  call .print
  ; clean up the number that was pushed onto the stack. Retaining the return address currently on top of stack
  pop rbx
  pop rcx
  push rbx
  ret
  
.print:           ; print expects the calling location to be at the top of the stack
  mov rax, 1
  mov rdi, 1
  syscall
  ret             ; return to location pointed to at top of stack
.exit:
  mov rax, 60
  mov rdi, 0
  syscall
```

There are some additional well-defined calling conventions that are helpful to follow. See [here](https://en.wikipedia.org/wiki/X86_calling_conventions).

I hope you enjoyed this article. To learn more, find the next part of this series here: Conditionals, Jumping, and Looping.
