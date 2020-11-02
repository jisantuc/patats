---
title: Property testing
author: James Santucci
patat:
    wrap: true
    margins:
        left: 40
        right: 40
---

# What's testing #

> - programs that verify some expected behavior occurs under known conditions

# Programs that verify

- is this a test?

```python
from .lib import foo

def test_foo():
    result = foo(3, 4)
    assert(result == 7)
```

> - I would say _no_

# Programs that verify

- is this a test?

```python
from .lib import foo

def test_foo():
    result = foo(3, 4)
    assert(result == 7)
```

```bash
$ python -m pytest
```

> - what are this test program's requirements?

# Programs that verify

- is this a test?

```python
from .lib import foo

def should_work():
    result = foo(3, 4)
    assert(result == 7)

if __name__ == '__main__':
    should_work()
```

```bash
$ python thing_that_should_work.py
```

# This talk

> - tests are programs that verify your expectations when you run them
> - property testing can save you from having to state your expectations separately about a lot of similar cases
> - you can property test _anywhere_

# A function #

```haskell
add :: Int -> Int -> Int
add x y = x + y
```

# Unit testing #

> - expectations come from examples we care about
> - we really need to know that adding 3 and 4 yields 7
> - `add 3 4 == 7`

# Property-based testing #

> - expectations come from "properties"
> - suppose `add` is actually complicated, but we have some other function that calculates a result we know is good
> - that other function we'll call `sum`
> - expectations come from equivalence relations that we think ought to be true for any values that satisfy our function

```haskell
test :: int -> int -> TestResult
test x y = add x y == sum x y
```

# Property-based testing #

> - but we've just kicked the can -- where do equivalence relations come from?
> - sometimes we have expectations about a function like add
> - sometimes we have expectations about all things that share a property

# Laws-based testing #

> - for when we have expectations about all things that share a property
> - back to add:

```haskell
combine :: (int -> int -> int) -> int -> int -> int
combine f x y = f x y

add :: int -> int -> int
add = combine (+)
```

> - but also!

```haskell
multiply :: int -> int -> int
multiply = combine (*)
```

# Laws-based testing #

> - Things that share this behavior are `semigroups`
> - Semigroups are things with a _binary associative operator_
> - All things that form semigroups have the associativity property for their binary associative operator

```haskell
(x `combine` y) `combine` z == x `combine` (y `combine` z)
```

> - so that's a law, and we can have tests like:

```haskell
associativityTest :: Semigroup a => a -> a -> a -> TestResult
associativityTest x y z = (x `combine` y) `combine` z == x `combine` (y `combine` z)
```

# Where do laws come from #

- for semigroups, math
- for json serialization / deserialization in circe, consensus of open source contributors doing their best to write good software that won't break in surprising ways and will protect people from bad impulses (like throwing errors in deserialization)

# How do we test laws #

- in Scala, with the `Discipline` library and trait
- e.g. in [Raster Foundry](https://github.com/raster-foundry/raster-foundry/blob/develop/app-backend/datamodel/src/test/scala/ScopeSpec.scala)

```scala
class ScopeSpec
  extends Discipline {
  ...
  checkAll("Scope.MonoidLaws", MonoidTests[Scope].monoid)
  checkAll("Scope.CodecTests", CodecTests[Scope].codec)
}
```
