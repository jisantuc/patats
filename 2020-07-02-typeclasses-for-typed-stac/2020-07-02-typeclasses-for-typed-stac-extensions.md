---
title: Typeful STAC Extensions with Typeclasses
author: James Santucci
patat:
    wrap: true
    margins:
        left: 20
        right: 20
---

# Typed STAC

## Why might we want types in general

> - making impossible states impossible! (or at least more difficult)
> - failing _really fast_ when things aren't correct
> - forcing recognition of possible failure states (if we're lucky)
> - computers are _really good_ at checking types

## Why should we specifically want types for STAC

> - JSON Schema split out across a billion files is hard to navigate
> - types of things are hard to remember (was this a list of ints? of strings? does it matter?)
> - lots of enums flying around

## Let's type some STAC

A really good type for items:

```python
class StacItem(object):
    pass
```

> - what kind of items are there?

## Let's type some extensions

```python
class ItemExtensionA(object):
    pass

class ItemExtensionB(object):
    pass

class ItemExtensionC(object):
    pass

class ItemWithB(StacItem, ItemExtensionB):
    pass

class ItemWithA(StacItem, ItemExtensionA):
    pass

class FancyItem(StacItem, ItemExtensionA, ItemExtensionB, ItemExtensionC):
    pass
```

## And some functions that need that type information

```python
AtLeastA = TypeVar("AtLeastA", bound=ItemExtensionA)
AtLeastB = TypeVar("AtLeastB", bound=ItemExtensionB)

def funcOnAs(item: AtLeastA) -> None:
    return

def funcOnBs(item: AtLeastB) -> None:
    return
```

## Does it work?

. . .

```
File "/.../src/types.py", line 35, in <module>: Function funcOnBs was called with the wrong arguments [wrong-arg-types]
         Expected: (item: ItemExtensionB)
  Actually passed: (item: ItemWithA)
File "/.../src/types.py", line 38, in <module>: Function funcOnAs was called with the wrong arguments [wrong-arg-types]
         Expected: (item: ItemExtensionA)
  Actually passed: (item: ItemWithB)
```

## Great let's do more

> - let's say we have a combination of item extensions we want to express

```python
class ItemWithAB(StacItem, ItemExtensionA, ItemExtensionB):
    pass

AtLeastAB = TypeVar("AtLeastAB", bound=ItemWithAB)

def funcOnAtLeastAB(item: AtLeastAB) -> None:
    return
```

> - can we call this with an instance of `ItemWithAB`?
> - can we call this with an instance of `FancyItem`?

## Well can we?

. . .

yes and no

. . .

```
File "/.../src/types.py", line 51, in <module>: Function funcOnAtLeastAB was called with the wrong arguments [wrong-arg-types]
         Expected: (item: ItemWithAB)
  Actually passed: (item: FancyItem)
```

> - why isn't `FancyItem` an `ItemWithAB`?
> - I don't know!

## How far did we get?

> - first hurdle: call `f` on anything with one extension ✔️
> - second hurdle: call `f` on anything with two extensions ❌
> - my claim: a sufficient mass of interesting work with extensions requires at least two

# Typeclassed STAC

## What can we do instead?

> - orientation of inheritance model: type of thing known in advance, our item _is a_ label item
> - why do we want our item _to be a_ label item?
  > - so we can get label item fields from it
> - can we express "get label item fields from it" instead?