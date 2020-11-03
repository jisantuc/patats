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
    assert result == 7, "oh no"
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
    assert result == 7, "oh no"

if __name__ == '__main__':
    should_work()
```

```bash
$ python thing_that_should_work.py
```

# Programs that verify

- is this a test?

```bash
$ sbt compile
```

# This talk

> - tests are programs that verify your expectations about other programs
> - property testing can save you from having to state your expectations separately about a lot of similar cases
> - you can property test _anywhere_

# A library

- [`tiny-test`](https://github.com/jisantuc/tiny-test/)

# When should you property test?

> - when there are _laws_
> - when you have an _oracle_
> - when you have a black box
> - when you have an expected round trip

# Property testing in python and javascript

> - [`hypothesis`](https://hypothesis.readthedocs.io/en/latest/)
> - [`jsverify`](http://jsverify.github.io/)