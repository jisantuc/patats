---
title: A Gentle Introduction to Typeclass Derivation
author: James Santucci
patat:
    wrap: true
    margins:
        left: 20
        right: 20
---

# Goals of this talk #

> - you'll know what typeclasses are
> - you'll understand implicit resolution in Scala
> - you'll understand (one example of) how automatic typeclass derivation works

# Code example #

- you can mess around in scastie here: https://scastie.scala-lang.org/jziUDNEfSN2NGO2Hf7j6TA

# Typeclasses #

- describe capabilities without affecting types
- "a parameterised trait representing some sort of general functionality that we'd like to apply to a wide range of types"
  _The Type Astronaut's Guide to Scala_

# Typeclasses #

- for example:
  - `chair`, `couch`, `bed`, `stool`, `porch`, `roof`, `jetSki`, `flagPole`
  - you can sit on all of these
  - In OO paradigm: `Seat`, and each would inherit from `Seat`
  - this inheritance affects the type -- every `chair` _is a_ `Seat`

# Typeclasses #

- with typeclasses instead:

```scala
trait Seat[A] {
    def sit(self: A): Unit
}

object Seat {
    implicit val chairSeat: Seat[Chair] = ???
}
```

> - `Chair`s gain powers without having their type changing -- every `Chair` is still just a `Chair`
> - `implicit val chairSeat` is _a Seat instance for Chair_
> - this idea is ubiquitous in Scala and Haskell, but not all languages that enable FP

# Typeclasses -- The Bad #

- instances can be hard to construct when nothing is free:

```scala
implicit val encLabelExtensionPropertiesObject: Encoder.AsObject[LabelItemExtension] = Encoder
  .AsObject[Map[String, Json]]
  .contramapObject((properties: LabelItemExtension) =>
    Map(
      "label:properties"  -> properties.properties.asJson,
      "label:classes"     -> properties.classes.asJson,
      "label:description" -> properties.description.asJson,
      "label:type"        -> properties._type.asJson,
      "label:tasks"       -> properties.tasks.asJson,
      "label:methods"     -> properties.methods.asJson,
      "label:overviews"   -> properties.overviews.asJson
    )
  )
```

# Typeclasses -- The Bad #

- instance can be hard to verify when nothing is free
> - reverse of previous encoder also includes a bunch of magic strings
> - how to check?
> - laws

# Typeclasses -- The Bad #

- No hard and fast rule for where to put your typeclass instances
> - in the companion object?
> - in the companion to the typeclass for common instances?
> - in an `Implicits` object?
> - in an `implicits` package?
> - what about typeclasses for _other people's types_?

# Typeclasses -- The Ugly #
- Corollary to "where to put them?": Without a coherence rule, you can be looking at
  _the wrong instance_

# Typeclasses in practice #

# A common experience #

> - you'll have some typeclass you need an instance for for your type
> - let's say it's `Codec` from `circe` -- a typeclass that says we know how to
    convert a type to and from JSON
> - if the type you need an instance for is a case class, and it's "normal stuff", you can
    derive the typeclass for free:

```scala
import io.circe._, io.circe.generic.semiauto._

case class Foo(a: Int, b: String, c: Boolean)

implicit val fooDecoder: Decoder[Foo] = deriveDecoder[Foo]
implicit val fooEncoder: Encoder[Foo] = deriveEncoder[Foo]
```

https://circe.github.io/circe/codecs/semiauto-derivation.html

# A common experience #

> - Or let's say you're talking to a database with doobie
> - And you need to get values into and out of database rows
> - It's fine as long as your case class is "normal stuff":

```scala
case class Country(code: String, name: String, pop: Int, gnp: Option[Double])

sql"select code, name, population, gnp from country"
  .query[Country]
```

# A common experience #

- what is it about case classes that makes this work?

# `HLists` #

# `HLists` #

> - doobie also mentions `HLists` as a type it can send into and out of databases
    as long as they're normal stuff
> - what are they and how does that work?
> - `HLists` are like lists but for heterogeneous types, like tuples, but _inductive_

```scala
// more or less
sealed abstract class HList
case object HNil extends HList
case class HCons[A](value: A, rest: HList) extends HList
```

> - constructor / destructor is `::`

# Recursion on normal lists #

```scala
def sum(nums: List[Int]) = nums match {
  case h +: t => h + sum(t)
  case Nil => 0
}
```

> - _value-level_ -- happens at run-time

# So what's this? #

```scala
implicit val hnilPrinter: PrintFieldTypes[HNil] =
  PrintFieldTypes.nil
implicit def hlistPrinter[H, T <: HList](
    implicit headPrinter: PrintFieldTypes[H],
    tailPrinter: PrintFieldTypes[T]
): PrintFieldTypes[H :: T] = PrintFieldTypes.instance {
  case h :: t =>
    h.printFieldTypes ++ t.printFieldTypes
}
```

> - when do the two `::` destructures occur?

# Bridging the `HList` <-> `case class` gap #

# Generics #

```scala
trait Generic[A] {
  type Repr
}
```

> - a bi-directional mapping between `A` and `Repr`
> - `Repr` is a _dependent type_: specific _values_ for `Generic[A]` will determine the type of `Repr`
> - `Repr` is the type encoding the _generic representation of `A`_

# `case class` Generics #

- probably you can guess that `Repr` for a `case class` is an `HList`

```scala
// from scastie
val gen = Generic[TSMExample]
// Generic[TSMExample]{type Repr = Int :: String :: Boolean :: shapeless.HNil}
```

> - we definitely know how to print field types for `Int :: String :: Boolean :: HNil` --
    we already did that
> - how can we use this generic to convince Scala that it knows how to print field types for
    our case class?

# Resolving generics with implicits #

- we'll use a helper type:

```scala
Generic.Aux[A, R] == Generic[A] { type Repr = R }
```

- and a function on generics:

```scala
// 
trait Generic[T] {
  type Repr
  /** Convert an instance of the concrete type to the generic value representation */
  def to(t: T): Repr
```

# Resolving generics with implicits #

```scala
implicit def genericPrinter[A, R](
    implicit gen: Generic.Aux[A, R],
    printer: PrintFieldTypes[R]
): PrintFieldTypes[A] =
  PrintFieldTypes.instance { a =>
    printer.printFieldTypes(gen.to(a))
  }
```

> - "given a type A and a generic representation R that we know how to print field types for,
    construct a `PrintFieldTypes[A]` as follows"

# :tada: #

# what can go wrong #

> - error messages unhelpful if something is missing
> - no really they're bad enough that there's a huge message in doobie if a Meta instance can't be constructed:
    https://tpolecat.github.io/doobie/docs/12-Custom-Mappings.html#when-do-i-need-a-custom-type-mapping
> - time consuming (why `skunk`, the successor to `doobie`, made all codecs explicit instead of implicit)

# what's missing here? #

> - not all types are case classes! (e.g., coproducts / sum types)
> - not all typeclasses take a type with kind TYPE (e.g., functors / applicatives monads)
> - some typeclasses need more than just the types of fields (e.g., json also wants field _names_)

# What can I read about these things? #

- there are at least two good books!
> - [The Type Astronaut's Guide to Shapeless](https://underscore.io/books/shapeless-guide/)
> - [Thinking with Types](https://leanpub.com/thinking-with-types)
> - I've started but not finished both and I'd love to have a buddy