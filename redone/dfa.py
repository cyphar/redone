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


class DFAException(Exception):
	pass


class DFANode(fsa.FSANode):
	"""
	Represents a node or state in a DFA graph. Due to the properties of directed
	graphs, *any* valid NFA node also describes a valid NFA graph.
	"""

	def __init__(self, tag="", accept=False):
		self._tag = tag
		self._accept = accept
		self._edges = {}

		self._sink = None

	def __repr__(self):
		return "<DFANode(tag=%r, accept=%r) at 0x%x>" % (self._tag, self._accept, id(self))

	def _move(self, token):
		"""
		Returns the node which will consume the given token during the transition
		from the current node. If no such node exists, then the DFA is not completely
		described and _move will raise a DFAException.
		"""

		if token not in self._edges:
			# Default to sink.
			if self._sink is not None:
				return self._sink

			# Oops!
			raise DFAException("Non-deterministic DFA node (missing edge '%s')." % token)

		return self._edges[token]

	def add_edge(self, label, node):
		"""
		Adds an edge to the current node with the given label to the given node. If
		there already is an edge with the given label, the DFA is non-deterministic
		and add_edge will raise a DFAException. It is an error to try to add an
		edge to a DFA node to something other than a DFA node.
		"""

		if not isinstance(node, DFANode):
			raise DFAException("Cannot add an NFA node edge to a non-NFA node.")

		if label in self._edges:
			raise DFAException("Non-deterministic DFA node (duplicate edge '%s')." % label)

		self._edges[label] = node

	def accepts(self, string):
		"""
		Returns true iff. the DFA graph (with the current node as the starting node)
		will consume the entire string and the ending node is an accepting node. If
		accepts detects that the DFA graph is not completely described, then it will
		raise a DFAException.
		"""

		state = self
		for token in string:
			next_state = self._move(token)

			if not next_state:
				break

			state = next_state

		return state._accept
