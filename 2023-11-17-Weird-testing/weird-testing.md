---
title: Weird testing
author: James Santucci
patat:

    wrap: true
    margins:
        left: 40
        right: 40
    images:
      backend: auto
---

# Weird testing

## Weird testing

* lots of testing is pretty standard
* unit tests, integration tests, end-to-end tests
* mostly it all works the same

. . .

* all boils down to -- does this unit work? does this unit work with that unit? does these three units all work with these three units?

## Standard "kinds of testing"

![](assets/testPyramid.jpg)

## Weird testing

* is scale the only question to ask?

. . .

> * do I even care about my tests' behaviors or do I just kinda know what output should look like?
> * are my tests sensitive to the input values I've chosen?
> * do my tests test what I say they test?

# Do I even care about what happens in this test?

## ⭐️ golden testing ⭐️

* sometimes tests really care about _what happens_
* other times tests only care about _not breaking things_
* "I shouldn't get anything different from before" -> *golden testing*

## ⭐️ golden testing ⭐️

* examples:

    > * serialization result shouldn't change even though we changed json libraries
    > * refactored code in some complex workflow -> think we should get the same result as we did before

. . .

* this is really useful when you don't really know what "behavior" means, so wire formats / black box refactors are more obvious candidates

## ⭐️ `pytest-golden` ⭐️

* enable by installing `pytest-golden`
* use in a test by using `pytest.mark.golden(path)` with a path to a special yaml file

## ⭐️ `pytest-golden` ⭐️
* demo time

## ⭐️ `pytest-golden` ⭐️

* where could we use it?

# Are my tests sensitive to the input values I've chosen?

## 🧪 property-based testing

* normal: you have expectations like "for **all** values of type `T`, some **property** should hold"; but then you pick two `T`s and say "yeah that's probably good"
* properties can be lots of things:
 
    > * the program shouldn't crash
    > * I should recover the original input
    > * the output should be smaller than the input
    > * the mean of the output should be within x of 2.8

. . .

* in python, `hypothesis`

## 🧪 `hypothesis`

* demo time

## 🧪 property-based testing

* where could we use it?
* it's already a transitive dep in a lot of places that I have cloned so we could use it lots of places
* `grep` your `poetry.lock` files to see if you already have it!

## 🧪 property-based testing

* where could we use it?
* `pg-pydantic` could provide some property tests enforcing semantics of `PGPydantic` model beyond "yeah man this talks to the database"
 
## 🧪 property-based testing

* where could we use it?
* `mentat-feasibility` could have expectations like:
 
    * given some `Access`, you can't schedule it twice
    * given some "presumed good" `Access` and an empty schedule, attempting to schedule the target spec puts it on the schedule

## 🧪 property-based testing

* where could we use it?
* probably you have some rules in your head for services you work on that would make decent properties

# Are my tests *good* tests?

## ❌ 👨 mutation testing ❌ 👨

> * I didn't have a good emoji for mutants, so you got an x and a man kinda
> * "sure some test passes / fails with the actual function I wrote, but what about with a similar but slightly different function?"
> * would be really tedious to test this on your own, but fortunately, _libraries_ and _tools_

## ❌ 👨 mutation testing ❌ 👨

* I tried out a few libraries here -- `pytest-mutagen` and `mutatest` weren't really doing much and have pretty old pytest version requirements
* I landed on `mutmut` (mute mute? mutt mutt? moot moot?), since:
        > * it's not obviously broken
        > * it has nice emojis for output

## ❌ 👨 `mutmut` ❌ 👨

* demo time

## ❌ 👨 mutation testing ❌ 👨

* where could we use it?
* anywhere we have god tests of large functions, we'll probably miss some mutants

# THE END
