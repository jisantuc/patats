---
title: Error Aggregation 101
author: James Santucci
patat:

    wrap: true
    margins:
        left: 5
        right: 5

---

# ⚡️ Error Aggregation 101 ⚡️

## The public goal

- understand narratives about what goes wrong when things go wrong
- how teams discover and prioritize bugs that affect multiple projects

## The secret goal

- uncover secret effective practices for managing Rollbar noise and preventing errors from occurring in the first place

## Assumptions

- Rollbar widely used across projects
- Weighted by usage, types reduce the total count of errors
- Weighting by usage is even possible

## How do people use Rollbar where it's present?

- differs widely across levels, across projects, and across languages and frameworks

## What are alternatives

- goal is to find out when something has gone wrong -- how else do we find out?
> - _sometimes when users / clients tell us_

## What did I end up learning

> - prod debugging is a skill that's aided by well organized available data
> - it would be good to be able to explicitly train prod debugging -- maybe add an actually broken toy to breakable toys for onboarding
> - even for standard tools, there's still wide variation in use across teams
> - even where we're using Rollbar **well**, devs are always required to estimate severity of report
> - there's a shared sentiment that _something is missing_ in the information we get from prod, but no consensus on what that might be

## What do we do

> - start with Rollbar everywhere -- there's a really generous free tier
> - think about PAGNIs -- "probably are gonna need its" -- especially where they're expensive to add later
> - find a way to train prod debugging, since the perfect prod error is probably not magically going to happen