#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from . import fsa
import types

def is_callable(obj):
	return type(obj) in (types.FunctionType, types.LambdaType)

class RegexMatch(object):
	def __init__(self, string, start, end, groups=None):
		self._slice = string[start:end]
		self._start = start
		self._end = end
		self._groups = groups or []

	def __repr__(self):
		return "<RegexMatch(%r, %r) %r>" % (self._start, self._end, self._slice)

	def group(self):
		return self._slice

	def groups(self, index):
		if index < len(self._groups):
			return self._groups[index]

class RegexMatcher(object):
	"""
	Wrapper for an internal structure which represents a regular expression
	finite state automata.
	"""

	def __init__(self, graph):
		if not issubclass(type(graph), fsa.FSANode):
			raise ValueError("Cannot use non-automata node graph as matcher graph.")

		self._graph = graph

	def match(self, string):
		"""
		Wraps the internal structure's matching methods.
		"""

		end = self._graph.accepts(string)

		# No match.
		if end < 0:
			return None

		return RegexMatch(string, 0, end)

	def fullmatch(self, string):
		"""
		Wraps the internal structure's full matching methods.
		"""

		end = self._graph.accepts(string)

		# Incomplete match.
		if end != len(string):
			return None

		return RegexMatch(string, 0, end)

	def search(self, string):
		"""
		Wraps the internal structure's searching methods.
		"""

		start = delta = -1

		while delta < 0 and len(string) > start:
			start += 1
			delta = self._graph.accepts(string[start:])

		if delta < 0:
			return None

		return RegexMatch(string, start, start + delta)

	def finditer(self, string):
		"""
		Wraps the internal structure's finditer methods.
		"""

		start = -1

		while start < len(string):
			delta = -1

			while delta < 0:
				start += 1

				if start >= len(string):
					break

				delta = self._graph.accepts(string[start:])

			if delta < 0:
				break

			yield RegexMatch(string, start, start + delta)
			start += delta - 1

	def findall(self, string):
		"""
		Wraps the internal structure's findall methods.
		"""

		return list(self.finditer(string))

	def sub(self, replace, string):
		"""
		Wraps the internal structure's substitution methods.
		"""

		last = 0
		out = ""

		repl = replace
		for match in self.finditer(string):
			out += string[last:match._start]

			# Callable replaces based on match.
			if is_callable(replace):
				repl = replace(match)

			out += repl
			last = match._end

		out += string[last:]
		return out
