redone
======

A correct implementation of regular expressions, using finite state automata
rather than backtracking.

## tl;dr ##
All regex implementations (except for GNU grep, GNU awk and a few others) use
backtracking, which (while adding support for backreferences) massively reduces
the efficiency of the implementation. Even the best backtracking implementations
have `O(2^n)` time complexity in several cases.

On the other hand, by using finite state automata, regular expression matching
can have `O(n)` time complexity (or possibly superlinear, if the implementation
uses NFAs and doesn't cache them to produce DFAs). In either case, the
differences [can be quite drastic](http://swtch.com/~rsc/regexp/regexp1.html).

## Usage ##
To use this, you just need to do the following:

```python3
>>> import redone
>>>
>>> pattern = "some pattern here"
>>> string = "some string here"
>>>
>>> # Pre-compiled version (recommended).
>>> r = redone.compile(pattern)
>>> r.match(string)
# => True or False
>>>
>>> # On-the-fly version.
>>> redone.match(pattern, string)
# => True or False
```

Support for things like `findall`, `search` and groups are in the works.

## Warnings ##
* This was made in order to prove a point (and as a programming exercise).
  Python's mantra is that it is "fast enough". It is possible to argue that
  using the well-tested `re` module is *much safer* than using an implementation
  some random on the internet wrote, and that the speed issue isn't a big deal
  on most regular expressions.
* I have yet to implement character sets (`[abc]` and `[^abc]`), wildcard matches
  (`.`) and a few other **necessary** features.
* Not suitable for programmers under the age of 3.
