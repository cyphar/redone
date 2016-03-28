#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Aleksa Sarai

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import collections

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

		self._sink = None
		self._edges = collections.defaultdict(self._get_sink)

	def __repr__(self):
		return "<DFANode(tag=%r, accept=%r) at 0x%x>" % (self._tag, self._accept, id(self))

	def _get_sink(self):
		return self._sink

	def move(self, token):
		"""
		Returns the node which will consume the given token during the transition
		from the current node. If no such node exists, then the DFA is not completely
		described and _move will raise a DFAException.
		"""

		# Oops!
		if self._edges[token] is None:
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
		end = -1

		for index, token in enumerate(string):
			next_state = state.move(token)

			# Landed on an accepting state.
			if next_state._accept:
				end = index + 1

			state = next_state

		return end
