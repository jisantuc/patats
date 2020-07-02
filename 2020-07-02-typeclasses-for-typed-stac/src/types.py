from typing import TypeVar


class StacItem(object):
    pass


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


AtLeastA = TypeVar("AtLeastA", bound=ItemExtensionA)
AtLeastB = TypeVar("AtLeastB", bound=ItemExtensionB)


def funcOnAs(item: AtLeastA) -> None:
    return


def funcOnBs(item: AtLeastB) -> None:
    return


# do we get expected type errors? (check with pytype)
# funcOnBs(ItemWithB())
# funcOnBs(ItemWithA())
# funcOnBs(FancyItem())

# funcOnAs(ItemWithB())
# funcOnAs(ItemWithA())
# funcOnAs(FancyItem())


class ItemWithAB(StacItem, ItemExtensionA, ItemExtensionB):
    pass


AtLeastAB = TypeVar("AtLeastAB", bound=ItemWithAB, covariant=True)


def funcOnAtLeastAB(item: AtLeastAB) -> None:
    return


# funcOnAtLeastAB(ItemWithAB())
# funcOnAtLeastAB(FancyItem())


class FancierItem(ItemWithAB, ItemExtensionC):
    pass


# funcOnAtLeastAB(FancierItem())


def funcOnExactlyAB(item: ItemWithAB) -> None:
    return


# funcOnExactlyAB(ItemWithAB())
# funcOnExactlyAB(FancyItem())
