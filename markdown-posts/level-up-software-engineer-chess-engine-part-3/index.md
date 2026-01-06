---
title: "Part III: Move Generation - Level Up as a Software Engineer by Writing a Chess Engine"
date: "2022-02-12"
draft: false
tags:
- chess engine
- software engineering
- guides
- programming
- algorithms
series:
- Level Up as a Software Engineer by Writing a Chess Engine
---

![](https://tiddlywiki-images-337530763245.s3.amazonaws.com/Ludwig-Zagler.webp)

**How does a computer think? It must know two things: what is possible and what is optimal.**

A chess move generation function calculates what is possible from a given position. An evaluation function determines what is optimal. **Move generation is the marriage of these two capabilities and the focus of this article**.

---

A note about the evaluation function
No computer can “see” to the end of a chess game but the engine still needs to find advantageous positions. This is why an evaluation function is necessary to score the approximate advantage of a position.

Evaluation typically uses a point system with pawns worth 100 and the following relative values:

```
pawn:    100
knight:  300
bishop:  320
queen:   900
king:    99999
```

The evaluation function also considers positional advantages. My engine’s evaluation function is simple, you can find it [here](https://github.com/tonyOreglia/glee/blob/master/pkg/evaluate/evaluate.go).

For the purpose of this article, imagine a simple evaluation that just adds up the scores of each piece and ignores positional advantage. Given this evaluation approach and a move generation function, how would you go about selecting the best move?

# Naive solution

The naive approach would be to evaluate each move and choose the best scoring one.

This approach has severe problems. For example, consider the following position with black to move

![](https://tiddlywiki-images-337530763245.s3.amazonaws.com/board-3.webp)

Of all the possible moves, the highest score is after the black queen captures the pawn. Using the evaluation mentioned above, taking the pawn would score negative 400 (negative scores being advantageous for black).

But clearly, this is a bad move! White will respond by capturing the black queen scoring 500 in white’s favor.

**Just like a human player, the chess engine needs to look beyond just a single move to play well**.

# Better — Minimax

Imagine the engine looks three [plies](https://www.chessprogramming.org/Ply) ahead.

![](https://tiddlywiki-images-337530763245.s3.amazonaws.com/minimax.webp)

Two-ply search
This poses an interesting problem. The engine cannot simply choose the move with the best outcome because the opponent has an opportunity to eliminate the best outcome. The engine must assume the opponent will play rationally. Its job is to limit the opponent's options while maximizing its own. **The minimax algorithm aims to do exactly this**.

This story helped me to conceptualize minimax. Imagine playing a game with an enemy you hate. Two open boxes are between you with a bunch of items inside. You have to give your opponent one of the boxes. They will then select one item from the box to give you. Of course, the opponent will choose the worst possible item. To maximize the value you receive, you have to eliminate the box which contains the worst of all items.

For example, if one box contains a pile of dog poop and the worst item in the other box is a paperclip, you should choose the box with the paperclip.

This scenario resembles a two-ply search. But the strategy also applies to deeper searches.

Here is the pseudo-code example of a min-max function of arbitrary depth (from [chess programming wiki](https://www.chessprogramming.org/Main_Page)):

```cpp
// depth is the intended number of moves to search
int miniMax( int depth ) {
    // evaluate scores the poition
    if ( depth == 0 ) return evaluate();
    int max = -oo;
    // all moves would be calculed by a move generation function
    for ( all moves)  {
        // call function recursively until intended depth is reached
        score = -miniMax( depth - 1 );
        if( score > max )
            max = score;
    }
    return max;
}
```

~minimax\ search\ pseudo-code~

This function is called for each move from a given position and the highest-scoring move is selected. Minimax requires a positive score for one side's advantage and a negative score for the opponent.

# Better — Alpha-beta pruning

Minimax is inefficient.

To understand why, imagine the two boxes again. Now imagine you looked into the first box the worst thing is a bag of money (**great!**). Now imagine the first thing you see in the second box is a lunch invitation from your in-laws (**ouch!!**). The opponent will definitely give you the invitation. You can stop checking the second box and just choose the first box.

**This is an optimization**. Alpha-beta pruning does this. Essentially, alpha-beta will ignore moves that are guaranteed to be worse than a previously analyzed move.

Here’s some pseudo-code of an alpha-beta pruning function (from chess programming wiki):

```cpp
int alphaBeta( int alpha, int beta, int depthleft ) {
   if( depthleft == 0 ) return evaluate();
   for ( all moves)  {
      score = -alphaBeta( -beta, -alpha, depthleft - 1 );
      if( score >= beta )
         return beta;   //  fail hard beta-cutoff
      if( score > alpha )
         alpha = score; // alpha acts like max in MiniMax
   }
   return alpha;
}
```

# Optimizations

The possible optimizations and improvements are endless. I will mention a few and provide links for the interested to dig in.

## Hash Algorithms

Hash tables can be used to eliminate duplication of work. For example, part of the move tree will overlap with the previous searches. If you can hash the position (efficient to do with bitboards) and store information about the outcome then time can be saved in upcoming searches.

## Quiescence Search or Selective Deepening

The engine’s depth horizon is problematic. If the engine is looking six moves ahead, but the seventh move is a queen capture, this can be a critical blind spot. Humans notice this naturally. For an engine, a quiescence search solves this. The quiescence search goes deeper in certain circumstances. The idea is to only evaluate “quiet” positions (where there is no imminent capture or tactic) but to search deeper in dynamic positions.

## Iterative Deepening

Complexity varies throughout the game. During the end game, there might be two legal moves. In the middle game, there can be thirty moves. The engine will be able to search deeper as the position simplifies. Therefore, the search depth should vary throughout the game.

Iterative deepening starts at a low depth search and iteratively increases the depth until some time limit is reached. The may sound inefficient but the low-depth calculations are rapid (the increase in time per ply is exponential). Generally, this optimizes the depth searched for a given time window. It is useful in cases where time is running low and the engine needs to decide quickly.

# Training a computer to think

I hope this article has piqued your interest in chess programming and programming machines to think. Even in the age of machine learning (ML), a machine must be shown **what is possible and what is optimal**. For example, training an ML algorithm requires a data set for feedback to adjust the “neurons” and increase accuracy. Even AlphaGo was given the rules (what’s possible) to then teach itself what’s optimal.

---

My chess engine is named Glee, a shortening of **Golang Chess Engine**.

* [Chess engine source code](https://github.com/tonyOreglia/glee)
* [Frontend source code](https://github.com/tonyOreglia/personal-website/tree/master/src/ChessGame)

---

# Resources

* [Iterative Deepening](https://www.chessprogramming.org/Iterative_Deepening)
* [Alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
* [Minimax](https://en.wikipedia.org/wiki/Minimax)
* [Selective Deepening](https://www.chessprogramming.org/Selectivity)
* [Quiescence Search](https://www.chessprogramming.org/Quiescence_Search)
* [Using Hash Tables](https://www.chessprogramming.org/Hash_Table)
* [Game Search Tree](https://www.chessprogramming.org/Search_Tree)
* [Ply](https://www.chessprogramming.org/Ply)
