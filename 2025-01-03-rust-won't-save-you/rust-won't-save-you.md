---
title: Rust won't save you
author: James Santucci
patat:

    wrap: true
    margins:
        left: 5
        right: 5
    speakerNotes:
      file: ./notes.md
    eval:
      sixel:
        command: sh
        replace: true
        fragment: false
        wrap: rawInline
---

# (Rewriting it in) Rust won't save you

## Alternate titles

* Go won't save you
* Haskell won't save you
* AI ~~overlords~~ coding assistants won't save you

. . .

* Python won't kill you
* JavaScript won't kill you
* Ruby won't kill you? PHP won't kill you?

<!--
* intended audience here is mainly people who operate the web portion of Umbra's software stack; I get that FSW has
  different constraints, and Rust vs. ... is a really important point
* do people still write Ruby? I don't know
* let's take python as a strawman -- if you want to have opinions about python, there are plenty of reasons you can
  pick to like or dislike python:
  * it's too slow
  * dynamic typing is bad, or gradual typing is bad, or the static typing part of it is bad
  * modeling is too OO-y without a convention of the good parts of OO (so many god classes / classes with no defined
    interfaces that just become dumping grounds for anything you need to happen) / too functional (lambdas are a
    mistake, reduce is too complicated, comprehensions are syntactically confusing relative to loops, whatever)
  * the module system is for children
  * the package management/artifact publication story is the worst of any major language (citation needed)
    (or maybe you're over lockfiles and you miss python 2.7.x when everything was compatible with your python version
    because there was practically one python version)
* or let's take javascript as a strawman:
  * actually let's not, just compare the Slack emoji we have for python and javascript
* point is, anywhere in this talk you see "Rust" you can substitute "Haskell" or "Zig" or "GoLang" or Clojure or Elixir
  whatever language is supposed to solve all of our problems tomorrow, and anywhere in this talk you see "Python" you
  can substitute "JavaScript" or "PHP" or "Java" or any other un-sexy language
-->

## My credentials

```sixel
magick convert -resize 480 "language-wars.png" sixel:-
```

<!--
* A long time ago I was excited about Haskell and wanted to rewrite a Scala service in Haskell
* Isn't Scala complicated and weird enough? NO! It's _impure_! Because JVM, it doesn't support
  _referential transparency_!
* And so I filled out the relevant forms to spend my 10% time (what it sounds like) on porting one piece of the
  database interaction to Haskell. There's still a
  [branch](https://github.com/jisantuc/raster-foundry/tree/experiment/js/haskell-foundry) if you want to see how that
  went. I'd do a better job today, but it was a ton of work that included making solo choices over libraries for the
  less exciting parts of application development -- "my code is fast and _safe_" is fun in the abstract, "my code is
  fast and _safe_ and... like... takes these objects I care about and puts them in and reads them from a database"
  is not all that exciting.
-->

## My credentials

```sixel
magick convert -resize 480 "what-could-it-cost.jpg" sixel:-
```

. . .

(the `IO` monad is in fact better than futures)

<!--
* To me -- Haskell was _obviously better_ -- the IO monad was obviously better than Futures, which, through
  non-laziness, break referential transparency; first-class typeclasses were obviously superior to implicit arguments;
  even further down the rabbit hole things like Eta lang meant we could still use JVM libraries with "basically
  Haskell"... why didn't anyone care that we'd get "more correct" code at basically no cost?
* Eventually we got more into _functional Scala_ in the TypeLevel ecosystem, getting an IO monad from a framework
  inspired by Rust's `tokio` and I decided Scala is ok enough that my next job was helping Java
  developers be better at Scala full time.
* I was a true believer -- even if I'd stopped fighting for Haskell in the language wars, I was still fighting for
  Haskell-y Scala (if you believe the marketing speak of the people who found that ecosystem too complicated) or
  Technically Superior Scala (if you believe the marketing speak of the people like me who really liked the
  Haskell-y FP ecosystem in Scala). To this day a few of the libraries in that ecosystem are what I think of as
  the best I've used in their domains, sometimes without competitors (`cats`/`cats-effect`), sometimes with a
  competitor I've only kind of dabbled in (`fs2` is the best streaming library I've ever used, but I've only ever used
  one other streaming library -- `conduit` -- and then only barely), and sometimes with a bunch of other competitors
  (last I checked on this, I thought `Scala.js` is the best compiles-to-javascript language out there)
-->

## My credentials

```sixel
magick convert -resize 480 "traverse.png" sixel:-
```

<!--
* tl;dr: I've been the "why doesn't anyone care about ___ as much as I do?" person. For Haskell/Haskell-y Scala, it's
  _correctness_ and _mathematically rigorous abstraction_ and "have you tried `traverse`?" and
  "all design patterns are literally just functions"
* for Rust I gather it's "speed" and "memory safety" and, I don't know, some Rust enthusiast can probably rattle off
  more benefits/memes
-->

## <fill in the blank> solves this!

* Rust is probably a better language than python

. . .

* memory safety is probably good, though I don't know why Pythonistas (or Java developers or anyone who mainly writes
  in a language with a garbage collector) would care
* speed is nice
* people seem to like `cargo`
* inline testing is pretty neat

<!--
* sometimes whatever you fill in the blank with is Rust, sometimes it's GoLang, sometimes it's zig, you get the idea
* better: it's a lot newer! Rust 1.0 May 2015 vs. Feb 1991 for the first Python -- that's 25 years of stuff
  to learn from in language design, computers today are more like computers from 2015 than computers today are like
  computers in 1991
* I don't think there's a definitive ranking of the best programming languages or a universal scale of goodness, but if
  you wrote down all the things you want in a language, it's likely that in 2025, Rust in general makes better trades
  than Python does
-->

## Digression: a real-life task

* your job is to design a service
* that service, as of right now, needs to talk to two other services
* you write it in python because everybody uses python

<!--
* this is kind of our status quo on the backend, but you could play out something similar for Rust -> WASM vs. JS/TS
  on the frontend
* there are costs, sure -- defaulting to python means everything pays whatever costs you have to pay from python apps,
  like the list of stuff above. everyone more or less knows those costs, so who cares? but they're costs nonetheless.
-->

## Digression: a real-life task

```sixel
magick convert -resize 480 "./one-eternity-later.jpg" sixel:-
```

* what's probably wrong with your service at this point?

. . .

<!--
* probably not: operationally significant memory management issues, ill-formed arguments in critical code paths,
  difficult software delivery; the reason these are probably not is that if your services are too bad at memory
  management, they fall over; if you can't detect ill-formed arguments in critical code paths, you spend all of your
  time on pretty dumb bugs; and if you can't deliver software, you... can't deliver software? and you just don't have
  services/a job/a company anymore, depending on how hard it is.
* probably:
  * you have a few leaky abstractions that show up everywhere that are going to be costly to un-leaky
  * the services you talk to don't have clear domains, so you need some stuff from them where, to give you what you
    you need, they maybe need some stuff from you
  * there are missing models that everybody has a piece of, or that one class has to stand in for in a bunch of
    different contexts
* also probably: a year has passed and you're still in business! You're probably running into scaling problems, good
  job.
-->

## Complexity problems

```sixel
magick convert -resize 480 "spaghetti.webp" sixel:-
```

<!--
* suppose instead your problem is that you've got some logic that exhibits the message chain code smell (function call
  whose main job is to slightly repackage the data for another function call which slightly repackages the data for
  another function call which ...)
* I don't think Rust spaghetti is better than python spaghetti? It'll be faster to run, but it'll still be spaghetti
-->

## Complexity problems

```sixel
magick convert -resize 480 "too-many-things.jpg" sixel:-
```

<!--
* Let's say you have an "abstraction" that doesn't have an interface, it's just a class that starts with methods
  to do two related things
* Later you need to do a kind of related thing, so it goes on the class
* Still later, you've free associated your way to a class that no longer has a defined responsibility and instead has
  a million things it's responsible for
* It doesn't have to be a class (it's python! or it's Rust! nothing has to be a class!) but God modules and God
  classes are, I think, the same kind of code smell
* Your least favorite gigantic module doesn't become suddenly tractable because it's 6000 lines of loosely related
  `utils` code written in Rust instead of in Python
-->

## Throughput problems

* a lot of your latency isn't going to be because your code is slow (it's because _my_ code is slow)

<!--
* not necessarily _my_ code, but you know, someone else's code -- if you're Doing Microservices™️ a lot of the logic
  you care about is going to happen somewhere else
-->

## Throughput problems

```sixel
magick convert -resize 1440 "sql-query-slow.png" sixel:-
```

<!--
* a relatively slow `command-invocations` `GET` in `sat-gateway` (about 13 seconds)
* will Rust make your SQL queries faster or help you create a schema that's better for the queries you execute
  all the time?
-->

## Throughput problems

```sixel
magick convert -resize 1440 "slow-other-service.png" sixel:-
```

<!--
* a relatively slow HTTP request for `restricted-access-areas` in `commercial-tasking-service`
* only slow because `python-scheduling-service` was slow
* `python-scheduling-service` was slow because it sat around forever before it was allowed to talk to the database
* will Rust make other teams' services faster or help them configure their database connection pools better?
* point on all of these -- even if Rust is 100x faster, you're still going to sit around waiting for the network a lot
  of the time
-->

## If we only rewrote in Rust

* the traces above would be faster by an amount no one would notice
* they'd be... memory... safer?
* they also wouldn't have runtime errors caused by invalid data being passed around?

# When is language choice important

## Choosing a language when you have nothing

* for some new project, you want to choose a language based on _language features_ and how they map to your problem
  domain
* some important language features:
  * type safety
  * memory safety
  * ecosystem
  * syntax
  * runtime for the kinds of tasks that you want to run

<!--
* type safety: you should probably be suspicious of anyone who makes too strong of a claim here https://danluu.com/empirical-pl/
* ecosystem: libraries useful for what you're up to, off-the-shelf CI components in Gitlab or GitHub, JUnit-style
  coverage reports
* syntax:  if you love operators, obviously Haskell; if you hate operators, obviously not Haskell
* runtime: if you have a bunch of array programming to do, don't pick a language where the ecosystem has great support
  for everything but array programming
* but really, you're probably not going to learn a new language for your greenfield service even if it's the best
  language for the job -- you're going to pick what you know best, and that's maybe even the right choice
-->

## Choosing a language when you have a business to operate

* choose the language that your services are already running in

<!--
* really I think that's the whole decision tree -- KEEP GOING
* not just you, but *EVERYONE* will have to learn new testing frameworks, and new web frameworks, and a new CI setup,
  and new weird failure modes, and new auxiliary tools that can get out of sync on different developers' machines,
  and new weird stuff that goes wrong when the service has been mostly ignored for two months because it's been doing
  fine, and...
-->

# How to rewrite your service in Rust

<!--
OUTLINE

* given you want to migrate service A to service A' + service B, how do you know that service A' + service B = service A?
* you have to know what service B's responsibilities are
* which means you have to know what service A's responsibilities are
* which means... uh-oh, now you have a design documentation problem
* design documentation is hard, "we should rewrite it in Rust" is easy

* challenge 1: _interface_ you want to migrate to service B
* challenge 2: _effects_ you want to migrate to service B
* challenge 3: _dependencies_ of service A on service B
* challenge 4: not doing it solo

* but wait: Rust has nothing to do with this, this is all part of a challenge for any service migration. you got it!
-->
