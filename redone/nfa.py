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

EPSILON_EDGE = ""

def _epsilon_closure(states):
	"""
	For a given set of NFA node states, return a set that describes the epsilon
	closure of all of the given states.
	"""

	epsilons = set()

	for state in states:
		epsilons |= state._epsilon_closure()

	return epsilons

def _move(states, token):
	"""
	For a given set of NFA node states, return a set that describes the states
	occupied after transitioning across all edges labeled with the given token.
	"""

	moved = set()

	for state in states:
		moved |= state._move(token)

	return moved

def _accept(states):
	"""
	For a given set of NFA node states, return true if any of the given states
	are accepting nodes (otherwise return false).
	"""

	return any(state._accept for state in states)


class NFAException(Exception):
	pass


class NFANode(object):
	"""
	Represents a node or state in an NFA graph. Due to the properties of directed
	graphs, *any* valid NFA node also describes a valid NFA graph.
	"""

	def __init__(self, tag="", accept=False):
		self._tag = tag
		self._accept = accept
		self._edges = {}

	def __repr__(self):
		return "<NFANode(tag=%r, accept=%r) at 0x%x>" % (self._tag, self._accept, id(self))

	def _epsilon_closure(self, states=None):
		"""
		Returns the set of all states connected via epsilon edges to the current
		state (as well as including the current state).
		"""

		if not states:
			states = {self}

		for node in self._edges.get(EPSILON_EDGE, set()):
			# Avoid infinite recursion.
			if node in states:
				continue

			# Add found node to set of states.
			states.add(node)

			# Recursively calculate its epsilon closure and add it to the set of states.
			states |= node._epsilon_closure(states)

		return states

	def _move(self, token):
		"""
		Returns the set of states which will consume the given token during the
		transition. In other words, this will give you the set of states that you
		inhabit after transitioning from the current state along all edges that accept
		the given token.
		"""

		states = set()

		# Get set of states from epsilons which can consume the given token.
		for state in self._epsilon_closure():
			states |= state._edges.get(token, set())

		# Get all epsilon closures for the given states.
		return _epsilon_closure(states)

	def add_edge(self, label, node):
		"""
		Adds an edge to the current state. It is an error to try to add an edge to
		something other than an NFANode. If the label is '%s', then the edge is
		treated as an epsilon edge (it consumes no tokens when transitioning through
		it).
		""" % (EPSILON_EDGE)

		if not isinstance(node, NFANode):
			raise NFAException("Cannot add an NFA node edge to a non-NFA node.")

		if label not in self._edges:
			self._edges[label] = set()

		self._edges[label].add(node)

	def accepts(self, string):
		"""
		Returns true iff. the NFANode graph (where the current state is the start
		node) will consume the given string and end on an accepting node.
		"""

		states = self._epsilon_closure()

		for token in string:
			next_states = _move(states, token)

			# If there are no next states, you cannot possibly match it.
			# XXX: This might need to be remove to allow for partial matches.
			if not next_states:
				return False

			states = next_states

		return _accept(states)

	def _get_lasts(self, seen=None):
		"""
		This returns all of the accepting nodes in the given NFA graph, starting at
		the current node.
		"""

		if not seen:
			seen = {self}

		lasts = set()

		# If current node is an accepting node, it is  a "last".
		if self._accept:
			lasts.add(self)

		for _, nodes in self._edges.items():
			for node in nodes:
				# Avoid infinite recursion.
				if node in seen:
					continue

				# Add node to list of seen nodes.
				seen.add(node)

				# Recursively find all accepting node and add them to the set.
				lasts |= node._get_lasts(seen)

		return lasts

	def patch(self, node, label=EPSILON_EDGE):
		"""
		This causes every accepting node in the given NFA graph to be changed to
		a non-accepting node with an edge with the given label to the given node. This
		is used when joining two NFA graphs.
		"""

		lasts = self._get_lasts()

		if not lasts:
			raise NFAException("Cannot patch an NFA graph with no accepting nodes.")

		for last in lasts:
			last._accept = False
			last.add_edge(label, node)

if __name__ == "__main__":
	pass
