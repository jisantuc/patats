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
      sixel:
        command: sh
        replace: true
        fragment: false
        wrap: rawInline
---

## (Rewriting it in) Rust won't save you

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

But I stuck with "Rust won't save you," because it's 2025 and I've wasted, I don't know, _whole minutes_ of my life
having to read past "it's written in Rust!" as the first feature people have listed in READMEs, and I'm over it.

There are other framings as well -- **SLIDE**

Do people still write Ruby? I don't know, probably, the world is big.

The big idea of this talk is that, while language choice matters some, but if you're careful, try hard, and really work
at it, you can write software you'll hate in three months in any language. **PAUSE** Or software that you'll still
love in six months in any language I guess.

My intended audience here is mainly people who operate the web portion of Umbra's software stack; I know less about
FSW's different constraints, so I'm mainly going to focus on a hypothetical rewrite of a backend web service in Rust.
Since our backend services are Python right now, let's take Python as a strawman.

If you have opinions about python, there are plenty of reasons you can pick to like or dislike python:

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

We could play a similar game with JavaScript, but I don't touch any of our frontend code, and vanilla JavaScript is
enough of a punching bag on its own that we don't have any not-on-fire JavaScript emojis.

The languages themselves aren't super important though -- anywhere in this talk you hear "Rust" you can substitute
Haskell or Zig or GoLang or Clojure or Elixir whatever language is supposed to solve all of our problems tomorrow,
and anywhere in this talk you see "Python" you can substitute "JavaScript" or "PHP" or "Java" or any other un-sexy
language.

I am not going to try to convince you that Python is better than Rust. I am going to try to convince you that you
shouldn't daydream about rewriting stuff in Rust anyway.
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
  by OOP! It _has mutation_!
* To me -- Haskell was _obviously better_ -- the IO monad was obviously better than Futures, which are only *kind of*
  if you don't look too closely monadic; first-class typeclasses were obviously superior to implicit arguments;
  even further down the rabbit hole things like Eta lang meant we could still use JVM libraries that we depended on
  with "pretty much Haskell"... why didn't anyone care that we'd get "more correct" code at basically no cost?

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
  developers be better at Scala full time.
* I was a true believer -- even if I'd stopped fighting for Haskell in the language wars, I was still fighting for
  Haskell-y Scala. To this day a few of the libraries in that ecosystem are what I think of as
  the best I've used in their domains, sometimes without competitors (`cats`/`cats-effect`), sometimes with a
  competitor I've only kind of dabbled in (`fs2` is the best streaming library I've ever used, but I've only ever used
  one other streaming library -- `conduit` -- and then only barely), and sometimes with a bunch of other competitors
  (last I checked on this, I thought `Scala.js` is the best compiles-to-javascript language out there)
* tl;dr: I've been the "why doesn't anyone care about ___ as much as I do?" person. For Haskell/Haskell-y Scala, it's
  _correctness_ and _mathematically rigorous abstraction_ and "have you tried `traverse`?" and
  "all design patterns are literally just functions"
* for Rust I gather it's "speed" and "memory safety" and, I don't know, some Rust enthusiast can probably rattle off
  more benefits/memes
-->

## <your favorite language> solves this!

* Rust is *probably* a better language than python

. . .

* memory safety/the borrow checker without having to think about a garbage collector is neat
* going fast is nice
* people seem to like `cargo`
* inline testing or whatever you call it where you write the tests in the same module as the production code looks
  super cool

<!--
* I've thought often "Haskell solves this!"

**SLIDE**

* sometimes whatever you fill in the blank with is Rust, sometimes it's GoLang, sometimes it's zig, you get the idea
* I don't think there's a definitive ranking of the best programming languages or a universal scale of goodness, but if
  you wrote down all the things you want in a language, it's likely that in 2025, Rust in general makes better trades
  than Python does
* better: it's a lot newer! Rust 1.0 May 2015 vs. Feb 1991 for the first Python -- that's 25 years of stuff
  to learn from in language design, and computers today are more like computers from 2015 than computers today are like
  computers in 1991. Python obviously has some evolutionary scars (hi GIL!) that Rust doesn't. Rust *should* be better.
* Obviously *you* are not like past me, and you've got more than memes to justify whatever Rust rewrite you want, and
  you'd spend more than 10% of your time on it when you could find the time, and you'll have an easier time picking
  libraries and getting CI set up in 2025 for Rust than the time I had in 2018/2019 for Haskell, but

Despite all this, I think you shouldn't day dream about rewriting your least favorite service in Rust anyway.

**SLIDE**
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

<!--
* probably not: operationally significant memory management issues, ill-formed arguments in critical code paths,
  difficult software delivery; the reason these are probably not is that if your services are too bad at memory
  management, they fall over; if you can't detect ill-formed arguments in critical code paths, you spend all of your
  time on dumb bugs; and if you can't deliver software, you... can't deliver software? and you just don't have
  services/a job/a company anymore, depending on how hard it is for you to deliver software.
* there's a strong filter on technical stacks that work for building software to do jobs, which is that computers
  cost money, and your time costs money, and if the computers break too often or it's too hard to get the computers to
  do new things, companies stop spending money on the computers or the people getting the computers to do things.
  * this is my economic explanation for the ubiquity of barely good enough software tooling / the seeming permanence
    of python
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

. . .

```sixel
magick convert -resize 480 "utils.jpg" sixel:-
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
* 
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

## The Rust edit

* the traces above would be faster
* they'd be... memory... safer?
* they also wouldn't have runtime errors caused by invalid data being passed around?

<!--
* faster by some amount, maybe someone would notice? But not if _my_ slow code is the problem
* Probably it wouldn't be safer! There's the NSA thing that everyone got all excited about, but that
  also included Python, C#, Java, Go, and Swift in the recommendations. Where's my Java gang?
  https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/article/3608324/us-and-international-partners-issue-recommendations-to-secure-software-products/
* Maybe there wouldn't be runtime errors? I don't know enough about Rust to know about this, but everything deals
  with data from the real world at some point. I'd bet Rust has an easier time with Parse, Don't Validate
  than python does (it's awful in python, and especially awful in `pydantic`, but I know, no one asked), but bad
  input is still bad input.
-->

## How to choose a new language when you have production services to operate

* DON'T
* choose the language that your services are already running in

<!--
* really I think that's the whole decision tree -- KEEP GOING
* not just you, but *EVERYONE* will have to learn new testing frameworks, and new web frameworks, and a new CI setup,
  and new weird failure modes, and new auxiliary tools that can get out of sync on different developers' machines,
  and new weird stuff that goes wrong when the service has been mostly ignored for two months because it's been doing
  fine, and...
* there is _so much more_ of this than you think there is.
-->

# How to rewrite your service in Rust

## How to rewrite your service at all

## What happens when you're wrong?

## What happens when you're right?
<!--
OUTLINE

* given you want to migrate service A to service A' + service B, how do you know that service A' + service B = service A?
  * if you're EXTREMELY LUCKY -- the interfaces between service A and everything that talks to service A will make it obvious
    what you need to care about
  * you are not extremely lucky
  * two examples: `ground-comms`, missing downlinks V2 from scheduling -> processing; processing sending two messages
    _fast_ when the scheduling service was counting on it sending the two messages with a longer gap
    * first example -- giant object, not obvious which part is important where, message serving like a million purposes
    * second example -- again a giant object where processing workflow told scheduling "object x should have state y,"
      which was fine while the second message for a specific piece of object x (missing pulses) wasn't getting
      processed at the same time
  * YOU WILL BE WRONG. when you're wrong, someone is likely to get paged. if you're lucky, it will be you.
  * you are not extremely lucky. (sorry Eugene)
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
