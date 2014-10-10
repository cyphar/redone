#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# 1. The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
