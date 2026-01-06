---
title: "Part I: Introduction - Level Up as a Software Engineer by Writing a Chess Engine"
date: "2022-01-25"
draft: false
tags:
- chess engine
- software engineering
- guides
- programming
series:
- Level Up as a Software Engineer by Writing a Chess Engine
---

![](https://tiddlywiki-images-337530763245.s3.amazonaws.com/deep-blue.webp)

I’ve always learned better working on projects rather than reading theory. So, when I started to learn Golang I wanted to find a challenging project requiring a variety of software engineering concepts.

I ended up writing a chess engine and it turned out to be more challenging than I had anticipated. It also greatly improved my skill in applying important software engineering concepts. **I want to share the challenges that make chess programming such a great way to level up as a software engineer.**

The chess engine I built is named Glee, short for Golang Chess Engine.

* [Chess engine source code](https://github.com/tonyOreglia/glee)
* [Frontend source code](https://github.com/tonyOreglia/personal-website/tree/master/src/ChessGame)

The following aspects of chess programming will improve your software engineering skills.

# Computing Constraints

A chess engine's strength depends to some degree on its search depth. For example, Stockfish, a leading open-source chess engine, searches to a depth of 24 on average. Of course, the search tree is pruned so that not every move is analyzed, but to give you some idea of the scale here, let’s check the numbers. If Stockfish is only analyzing three moves per position that’s 3²⁴ position, i.e. 282,429,536,481 or 282 billion. How efficiently the chess engine can determine legal moves and evaluate positional advantage is critical to its strength. This poses a fun, worthwhile challenge for developers of any experience level.

# Algorithms

A given chess position has an average of 31 possible moves. Searching every position to a depth of 24 requires evaluating 6.2e+10³⁵ (or 620 decillion) positions. This is not possible to compute within the time bounds of a chess match. There are many clever search algorithms, pruning strategies, hashing methods, and move generation approaches to reduce the search space and increase efficiency.

Just as an example, the naive Minimax algorithm is effective in finding the optimal move given a search tree with each node evaluated. However, using an Alpha-beta pruning will reduce the number of nodes that need to be evaluated by ignoring branches that are worse than previously analyzed branches. In the best case, Alpha-beta can reduce the search size to the square root of the original search.

# Hash Tables

Understanding when and how to use hash tables is critical in software engineering. Writing a chess engine is a great opportunity to improve this skill. It’s obviously inefficient to evaluate a given position multiple times, however, as the game progresses the engine will of course have large parts of the current and previous search trees overlapping. Hash tables are a useful way to save time and resources by saving the resulting evaluation for a position.

# Links Lists

Data structures are central to computer science. A chess position and its “children” form a tree of connected possibilities. Building a data structure with efficient insertion, deletion and search is another critical piece of a competitive chess engine.

# Be a Part of Computing History

Kasparov played against IBM's Deep Blue chess engine in 1997. This became the first defeat of a world chess champion by a computer under tournament conditions. This is a symbolic moment in the advance of computing technology. Today Machine Learning and Artificial Intelligence are increasingly powerful and ubiquitous. It's a great experience to walk in the footsteps of those pioneers of computer science.

# Performance Testing and Constraints

> For engineers, designers and other creative problem-solvers, a formal definition of the constraints within which they must work is essential to channel energies and expand creativity.

^-\ Adam\ Morgan^

In my opinion, the most beneficial aspect of chess programming is that performance is a first-class citizen. Every performance improvement will benefit the engine’s chess rating. Constraints should be at the forefront of good engineering but with the ever-increasing compute, memory, and storage available to software engineers, constraints have become less and less important in most applications. This is sad because constraints are really at the heart of engineering, and creativity in general. I think of the inspiring story of NASA engineers puzzling over how to cram all the necessary Newtonian equations into 4KB of ram. Chess programming is a chance to bring constraints and performance concerns back to the forefront of your thinking.

![](https://tiddlywiki-images-337530763245.s3.amazonaws.com/nasa-code.webp)

I hope this overview has convinced you to continue exploring the world of chess programming. Perhaps you’ll even write your own engine. I am certain it’s worth the effort.

---

# Resources

* [Glee Chess Engine](https://github.com/tonyOreglia/glee)
* [Glee React UI](https://github.com/tonyOreglia/personal-website/tree/master/src/ChessGame)
* [Stockfish](https://stockfishchess.org/)
* [Discussion of possible games within the scope of average reasonable moves per turn here](https://www.chess.com/forum/view/fun-with-chess/total-number-of-reasonable-moves-per-turn#:~:text=We%20know%20that%20on%20average,in%20an%20average%20chess%20match)
* [Discussion of average legal moves per position here](https://chess.stackexchange.com/questions/23135/what-is-the-average-number-of-legal-moves-per-turn)
