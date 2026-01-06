---
title: "Part II: Data Structures - Level Up as a Software Engineer by Writing a Chess Engine"
date: "2022-02-04"
draft: false
tags:
- chess engine
- software engineering
- guides
- programming
- data structures
series:
- Level Up as a Software Engineer by Writing a Chess Engine
---

![](https://tiddlywiki-images-337530763245.s3.amazonaws.com/kasparov.webp)

Internal board representation is a good place to start if you are building a chess engine. In other words, how will the program represent a chess position? Resolving this question correctly requires thinking through the entire solution before going to the keyboard.

# Naive Approach

The naive approach is to simply look at the board and come up with a structure that can encode the information. For example, you might use an array of length 64, encoding the pieces as single characters.

Not surprisingly, this solution encounters some limitations. For example, when the program needs to generate legal moves. To illustrate this, imagine a position with just one king and one rook of each color.

![](https://tiddlywiki-images-337530763245.s3.amazonaws.com/board-1.webp)

Chess Position
To provide a visualization that is closer to the internal board representation, the position could be represented as:

```bash
8| - k - - - - - - |
7| - r - - - - - - | 
6| - - - - - - - - |
5| - - - - - - - - |
4| - - - - - - - - |
3| - - - - - - - - | 
2| R - - - - - - - | 
1| K - - - - - - - | 
   a b c d e f g h
```

Now imagine the legal moves for the white rook, sliding to the right. Given the position, the engine must check each index for legality. This is simple at first as one is added index and the location is checked for an enemy or friendly piece. The first two legal positions for white would look like the following as the rook slides to the right:

```
8| - k - - - - - - |
7| - r - - - - - - | 
6| - - - - - - - - |
5| - - - - - - - - |
4| - - - - - - - - |
3| - - - - - - - - | 
2| - R - - - - - - | 
1| K - - - - - - - | 
   a b c d e f g h
   
8| - k - - - - - - |
7| - r - - - - - - | 
6| - - - - - - - - |
5| - - - - - - - - |
4| - - - - - - - - |
3| - - - - - - - - | 
2| - - R - - - - - | 
1| K - - - - - - - | 
   a b c d e f g h
```

However, eventually, the rook will reach the edge of the board. It’s not obvious from the index that this has occurred as the board representation is just a single array of length 64.

```
8| - k - - - - - - |
7| - r - - - - - - | 
6| - - - - - - - - |
5| - - - - - - - - |
4| - - - - - - - - |
3| R - - - - - - - | 
2| - - - - - - - - | 
1| K - - - - - - - | 
   a b c d e f g h
```

To avoid this, the chess engine must check that the index is not on the A-file or H-file depending on the direction of movement. Consider how to programmatically check this condition:

```cpp
bool isOffBoard(bool directionIsRight, short index) {
  if (directionIsRight) {
    return !(index % 8 == 0);
  }
  // piece is moving left from white side 
  // so check the h-file
  return (index % 8 == 7)
}
```

This is a branching condition dependent on integer comparison, which is a slow operation. Unfortunately, it is necessary for every single horizontal move. For a chess engine dealing with millions of positions per second, this is a big efficiency drain. If you are not familiar with the performance implications of integer comparison and branching, this article on CPU pipeline architecture provides context as to why branches slow down execution. Essentially, the CPU cannot make accurate time-saving assumptions beyond a conditional branch so parallelization is greatly reduced.

Note that kings, pawn attacks, and every other piece must also include this check for horizontal moves. Knights are even worse, the B and G files must also be checked since a knight can jump two files horizontally.

# An Improvement

Luckily, there is a clever method of mitigating this issue with a solution dubbed 0x88 (you’ll see why). By representing the board as a 128 length array, there is a clever way to efficiently identify off-board indexes. Image the 128 index array as two chess boards side by side:

```text
8| - - - - - - - - | - - - - - - - - |
7| - - - - - - - - | - - - - - - - - |
6| - - - - - - - - | - - - - - - - - |
5| - - - - - - - - | - - - - - - - - |
4| - - - - - - - - | - - - - - - - - |
3| - - - - - - - - | - - - - - - - - |
2| - - - - - - - - | - - - - - - - - |
1| - - - - - - - - | - - - - - - - - |
   a b c d e f g h   a b c d e f g h
```

It's not obvious, but this board representation simplifies the off-board check by enabling the use of bitwise operations instead of comparisons. For example, consider the off-board calculation (I’ll explain why this works):

```cpp
bool isOffBoard(short index) {
  return (square && 0x88 != 0);
}
```

This single bitwise operation requires fewer CPU clock cycles than integer comparisons. To understand why this comparison works, let’s look at our representation again but this time with each index printed out in binary. I’ve put the boards on top of each other in order to be within the viewing window.

```
// Left side board
8| 00000000 00000001 00000010 00000011 00000100 00000101 00000110 00000111 |
7| 00010000 00010001 00010010 00010011 00010100 00010101 00010110 00010111 | 
6| 00100000 00100001 00100010 00100011 00100100 00100101 00100110 00100111 | 
5| 00110000 00110001 00110010 00110011 00110100 00110101 00110110 00110111 | 
4| 01000000 01000001 01000010 01000011 01000100 01000101 01000110 01000111 | 
3| 01010000 01010001 01010010 01010011 01010100 01010101 01010110 01010111 | 
2| 01100000 01100001 01100010 01100011 01100100 01100101 01100110 01100111 | 
1| 01110000 01110001 01110010 01110011 01110100 01110101 01110110 01110111 | 

// right side board
8| 00001000 00001001 00001010 00001011 00001100 00001101 00001110 00001111 |
7| 00011000 00011001 00011010 00011011 00011100 00011101 00011110 00011111 |
6| 00101000 00101001 00101010 00101011 00101100 00101101 00101110 00101111 |
5| 00111000 00111001 00111010 00111011 00111100 00111101 00111110 00111111 |
4| 01001000 01001001 01001010 01001011 01001100 01001101 01001110 01001111 |
3| 01011000 01011001 01011010 01011011 01011100 01011101 01011110 01011111 |
2| 01101000 01101001 01101010 01101011 01101100 01101101 01101110 01101111 |
1| 01111000 01111001 01111010 01111011 01111100 01111101 01111110 01111111 |
```

Now, it is easier to see that using `0x88` (`0b10001000`) as a mask, always results in a positive value on the real board and a zero value if the piece has left the edge of the board.

Here are a few example bitwise `&` operations to drive the point home. Three random indexes from on the real board:

```text
00000000
10001000
--------
00000000

01010011
10001000
--------
00000000

01110111
10001000
--------
00000000
```

and three from the right side validation board:

```text
00001000
10001000
--------
00001000

01001010
10001000
--------
00001000

01111111
10001000
--------
00001000
```

As you can see the bitwise `&` with hexadecimal `0x88` can quickly indicate whether a move goes off the edge of the board. This is a big efficiency gain for the chess program!

# Bitboards

Keeping in mind the efficiency of bitwise operations, there is an even better approach than `0x88`.

Taking advantage of the 64-bit registers in modern CPUs (there are 64 possible locations on a chessboard), a position can be represented with a group of 64-bit integers. The approach is called bitboards. In this approach, each bit of an integer represents a single square on the chessboard.

With bitboards, efficient bitwise operations can be used to calculate legal moves. Let's take an example of finding the moves for a bishop in the corner of the board, with a single enemy piece in its path:

![](https://tiddlywiki-images-337530763245.s3.amazonaws.com/board-2.webp)

As two relevant bitboards might look like the following:

```cpp
const uint64_t white_bishop_bb = 0x8000000000000000;
/** 
10000000
00000000
00000000
00000000
00000000
00000000
00000000
00000000
*/ 

const uint64_t black_knight_bb = 0x40000;
/** 
00000000
00000000
00000000
00000000
00000000
00000100
00000000
00000000
*/
```

A usual approach with bitboards is to have a precalculated lookup table for sliding moves in all directions from every index. Check out my Golang utility for calculating these hashtables [here](https://github.com/tonyOreglia/glee/blob/master/pkg/hashtables/generate-hash-tables.go). The one utilized in this case would be

```cpp
uint64_t south_east_array_bitboard_lookup[64];
south_east_array_bitboard_lookup[0] = 0x40201008040201; 
/** 
00000000
01000000
00100000
00010000
00001000
00000100
00000010
00000001
*/
```

With this information at hand, calculating the available bishop moves becomes a series of bitwise operations

```cpp
uint64_t GenerateValidMovesSouthEastBitboard(char index) {
    uint64_t bb_occupied_squares_overlap_with_southeast_array = 
        black_knight_bb & south_east_array_bitboard_lookup[0][index];
    
    if(bb_occupied_squares_overlap_with_southeast_array) {
        char least_significant_bit = lsb_scan(bb_occupied_squares_overlap_with_southeast_array);
        return (south_east_array_bitboard_lookup[index] ^
            south_east_array_bitboard_lookup[least_significant_bit]);
    }
    return south_east_array_bitboard_lookup[index];
}
```

This is much more complex, but remember the most important measure for a chess engine is speed. There is a least significant-bit scan (which can be done optimally with processor instructions). The result is a bitboard representing the legal moves for the bishop. Utilizing this approach for all four diagonal directions (all eight in the case of the queen) the chess program can calculate moves much more efficiently than the previous two board representations.

[Chess Programming Wiki](https://www.chessprogramming.org/Bitboards) is a great resource to learn more about bitboards, and chess programming in general.

# Thinking with the end in mind

The lesson is applicable to any software engineering project. **Always consider the use case in detail when designing an information architecture**. That rule applies to implementing internal data structures, database table relationships, website layout, and anything else. The primary consideration when choosing how to represent any data is how that data is meant to be used. **As engineers, we must always think with the end in mind**.

---

My chess engine is named Glee, a shortening of **Golang Chess Engine**.

* [Chess engine source code](https://github.com/tonyOreglia/glee)
* [Frontend source code](https://github.com/tonyOreglia/personal-website/tree/master/src/ChessGame)

I hope this article has been interesting and insightful!
