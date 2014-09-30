#!/usr/bin/env python3

EPSILON_EDGE = ""


class NFAException(Exception):
	pass


class NFANode(object):
	"""
	Represents a node or state in an NFA graph. Due to the properties of directed
	graphs, *any* valid NFA node also describes a valid NFA graph.
	"""

	def __init__(self, tag="", accept=False):
		self._tag = tag
		self._accept = accept or False

		self._edges = {}

	def __repr__(self):
		return "NFANode(tag=%r, accept=%r)" % (self._tag, self._accept)

	def _epsilon_states(self, states=None):
		"""
		Returns the set of all states connected via epsilon edges to the current
		state (as well as including the current state).
		"""

		if not states:
			states = {self}

		for node in self._edges.get(EPSILON_EDGE, set()):
			# Stop recursive epsilon expansions.
			if node in states:
				continue

			states.add(node)
			states |= node._epsilon_states(states.copy())

		return states

	def _match_token(self, token):
		"""
		Returns the set of states which will consume the given token during the
		transition. In other words, this will give you the set of states that you
		inhabit after transitioning from the current state along all edges that accept
		the given token.
		"""

		next_states = set()
		states = self._epsilon_states()

		# Exact token matches.
		for state in states:
			next_states |= state._edges.get(token, set())

		return next_states

	def add_edge(self, label, node):
		"""
		Adds an edge to the current state. It is an error to try to add an edge to
		something other than an NFANode.

		If the label is '%s', then the edge is treated as an epsilon edge (it consumes
		no tokens when transitioning through it).
		""" % (EPSILON_EDGE)

		if not isinstance(node, NFANode):
			raise NFAException("Cannot add an NFA node edge to a non-NFA node.")

		if label not in self._edges:
			self._edges[label] = set()

		self._edges[label].add(node)

	def accepts(self, string):
		"""
		Returns True iff. the NFANode graph (where the current state is the start
		node) will consume the given string and end on an accepting node.
		"""

		current_states = {self}

		start = 0
		while start < len(string):
			next_states = set()

			for node in current_states:
				next_states |= node._match_token(string[start])

			# If there are no next states, you cannot possibly match it.
			if not next_states:
				return False

			current_states = next_states
			start += 1

		return any(node._accept for node in current_states)

	def _get_lasts(self, seen=None):
		"""
		This returns all of the accepting nodes in the given NFA graph, starting at
		the current node.
		"""

		if not seen:
			seen = {self}

		lasts = set()

		if self._accept:
			lasts.add(self)

		for _, nodes in self._edges.items():
			for node in nodes:
				# Avoid recursive expansions.
				if node in seen:
					continue

				seen.add(node)
				lasts |= node._get_lasts(seen.copy())

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
