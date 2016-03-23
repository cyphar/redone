#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import collections
from . import fsa

EPSILON_EDGE = ""

CACHE_MOVE = 0

def _epsilon_closures(states):
	"""
	For a given set of NFA node states, return a set that describes the epsilon
	closure of all of the given states.
	"""

	epsilons = set()

	for state in states:
		epsilons |= state._epsilon_closure()

	return epsilons

def _moves(states, token):
	"""
	For a given set of NFA node states, return a set that describes the states
	occupied after transitioning across all edges labeled with the given token.
	"""

	moved = set()

	for state in states:
		moved |= state.move(token)

	return moved

def _accepts(states):
	"""
	For a given set of NFA node states, return true if any of the given states
	are accepting nodes (otherwise return false).
	"""

	return any(state._accept for state in states)


class NFAException(Exception):
	pass


class NFANode(fsa.FSANode):
	"""
	Represents a node or state in an NFA graph. Due to the properties of directed
	graphs, *any* valid NFA node also describes a valid NFA graph.
	"""

	def __init__(self, tag="", accept=False):
		self._tag = tag
		self._accept = accept
		self._edges = {}

		# Used to check for cache invalidation.
		self._canary = {
			CACHE_MOVE: {},
		}

		# The actual cache.
		self._cache = {
			CACHE_MOVE: {},
		}

	def __repr__(self):
		return "<NFANode(tag=%r, accept=%r) at 0x%x>" % (self._tag, self._accept, id(self))

	def _epsilon_closure(self):
		"""
		Returns the set of all states connected via epsilon edges to the current
		state (as well as including the current state).
		"""

		# Basically a breadth-first search because it removes the overhead of recursive
		# calls. But we aren't searching, just storing all nodes found in the path.

		states = {self}
		todo = collections.deque([self])

		# Still more epsilons to find.
		while todo:
			current = todo.pop()

			# Get set of epsilon transitions from current node.
			epsilons = current._edges.get(EPSILON_EDGE)

			if not epsilons:
				continue

			# Add all nodes which haven't already been seen to the list of states and
			# to the list of nodes left to search.
			for node in epsilons.difference(states):
				todo.append(node)
				states.add(node)

		return states

	def move(self, token):
		"""
		Return the set of states inhabited after transitioning from the current state
		along all edges that accept the given token (with epsilon closures).
		"""

		# Only fetch from cache if no changes since last cache write.
		if self._canary[CACHE_MOVE].get(token) and token in self._cache[CACHE_MOVE]:
			return self._cache[CACHE_MOVE][token]

		states = self._move(token)

		# Add to cache.
		self._canary[CACHE_MOVE][token] = True
		self._cache[CACHE_MOVE][token] = states

		return states

	def _move(self, token):
		states = set()

		# Get set of states from epsilons which can consume the given token.
		for state in self._epsilon_closure():
			states |= state._edges.get(token, set())

		# Get all epsilon closures for the given states.
		states = _epsilon_closures(states)
		return states

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

		# New epsilon edges completely break the move cache, but other edges only
		# break the cache for that specific label.
		if label == EPSILON_EDGE:
			self._canary[CACHE_MOVE] = {}
		else:
			self._canary[CACHE_MOVE][label] = False

		# Add edge to given node with given label.
		self._edges[label].add(node)

	def accepts(self, string):
		"""
		Returns the right-most index of the given string which, when consumed by the
		NFA graph, ends on an accepting node. If no such index exists, accepts returns
		-1.
		"""

		states = self._epsilon_closure()
		end = -1

		for index, token in enumerate(string):
			next_states = _moves(states, token)

			# Landed on an accepting set of states.
			if _accepts(next_states):
				end = index + 1

			# If there are no next states, we cannot proceed further.
			if not next_states:
				break

			states = next_states

		return end

	def _get_lasts(self, seen=None):
		"""
		This returns all of the accepting nodes in the given NFA graph, starting at
		the current node.
		"""

		# Basically a breadth-first search because it removes the overhead of recursive
		# calls. But we aren't searching, just storing all nodes found in the path.

		lasts = set()

		seen = {self}
		todo = collections.deque([self])

		# Still more nodes to find.
		while todo:
			current = todo.pop()

			if current._accept:
				lasts.add(current)

			# Get set of epsilon transitions from current node.
			for _, nodes in current._edges.items():
				for node in nodes.difference(seen):
					todo.append(node)
					seen.add(node)

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

		# Update all lasts.
		for last in lasts:
			last._accept = False
			last.add_edge(label, node)
