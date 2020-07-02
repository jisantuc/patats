class Item {}

trait ItemExtension1

trait ItemExtension2

trait ItemExtension3

class FancyItem
    extends Item
    with ItemExtension1
    with ItemExtension2
    with ItemExtension3 {}

class With1And3 extends Item with ItemExtension1 with ItemExtension3 {}

def foo1[T <: Item with ItemExtension1 with ItemExtension2]: Unit =
  println("callable 1")

def foo2(item: Item with ItemExtension1 with ItemExtension2): Unit =
  println("callable 2")

// calling
// foo1[FancyItem]
// foo2(new FancyItem())
// foo1[With1And3]
// foo2(new With1And3())
