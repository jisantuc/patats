---
title: Borrowing your favorite JavaScript libraries with PureScript
author: James Santucci
patat:
    wrap: true
    margins:
        left: 5
        right: 5
    slideLevel: 2
---

# Welcome #

## Two bad options ##

> - Option 1: JS / gradually TS and live with "things just break at runtime sometimes because frontend testing is **really hard**"
> - Option 2: Use a fancy fully typed compiles-to-JS buddy, stare with hostility at JavaScript every time you need it, and reimplement everything you need from scratch because **ecosystems**

## Why is breaking at runtime bad? ##

💰

## Why is reimplementing everything bad? ##

🙄

## What can we do? ##

> - **I will convince you that we can have strong safety, pleasant syntax, expansive FP facilities, and also the entire ecosystem of things published on npm without immense physical discomfort.**

. . .

- the simplest FFI imaginable
- why would we even want to do this
- a less trivial dive into `@turf/helpers`

# FFI - Crass Version #

# Why bother #

## Really why ##

- safety
- functional patterns
- improve on existing APIs

## Safety ##

> - don't you have other options for safety at this point? sure
> - cleaner separation than gradual TS if that's what you want, but TS is tbh _pretty good_

## Functional patterns ##

- do you really *need* `traverse`?
- maybe you don't even want these
- I want these, so for the duration of this presentation they're a Good Thing to Have™

## Better APIs ##

> - **this part rules**
> - Maybe you're also reading *A Philosophy of Software Design* (big ol' OOP tome btw) and want to "define errors out of existence"
> - Maybe you read Peter's *Modeling State with TypeScript* blog a while ago and want to "make those bad states unrepresentable" in some existing library
> - **you can!**
> - bonuses: way easier property testing, which makes boundaries easier to find

# FFI - Pretentious Mix #

## The problem ##

- STAC 10% time project: write a client that I can call from JS
- STAC: **Spatio**-temporal asset catalog
- spatial
- oh no

## Needed spatial types ##

- spatial types??? _special_ types

. . .

- my normal response to this problem:

😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱

😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱

😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱

😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱

😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱😱

## Can we solve this problem again live?? ##

ish.

yes, let's do it

# Links #

- Peter's blog: https://www.azavea.com/blog/2019/12/12/modeling-state-with-typescript/
- A Philosophy of Software Design: https://www.amazon.com/Philosophy-Software-Design-John-Ousterhout/dp/1732102201
- Do you really need traverse? https://impurepics.com/fp-bot/ 🐱
