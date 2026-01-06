---
title: "Part V: Conditionals, Jumping, and Looping"
draft: false
date: "2021-11-01"
series: 
- Writing an X86–64 Assembly Language Program
tags:
- software engineering
- assembly language
- docker
- guides and tutorials
- programming
---

![](fun-ride.webp)

This guide is part five of the series, [X86–64 Assembly Language Program](https://tonycodes.com/blog/series/writing-an-x8664-assembly-language-program/).

---

# Conditionals and Looping
Assembly language supports conditionally jumping to a specific line of the code. Looping is actually just a special implementation of jumping. It’s a jump to the beginning of the “loop” until some condition is finally met.

Essentially this post is about writing conditional statements to branch one of two ways depending on some condition.

The core conditional operator is cmp which is short for ‘compare’. The cmp operator compares two values and then sets some flags indicating the relation of the two values. Flags can be checked using some other operators, namely:

- `JE` means to jump if equal
- `JZ` means to jump if zero
- `JNE` means to jump if not equal
- `JNZ` means to jump if not zero
- `JG` means to jump if the first operand is greater than second
- `JGE` means to jump if the first operand is greater or equal to second
- `JA` is the same as JG, but performs an unsigned comparison
- `JAE` is the same as JGE, but performs an unsigned comparison

To loop, a function simply calls itself based on the outcome of a conditional statement. Of course, at some point, the condition must break the loop to avoid an infinite cycle.

Here is an example demonstrating a looping function used to print a list of arguments from the stacks

```nasm
.printAllArgs:
  call .printNewline   ; fxn prints newline
  pop r11              ; pop address of the calling fxn. Remove temporarily
  mov rsi, [rsp]       ; stack pointer memory address. Holding argument to print. 
  mov rdx, 8           ; how long is the message. TO DO: calculate argument length
  push r11             ; push return address back onto the stack
  call .print
  pop r11              ; pop return address
  pop rcx              ; this is the already printed arg
  push r11             ; push return address back onto the stack
  sub rbx, 1           ; rbx is the argument count. Iterate down 1
  cmp rbx, 0           ; are there zero args left to print? 
  jne .printAllArgs    ; if more args to print, loop again
  call .printNewline   ; otherwise print Newline and return
  ret
```