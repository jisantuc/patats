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

## Why should we want typed STAC

> - failing _really fast_ when things aren't correct
> - JSON Schema split out across a billion files is hard to navigate
> - types of things are hard to remember (was this a list of ints? of strings? does it matter?)
> - lots of enums flying around, and remembering words is hard
> - computers are _really good_ at checking types

## Let's type some STAC

- A really good type for items:

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

## Does it reject bad inputs?

. . .

```python
funcOnBs(ItemWithA())
```

```
File "/.../src/types.py", line 35, in <module>: Function funcOnBs was
    called with the wrong arguments [wrong-arg-types]
         Expected: (item: ItemExtensionB)
  Actually passed: (item: ItemWithA)
```

```python
funcOnAs(ItemWithB())
```

```
File "/.../src/types.py", line 38, in <module>: Function funcOnAs was
    called with the wrong arguments [wrong-arg-types]
         Expected: (item: ItemExtensionA)
  Actually passed: (item: ItemWithB)
```

## Does it accept FancyItems?

. . .

```python
funcOnBs(FancyItem()) # ✔️
funcOnAs(FancyItem()) # ✔️
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

- `ItemWithAB` ✔️
- `FancyItem` ❌

. . .

```python
funcOnAtLeastAB(FancyItem())
```

```
File "/.../src/types.py", line 51, in <module>: Function funcOnAtLeastAB was
    called with the wrong arguments [wrong-arg-types]
         Expected: (item: ItemWithAB)
  Actually passed: (item: FancyItem)
```

> - why isn't `FancyItem` an `ItemWithAB`?
> - I don't know!

## What do we have to do?

```python
class FancierItem(ItemWithAB, ItemExtensionC):
    pass
```

## How far did we get?

> - first hurdle: call `f` on anything with one extension ✔️
> - second hurdle: call `f` on anything with two extensions ❌

# Typeclassed STAC

## What can we do instead?

> - orientation of inheritance model: our item _is a_ label item
> - what knowledge does this encode? "we know this item has label extension fields"

## Let's typeclass some extensions

```scala
type ExtensionResult[T] = ValidatedNel[String, T]

trait ItemExtension[T] {
    def getExtensionFields(stacItem: StacItem): ExtensionResult[T]
}
```

. . .

- plus some other stuff in practice

## What is this?

> - `ItemExtension[T]` is a _typeclass_
> - Big picture, it says if we can find an _instance for T_, we can try to get something
    of type `T` from a `StacItem`

## More on typeclasses

> - typeclasses are a way of describing capabilities
> - a simple example -- `Show` is a typeclass for types that can be converted to `Strings`

```scala
trait Show[T] {
    def show(value: T): String
}
```

> - goal is to express the things that a type must be able to do, and reason about things from there
> - importantly: we don't modify `T` at all (i.e., nothing _extends_ `Show`), so functions from `T`
    to something else don't need to care about `Show` unless we ask them to


## How does this help with our problem?

> - Before, with one extension:

```python
AtLeastA = TypeVar("AtLeastA", bound=ItemExtensionA)

def funcOnAs(item: AtLeastA) -> None:
    return
```

> - After, with one extension:

```scala
val item: StacItem = ???
item.getExtensionFields[ItemExtensionA]
// ExtensionResult[ItemExtensionA]
// then do whatever we want with the result
```

## How does this help with our problem?

> - Before, with two extensions:

```
File "/.../src/types.py", line 57, in <module>: Function funcOnExactlyAB was
    called with the wrong arguments [wrong-arg-types]
         Expected: (item: ItemWithAB)
  Actually passed: (item: FancyItem)
```

> - After, with two extensions:

```scala
(item.getExtensionFields[ItemExtensionA],
 item.getExtensionFields[ItemExtensionB]).tupled
// ExtensionResult[(ItemExtensionA, ItemExtensionB)]
// then do whatever we want with the result
```

## Typeclass usage in `stac4s`

> - what are the capabilities we want all item extensions to have?
> - get the relevant fields from an item, and let me know what went wrong
> - if I have valid fields, add them to an item and give me the result
> - in `stac4s`:

```scala
trait ItemExtension[T] {
  def getExtensionFields(item: StacItem): ExtensionResult[T]
  def addExtensionFields(item: StacItem, properties: T): StacItem
}
```

## Usage in Franklin

> - "and let me know what went wrong"
> - nascent `validation` extension, returning attempted extension validations and the fields that failed

```scala
final case class ValidationExtension(
    attemptedExtensions: NonEmptyList[NonEmptyString],
    errors: List[NonEmptyString]
)
```

> - `ValidationExtension` is an item extension

## What do we get from this?

> - functions can ask for extensions, rather than items with extensions
> - we can ask for as many as we want, then combine the results (if they're all valid) or do something with all
    the errors
> - we can handle incorrectly constructed STAC items (from hand-written json or what have you), provide information,
    and let people fix it with the transactions extension

## What if I don't want to write Scala?

# END / thank you