---
title: The Great Replacement
date: '2026-01-26'
draft: true
tags:
- LLM
- productivity
- coding
---

# Karpathy Notes 

There have been a few predictions that one effect of AI on the software industry will be to cut away some of the proliferation of micro-apps.

In the business context this was predicted by the All In Podcast. 

In the B2C space this has been predicted multiple times on hacker news. 

I tend to agree with the sentiment, and here's an example where I've used AI to generated a micro-app for a specific functionality I wanted. 


I really like this tweet from Andrew Karpathy regarding the single note strategy. I started using it and it's great. But there were a few things bothering times

1. Slightly annoying to move the cursor to the top of the note, add the date, enter enter and now you can enter your notes for the day. In other words, appending to the top is not the expected behavior for most apps. So I wanted to make append to the top the default mechanism
2. Grouping by tag -- of course you can search by tag or keyword and this is easy with a single text file. But I love some of the functionality you get with tiddlywiki for example. So I started writing some scripts that dynamically curate a note based on some tag. This is very fast to do with LLM support. 

So I used Claude Code to write a light html/css/js wrapper around my notes.md file. You can find the result here: github.com 


Here is screenshot: 




