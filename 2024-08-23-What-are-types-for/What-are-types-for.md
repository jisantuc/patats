---
title: What are types for?
author: James Santucci
patat:

    wrap: true
    margins:
        left: 5
        right: 5
    images:
      backend: auto
    speakerNotes:
      file: ./notes.md

---

# What are types *good* for? (and how to have a bad time)

# SWE in 2024

* you're gonna have types
* you're not going to release code unless it mostly agrees with those types

<!--
* Typescript ubiquity, incremental typing in python, Rust, lots of others
* obviously still a few holdouts (Clojure! Vanilla JS! Nix! obviously everyone's sad about nix not being typed)
-->

# Some things types are good for

* automatic documentation
* software simplification

<!--
crux of this talk is these three things -- types can be really good at them, but it's easy to get less benefit
and still have to have a bunch of arguments with mypy if you don't _use the types_
-->

# How to have a bad time 1: documentation

* types tell users important details about code that they otherwise have to rely on human prose to figure out

. . .

```python
def geohash_point(x: float, y: float) -> str: ...
```

vs.

```python
def geohash_point(x, y):
    """Return a geohash string from x and y.

    Args:
        x (float): the x value
        y (float): the y value

    Returns:
        the geohash of the point (x, y)
    """
    ...
```

<!--
* what happens when the interface to geohash changes?
* without static type checking + with tests making sure geohash_point works you get yelled at in tests
* without static type checking or tests you get yelled at in prod
-->

# How to have a bad time 1: documentation

* but really `Callable[[float, float], str]` doesn't tell us much

. . .

```python
from typing import NewType

Lon = NewType("Lon", float)
Lat = NewType("Lat", float)
GeoHash = NewType("GeoHash", str)

def geohash_point(x: Lon, y: Lat) -> GeoHash: ...

geohash_point(22.2, 22.3)  # error!
```

<!--
* Why is float -> float -> str _bad_? No domain information! Only primitive types. We know some things about our
  domain, e.g., that we're geohashing a lat/lon coordinate
* We can represent that information! with the edit above, we can't call geohash_point with any two floats, and we can't
  pass a Lat to the Lon parameter or vice-versa (well we can -- newtypes don't mess with runtime, but VSCode / mypy
  will yell at you if you do)
* summary: use newtype for domain-specific primitive types instead of un-informative plain primitives, get better type-
  driven documentation
-->

# How to have a bad time 2: software simplification

* consider two series of function calls, here marked only with their return types

```
Any -> Any -> Any -> Any -> ... -> Any

bool -> int -> str -> int -> ... -> int
```

<!--
* which of these is easier to understand? knowing nothing about the code, I think the latter -- you at least have some
  sense of the limits of what can happen at each step
* this has to do with _cardinality_ -- types can tell us how many possible implementations there are of a function
  (notwithstanding side-effects / mutation)
-->

# How to have a bad time 2: software simplification

* let `|a|` be "the cardinality of type `a`"
* `|None|` = 1
* `|bool|` = 2

. . .

* `|Optional[bool]|` = 3
* `|tuple[bool, bool]|` = 4
* `|Callable[[bool], Optional[bool]]|` = 9
* `|str|` = ??

<!--
* type cardinality is at the core of why "algebraic data types" are algebraic
* cardinality of Optional[bool] is 3 because Optional is a sum type, where the cardinality of the type is the _sum_
  of the cardinality of the types in its branches (in this case, None and `bool`)
* cardinality of `tuple[bool, bool]` is 4 because tuple is a product type, where the cardinality of the type is
  the _product_ of the cardinality of the types it contains (a _and_ b, in this case bool and bool)
* `bool -> Optional[bool]` has cardinality |Optional[bool]| ^ |bool|, which is where we get exponentiation, which is
  where these numbers can start to go a little nuts
-->

# How to have a bad time 2: software simplification

* `str -> bool` vs. `TaskStatus -> bool` -- how many implementations?

. . .

* `int -> None` vs. `int -> int`

<!--
* if you live in primitive types, there are 2 ^^ infinity paths through `str -> bool`, but only 2 ^^ |TaskStatus| paths
  through a TaskStatus -> bool function. That's a big improvement!
* if you have functions that exist only for their side-effects, all bets are off. A function with a signature
  `int -> None` only has one _pure_ implementation (`return None`), but because `-> None` is the side-effect shibboleth
  in python, that function can do literally anything
* summary: use lower cardinality types when you can do limit the incidental complexity of implementations of _things_
-->

# The end

<!--
* and that's kind of it for now, since half-baked
-->
