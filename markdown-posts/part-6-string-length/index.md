---
title: "Part VI: How to Determine String Length"
draft: false
date: "2021-11-28"
series: 
- Writing an X86–64 Assembly Language Program
tags:
- software engineering
- assembly language
- docker
- guides and tutorials
- programming
---

![](https://img.tonycodes.com/scrabble.webp)

This guide is part six of the series, [X86–64 Assembly Language Program](https://tonycodes.com/blog/series/writing-an-x8664-assembly-language-program/).

---

# How to Calculate String Length

In order to calculate the length of a string, we’ll first need to know what determines the end of a given string.

Strings in memory are represented as a pointer. The location pointed at is a byte of data representing a character followed by additional characters contiguous in memory. The important point is that this sequence of bytes is terminated by the byte 0x00. This is called the zero-termination character which is one method of terminating a string (C uses this approach, for example). There are methods of encoding strings that we won’t cover here.

For example, the string “HELLO WORLD!” would hold the following values in memory (binary values represented in hexadecimal):


```
+------+------+------+------+------+---------+------+------+------+------+------+------+----------------------------+
|  H   |  E   |  L   |  L   |  O   | <space> |  W   |  O   |  R   |  L   |  D   |  !   | zero-termination character |
+------+------+------+------+------+---------+------+------+------+------+------+------+----------------------------+
| 0X48 | 0X45 | 0X4C | 0X4C | 0X4F | 0X20    | 0X57 | 0X4F | 0X52 | 0X4C | 0X44 | 0X21 | 0x00                       |
+------+------+------+------+------+---------+------+------+------+------+------+------+----------------------------+
```

So the length can be determined by looping through each byte of memory in a string until the zero-termination character is reached. Here is an initial implementation of how this may be implemented, but if you look closely there are a couple of bugs, see if you can identify the issues with this code snippet.

```nasm
; expects * char array in $rdi
.strlen:
  mov rax, 1              ; initialize strlen counter
.loop:
  add rdi, 1              ; increment char * to next character
  add rax, 1              ; increment strlen counter
  cmp byte [rdi], 0x00    ; if value at [rdi] is 0x00 return
  jne .loop               ; loop if not at end of string
  ret
```

If you found the issues, great job. If you just want to learn, read on. The problem is that [rdi] could point at an empty string, so the character in which case the character at [rdi] is 0x00. This is a classic example of not taking corner cases into consideration when writing a solution.

```nasm
.strlen:
  mov rax, 1             ; initialize strlen counter
```

Now `[rax] = 1`, even though the string’s length is 0.

```nasm
.loop:
  add rdi, 1              ; increment char * to next character
```

Now the program is pointing past the first character in the string in memory.

```nasm
  add rax, 1              ; increment strlen counter
```

Now, `[rax]` could equal 2, even though the string length is 0.

```nasm
  cmp byte [rdi], 0x00    ; if value at [rdi] is 0x00 return
```

The byte at `[rdi]` is not `0x00` because the program walked right past that byte. When will this loop end? The program does not know, because it’s looking at the memory it’s not supposed to.

The second bug is that the final value is too long by one. The length does not need to include the terminating null character.

A revised version of the solution could look like this

```nasm
.strlen:
    mov rax, 0              ; initialize strlen counter
    cmp byte [rdi], 0x00    ; if value at [rdi] is 0x00 return
    jne .loop               ; loop if not at end of string
    ret
.loop:
    add rdi, 1              ; increment char * to next character
    add rax, 1              ; increment strlen counter
    cmp byte [rdi], 0x00    ; if value at [rdi] is 0x00 return
    jne .loop               ; loop if not at end of string
    ret
```

Of course, there is a bit of repeated code. Perhaps you can optimize this solution to avoid duplication. If you do, let people know in the comments!