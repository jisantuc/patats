---
title: Property testing
author: James Santucci
patat:

    wrap: true
    margins:
        left: 40
        right: 40

---

# Welcome #

> - [Matt Bachmann on Hypothesis](https://www.youtube.com/watch?v=jvwfDdgg93E)
> - [Old RF ADR on testing](https://github.com/raster-foundry/raster-foundry/blob/develop/docs/architecture/adr-0015-refactor-testing.md#3-property-based-testing)

# This talk #

> - tests are programs that verify your expectations about other programs
> - property testing can save you from having to state your expectations separately about a lot of similar cases
> - you can property test _anywhere_

# What's testing #

> - programs that verify some expected behavior occurs under known conditions

# Programs that verify #

* is this a test?

``` python
from .lib import foo

def test_foo():
    result = foo(3, 4)
    assert result == 7
```

# Programs that verify #

* is this a test?

``` python
from .lib import foo

def test_foo():
    result = foo(3, 4)
    assert result == 7, "oh no"
```

``` bash
$ python -m pytest
```

# Programs that verify #

* is this a test?

``` python
from .lib import foo

def should_work():
    result = foo(3, 4)
    assert result == 7, "oh no"

if __name__ == '__main__':
    should_work()
```

``` bash
$ python thing_that_should_work.py
```

# Programs that verify #

* is this a test?

``` bash
$ sbt compile
```

# A library #

* [`tiny-test`](https://github.com/jisantuc/tiny-test/)

# When should you property test? #

> - when there are _laws_
> - when you have an _oracle_
> - when you have a black box
> - when you have an expected round trip

# Property testing _everywhere_

> - [haskell](https://hackage.haskell.org/package/QuickCheck)
> - [purescript](https://github.com/purescript/purescript-quickcheck)
> - [scala](https://www.scalacheck.org/)
> - [elm](https://package.elm-lang.org/packages/elm-explorations/test/latest)
> - [rust](https://github.com/BurntSushi/quickcheck)
> - [C](https://github.com/silentbicycle/theft)
> - [python](https://hypothesis.readthedocs.io/en/latest/)
> - [old javascript](http://jsverify.github.io/)
> - [new javascript](https://github.com/dubzzz/fast-check)
> - [R](https://github.com/RevolutionAnalytics/quickcheck)
> - [julia](https://quickcheckjl.readthedocs.io/en/latest/)
