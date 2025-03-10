---
title: (Rewriting it in) Rust won't save you
author: James Santucci
patat:

    wrap: true
    margins:
        left: 5
        right: 5
    speakerNotes:
      file: ../notes.md
    eval:
      dot:
        command: graph-easy --from=dot --as=boxart
        fragment: false
        replace: true
      sixel:
        command: sh
        replace: true
        fragment: false
        wrap: rawInline
---

# (Rewriting it in) Rust won't save you

<!--
Hello everyone, welcome to "Rewriting it in Rust won't save you", where I'll try to convince you that "it's not
written in Rust" isn't responsible for anything that makes you mad on a daily basis.

There are some reasonable alternate titles for this talk -- **SLIDE**
-->

## Alternate titles

* Go won't save you
* Haskell won't save you
* AI ~~overlords~~ coding assistants won't save you

. . .

* Python won't kill you
* JavaScript won't kill you
* Java won't kill you
* Ruby won't kill you? PHP won't kill you?

<!--

But I stuck with "Rust won't save you," because it's 2025 and I've spent, I don't know, _whole minutes_ of my life
having to read past "it's written in Rust!" as the first feature people have listed in READMEs, and I'm over it.

There are other framings as well -- **SLIDE**

The big idea of this talk is that, while language choice matters some, but if you're careful, try hard, and really work
at it, you can write software you wish you hadn't in three months in any language. **PAUSE** Or software that you'll
still be proud of in six months in any language.

The obvious question here is "save you from what?" Two things:

1. the hard parts of writing good services in python
1. the hard parts of microservices

My intended audience here is mainly people who operate the web portion of Umbra's software stack; I know less about
FSW's different constraints, so I'm mainly going to focus on a hypothetical rewrite of a backend web service in Rust.

To be clear about my biases, I do not love Python. I have my reasons, but you hear plenty of reasons to be cranky
about Python, especially when people want to write different flavors of not-Python:

* it's too slow
* dynamic typing is bad, or gradual typing is bad, or the static typing part of dynamic typing is bad -- somehow you
  hear all of these
* modeling is too OO-y without a convention of the good parts of OO (so many god classes / classes with no defined
  interfaces that just become dumping grounds for anything you need to happen) / too functional (lambdas are a
  mistake, reduce is too complicated, comprehensions are syntactically confusing relative to loops, whatever)
* the module system is for children
* package management is worse than _insert your favorite language here_ (citation needed)
  (or maybe you're over lockfiles and you miss python 2.7.x when everything was compatible with your python version
  because there was practically one python version)

You could list similar complaints about JavaScript, but I don't touch any of our frontend code, and vanilla JavaScript
is enough of a punching bag on its own that we don't have any not-on-fire JavaScript emojis.

The languages themselves aren't super important though -- anywhere in this talk you hear "Rust" you can substitute
Haskell or Zig or GoLang or Clojure or Elixir whatever language is supposed to solve all of our problems tomorrow,
and anywhere in this talk you see "Python" you can substitute "JavaScript" or "PHP" or "Java" or any other un-sexy
language.

I am not going to try to convince you that Python is better than Rust, or that they're about as good as each other.
I am going to try to convince you that you shouldn't daydream about rewriting your services in Rust anyway.
-->

## My credentials

```sixel
convert -resize 480 "language-wars.png" sixel:-
```

. . .

(the `IO` monad is in fact better than futures)

<!--
Why should you listen to me? Am I just a Rust hater who wants you not to get to write Rust? I'd love for you to get to
write Rust!

* A long time ago I was excited about Haskell and wanted to rewrite a Scala service in Haskell. We'd read _Haskell
  Programming From First Principles_ as a group called Functional Summer, January had rolled around so we'd just
  finished it, and I was ready to put my enthusiastic beginner Haskell knowledge to the test.
* We had a Scala service, and I thought it would be fun and cool and maybe useful to rewrite the database interaction
  for one of the entities in Haskell.
* You might be asking -- isn't Scala complicated and weird enough? NO! It's _impure_! Because of JVM, it's _tainted_
  by OOP! It _has non-obvious mutation_!
* To me -- Haskell was _obviously better_ -- why didn't anyone care that we'd get "more correct" code at basically no cost?
  * reasons, in case anyone asks: the IO monad was obviously better than Futures, which are only *kind of*
    if you don't look too closely monadic; first-class typeclasses were obviously superior to implicit arguments;
    even further down the rabbit hole things like Eta lang meant we could still use JVM libraries that we depended on
    with "pretty much Haskell"... 

**SLIDE**
-->

## My credentials

```sixel
magick convert -resize 480 "what-could-it-cost.jpg" sixel:-
```

<!--
* And so I filled out the relevant forms to spend 10% of my time on porting one piece of the database interaction to
  Haskell. There's still a
  [branch](https://github.com/jisantuc/raster-foundry/tree/experiment/js/haskell-foundry) if you want to see how that
  went. I'd do a better job today, but it was a ton of work that included making solo choices over libraries for the
  less exciting parts of application development -- "my code is fast and _safe_" is fun in the abstract, "my code is
  fast and _safe_ and... like... takes these objects and puts them into the database and reads them from the database"
  is not all that exciting. That all went basically nowhere.
* Things I included:
  * one database model
  * a test harness that made sure I could do database serde with the model
* Things I did not include:
  * anything to manage database migrations (my database was already provided from the actual application)
  * any kind of wiring to run an application that could use my database model in a useful way
  * wiring up to any kind of CI process (which also means making sure CI can run the Haskell code -- that's easy
    enough for current me with `nix`, but it would have been _really hard_ for past me)
* The commit history stretches from late October 2018 to mid-February 2019

**SLIDE**
-->

## My credentials

```sixel
magick convert -resize 480 "traverse.png" sixel:-
```

<!--
* Eventually we got more into _functional Scala_, and I decided Scala is ok enough that my next job was helping Java
  developers be better at functional Scala full time.
* At an internal talk at that second job on one of the functional abstractions provided by one of the libraries,
  some Java dev with like 30 years of experience asked "is this supposed to be easy?"
* tl;dr: I've been the "why doesn't anyone care about ___ as much as I do?" person. For Haskell/Haskell-y Scala, it's
  _correctness_ and _mathematically rigorous abstraction_ and "have you tried `traverse`?" and
  "all design patterns are literally just functions"
* for Rust I gather it's "speed" and "memory safety" and, I don't know, some Rust enthusiast can probably rattle off
  more benefits
* But the point of this story is -- I too have wanted people to write everything in a better language. Rust isn't
  Haskell and you're not me from several years ago, but I'm still willing to bet several burritos that spinning up Rust
  skills for your team is harder than you think.
-->

# Why Rust?

## Why Rust in general?

* Rust is *probably* a better language than python

. . .

* memory safety/the borrow checker without having to think about a garbage collector is neat
* going fast is nice
* people seem to like `cargo`
* inline testing or whatever you call it where you write the tests in the same module as the production code looks
  super cool
* I like "pair programming with the compiler" and I think I'd like clippy

<!--
* I won't dispute that Rust is probably better than Python at being fast and at data modeling and probably a bunch
  of other things.

**SLIDE**

* I don't think there's a definitive ranking of the best programming languages or a universal scale of goodness, but if
  you wrote down all the things you want in a language, it's likely that in 2025, Rust in general makes better trades
  than Python does
* better: it's a lot newer! Rust 1.0 May 2015 vs. Feb 1991 for the first Python -- that's 25 years of stuff
  to learn from in language design, and computers today are more like computers from 2015 than computers today are like
  computers in 1991. It's also 25 years of not accumulating evolutionary scars like the GIL. Rust *should* be better.

Despite all this, I think you shouldn't day dream about rewriting your least favorite service in Rust anyway.

**SLIDE**
-->

# Why not Rust?

## What's wrong with your services today?

* does your service have non-communicative or confusing interfaces?
* is your service too slow?
* is your service too complex?

<!--
* Ok, so if Rust is probably technically superior to Python, why shouldn't we rewrite things in Rust? My short answer
  is that Rust isn't magic, it's just _really good at some stuff_.
-->

## Why won't Rust magically make your data modeling better?

[example](https://www.rustfinity.com/blog/parse-dont-validate#the-traditional-way:-validate)

```rust
async fn create_user_handler(body: &str) -> Result<(), Error> {
    let body: Value = serde_json::from_str(body)?;
 
    let email = body.get("email").ok_or("Email is required")?;
    let password = body.get("password").ok_or("Password is required")?;
 
    if !validate_email(email) {
        return Err("Invalid email");
    }
 
    if !validate_password(password) {
        return Err("Invalid password");
    }
 
    // ...
    create_user(email, password).await?;
}
 
async fn create_user(email: &str, password: &str) -> Result<(), Error> {
    // ...
}
```

<!--
* this example comes from one of the nine million "Parse, Don't Validate" riffs (as an example of what not to do)
* validators like this are _forgetful_ -- they throw away the knowledge you gain from validation, so anywhere you
  want to re-use something that you need to be validated, you have to check, since there's no evidence that that
  validation has occurred. So when you want to deal with the "user" that you've created here, you still have no
  knowledge of whether validation occurred. (In this case it's side-effecting rather than returning an object, but
  still)
* if you're used to `validate_foo(...) -> None:`, where either you get errors or your code continues to execute, this
  is the kind of thing you're going to write, and having `Result` available doesn't make the types any more informative
* or more generally, if you write your existing Python code, but in Rust, it'll have the same problems as the existing
  Python code.
-->

## Why won't Rust magically make your data and interface modeling better?

* Rust is better at modeling data, but are _you_ better at modeling data in Rust?
* Rust's module system is probably better than Python's, but are _you_ better at module design in Rust?

. . .

```python
def foo(q0: float, q1: float, flag: bool) -> float:
    ...
```

```rust
fn foo(q0: f32, q1: f32, flag: Boolean) -> float:
  ...
```

. . .

```sixel
magick convert -resize 480 "utils.jpg" sixel:-
```

<!--
* It's tempting to think that because you have a much stronger type system, you'll do a better job modeling data.

*SLIDE*

* I think this is incorrect for at least two reasons:
  1. types aren't data modeling. int, string, and bool are garbage types, but you'll use them everywhere anyway unless
     you get really used to newtype-ing everything. A function that takes two floats and a bool and returns a float
     in Rust is no more obvious than a function that takes two floats and a bool and returns a float in python.
  2. if you knew a cleaner, nicer set of interfaces for your service _right now_, you wouldn't need to
     rewrite your service in Rust to take advantage of it.
* Better types aren't magic, and designing good interfaces is hard even with good types.
* If you're not used to leveraging the type system the way that you can in Rust, you're not going to write super
  safe code leveraging the type system, you're going to write Python, but in Rust.

*SLIDE*

* Module design also isn't free, which explains the nearly 78 thousand `utils.rs` modules (as a sanity check, I also
  searched utils.java and utils.py, and they each had about 1.5 million files in GitHub; give it time, Rust
  will get there!)
  * some stats --
    * Rust: 78k `utils.rs`, 11.8 million `*.rs`, about 0.6% of files
    * Haskell: 14.3k `utils.hs`, 1.6 million `*.hs`, about 0.9% of files
    * Java: 1.3 million `utils.java`, 164 million `*.java`, about 0.8% of files
    * Python: 1.5 million `utils.py` out of 94.4 million `*.py`, about 1.6% of files -- this slightly deflated
      by about 4 million mandatory boilerplate `__init__.py` files but not by much

*SLIDE*
-->

## Why won't Rust magically make your services faster?

* a lot of your latency isn't going to be because your code is slow (it's because _my_ code is slow)

. . .

```sixel
magick convert -resize 1440 "sql-query-slow.png" sixel:-
```

```sixel
magick convert -resize 1440 "slow-other-service.png" sixel:-
```

<!--
* not necessarily _my_ code, but you know, someone else's code -- if you're Doing Microservices™️ a lot of the logic
  you care about is going to happen somewhere else (sometimes your database!)

*SLIDE*

* these two requests are:
  * a relatively slow command history `GET` in the `sat-gateway` (about 13 seconds)
  * a relatively slow HTTP request for `restricted-access-areas` from commercial tasking to scheduling
* the first request was slow because the database queries took a while. that gets faster with a schema / operations
  that query faster, e.g. with indices on relevant fields if it's a performance-sensitive query. Maybe it _is_
  performance-sensitive and you'd update the query to reflect that if you wrote the service in Rust.
  But why not just do that in Python?
* the scheduling request was slow because it sat around forever before it was allowed to talk to the database;
  that gets faster with better database connection pool tuning, not with Rust. maybe you'll do a better job with your
  connection pool config in Rust. Why not just do that in Python?
* So there are two things working against you here:
  * If you rewrite your service in Rust, you'll still have to write good database queries and figure out good connection
    pool configurations in your own services to prevent slowdowns that have nothing to do with the application code.
  * If you rewrite your service in Rust, even if your service is 100 times faster, you'll still have to talk to _my_
    slow old service.
* even if Rust is 100x faster, you're still going to sit around waiting for the network a lot of the time

*SLIDE*
-->

# How to rewrite your service in Rust

## How to rewrite your service at all

```dot
graph {
  A -> "A'"
  A -> B
}
```

Prove: `A' + B = A`

<!--
Your goal here is to show that the decomposition of service A into A' + B has the same interface and the same side
effects as service A.

Steps:
* write down all the side-effects that you're migrating
* write down the interface that you're migrating
* Example: Let Mentat Cook; migration / rewrite of downlink scheduling in `mentat-feasibility`
  * side-effects documented in "Summary of Proposal" in ADR
  * lucky, we thought: no public interface
-->

## You will be wrong

* Sometimes _really wrong_

<!--
* if the interfaces and side-effects were easy to write down, you probably wouldn't be excited to migrate whatever
  you're migrating to begin with.
* you have a design documentation problem coming in, and a different design documentation problem coming out.
* if you're very lucky and the world is just, when you're wrong, it will be your problem.
* if you're unlucky, when you're wrong, Eugene will get paged.
* Let Mentat Cook / 07 anomaly mitigation had the same issue -- part of the interface of downlink planning is an
  otherwise non-noteworthy comm message that gets sent after passes end, and also part of the internal interface is
  _time_ in a kinda confusing way.
-->

## Eventually you'll be right

* someday you will exercise all the edges you couldn't write down, then you win

<!--
* at this point, it's really exciting -- you've done the thing, and whatever benefits you predicted when you planned
  to migrate the thing should be coming in.
* now you can get back to normal SWE problems, which are still hard.
* there's no magic here, you still just have to try to do a really good job, so learn some stuff, do your best,
  and work through the built-in challenges of operating services
-->

# You're still you, you just write Rust now.
