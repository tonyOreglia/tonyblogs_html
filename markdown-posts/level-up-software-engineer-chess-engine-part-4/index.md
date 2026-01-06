---
title: "Part IV: Testing - Level Up as a Software Engineer by Writing a Chess Engine"
date: "2022-02-20"
draft: false
tags:
- chess engine
- software engineering
- guides
- programming
- testing
series:
- Level Up as a Software Engineer by Writing a Chess Engine
---

![](https://tiddlywiki-images-337530763245.s3.amazonaws.com/road-runner.webp)

**Healthy software requires testing**. Today, testing is inseparable from the development cycle because it improves reliability and eases refactoring which speeds up features development. **This article covers common testing strategies used in chess engine development**. These strategies follow tech industry best practices and can be applied to any software project.

# Component Testing

A chess engine requires a move generation function to calculate legal moves. This is a foundational component of the chess engine’s overall quality.

Since chess is deterministic, the exact number of legal moves from a position is known. **One common way to test move generation is by counting all possible moves from tricky positions and checking if the count is correct**. This approach is referred to as move path enumeration or sometimes “perft” testing.

For example, there are 48 legal moves for white from the following position:

![](https://tiddlywiki-images-337530763245.s3.amazonaws.com/board-4.webp)

~r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R\ w\ KQkq\ -~

If you go on to check every legal move from all 48 resulting positions, you will find 2,039 legal moves. These are called leaf nodes of the move tree. This image helps visualize what I mean by leaf nodes:

![](https://tiddlywiki-images-337530763245.s3.amazonaws.com/minimax.webp)

~Leaf\ Nodes\ at\ the\ bottom\ of\ the\ tree~

Each leaf node is not necessarily a unique position. However, the ordered combination of moves leading to the end positions is unique. Extending to six moves, there are exactly 88,031,647,685 leaf nodes from the position shown above.

If an engine can match the expected leaf node count for difficult positions, it's unlikely to have bugs in the move generation function. With this type of testing in place, you can confidently update the engine's move generation code.

Some helpful public databases for this type of testing exist. For example, my chess engine's move path enumeration tests are [here](https://github.com/tonyOreglia/glee/blob/19ec9959911ab9a045a9d40e7548fd0f8dd4b6e9/pkg/engine/engine_test.go).

Read more about component testing [here](https://martinfowler.com/bliki/ComponentTest.html).

# A Note on Test Driven Development

Testing for bugs can start before you have working software. In fact, using Test Driven Development (TDD) the idea is to write the expected functionality into tests and only then develop the software that enables the tests to pass. This is a great strategy and comes with the added benefit of starting with defined behavior enforced with tests.

I do recommend building the move path enumeration tests before implementing move generation. This will provide constant feedback as you work.

Read more about TDD [here](https://martinfowler.com/bliki/TestDrivenDevelopment.html).

# Performance Test

This type of testing has another advantage. By monitoring the speed of move enumeration you can have a good idea of the move generation performance.

Note that, this type of testing necessarily bypasses any optimizations like alpha-beta pruning and hashing. That’s because the test criteria rely on the entire move tree. Therefore, any optimization that trims part of the move tree will break these tests. That is why it is essentially a component test, it does not cover all aspects of the chess engine. So additional performance testing should be used to see how efficiently the engine is refining the search space.

# Broad-Stack Test

Improvements to the search and position evaluation function require we have some tests to evaluate how well the chess engine is playing. For some engines that don’t incorporate a user interface, this level of testing is essentially End to End. If the engine is integrating with a certain protocol or UI, then this is more of a broad-stack test. This is essentially the engine's end-to-end testing. It takes into account all aspects of the move generation, search, and evaluation methods. See Martin Fowler’s [testing guide](https://martinfowler.com/testing/) for more information on these categories of testing.

Similar to **move path enumeration** testing, there are resources online with test positions and the corresponding best move. For example, the [Bratko-Kopec test](https://www.chessprogramming.org/Bratko-Kopec_Test) is a respected test suite in use for over forty years.

Read about the general approach to broad-stack testing [here](https://martinfowler.com/bliki/BroadStackTest.html).

# Unit Testing

Unit Testing is another chance to practice test-driven development (TDD).

Say you are using a bitboard for the chess engine position representation. It is useful to have an interface that implements common bitboard mechanisms like Least Significant Bit calculation, for example. Here is a perfect opportunity to use TDD to define the exact outcomes of the interface methods before implementing the actual method.

As an example, some tests written for my chess engine's bitboard interface are [here](https://github.com/tonyOreglia/glee/blob/master/pkg/bitboard/bitboard_test.go).

Although these lower-level methods should not change often, you may find yourself turning them if one is a performance bottleneck. Then it's helpful to have a test covering the expected behavior.

> Quality is never an accident; it is always the result of intelligent effort

~—\ John\ Ruskin~

Testing is critical. Writing a chess engine is a great opportunity to sharpen these skills. If you decide to take on this challenge and write your own engine, let me know in the comments!

I hope you've found this article helpful!

# Resources

* [Performance Testing (perft), move path enumeration](https://www.chessprogramming.org/Perft)
* [Bratko-Kopec Test](https://www.chessprogramming.org/Bratko-Kopec_Test)
* [Martin Fowler Testing Guide](https://martinfowler.com/testing/)
* [Component Testing](https://martinfowler.com/bliki/ComponentTest.html)
* [BroadStack Test](https://martinfowler.com/bliki/BroadStackTest.html)
* [Test Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
* [FEN Notation](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
* [Extreme Programming](https://martinfowler.com/bliki/ExtremeProgramming.html)
