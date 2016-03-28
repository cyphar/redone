#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Aleksa Sarai

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from . import conv
from . import parser
from . import regex

__all__ = ["compile", "match", "fullmatch", "search"]

def _compile(pattern, _convert=False):
	graph = parser._parse(pattern)

	if _convert:
		graph = conv.nfa2dfa(graph)

	return regex.RegexMatcher(graph)

def compile(pattern):
	"""
	Compile the given regular expression into a RegexMatcher which can be used to
	run regex operations on any given string without needing to recompile the
	expression.
	"""

	return _compile(pattern, _convert=True)

def match(pattern, string):
	"""
	Partial matches the given string against the given regex pattern. It returns
	either the slice of the partial match or None if not matched.
	"""

	if isinstance(pattern, regex.RegexMatcher):
		return pattern.match(string)

	# Avoid overhead of converting the NFA (one-time use only).
	reo = _compile(pattern, _convert=False)

	# Forward to RegexMatcher.
	return reo.match(string)

def fullmatch(pattern, string):
	"""
	Fully matches a given string against a given regex pattern. It returns either
	the slice of the match (the given string) or None if not matched.
	"""

	if isinstance(pattern, regex.RegexMatcher):
		return pattern.fullmatch(string)

	# Avoid overhead of converting the NFA (one-time use only).
	reo = _compile(pattern, _convert=False)

	# Forward to RegexMatcher.
	return reo.fullmatch(string)

def search(pattern, string):
	"""
	Searches the given string for a match against the given regex pattern. It
	returns either the slice of the left-most match or None if there was no match.
	"""

	if isinstance(pattern, regex.RegexMatcher):
		return pattern.search(string)

	# Avoid overhead of converting the NFA (one-time use only).
	reo = _compile(pattern, _convert=False)

	# Forward to RegexMatcher.
	return reo.search(string)

def finditer(pattern, string):
	"""
	Finds all non-overlapping matches for the pattern in the string. This returns
	a generator which will yield results.
	"""

	if isinstance(pattern, regex.RegexMatcher):
		return pattern.finditer(string)

	# Avoid overhead of converting the NFA (one-time use only).
	reo = _compile(pattern, _convert=False)

	# Forward to RegexMatcher.
	return reo.finditer(string)

def findall(pattern, string):
	"""
	Finds all non-overlapping matches for the pattern in the string. This returns
	a list of results.
	"""

	if isinstance(pattern, regex.RegexMatcher):
		return pattern.finditer(string)

	# Avoid overhead of converting the NFA (one-time use only).
	reo = _compile(pattern, _convert=False)

	# Forward to RegexMatcher.
	return reo.findall(string)

def sub(pattern, replace, string):
	"""
	Replaces all occurences of the pattern in the string with the given
	replacement.
	"""

	if isinstance(pattern, regex.RegexMatcher):
		return pattern.sub(replace, string)

	# Avoid overhead of converting the NFA (one-time use only).
	reo = _compile(pattern, _convert=False)

	# Forward to RegexMatcher.
	return reo.sub(replace, string)
