#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from . import nfa
from . import dfa
from . import constants

def _all_edges(states):
	"Get all edges from all states."

	tokens = set()

	for state in states:
		tokens |= set(key for key, value in state._edges.items() if key != nfa.EPSILON_EDGE)

	return tokens

def nfa2dfa(graph):
	"""
	Converts an NFA graph to a DFA graph using the NFA deterministation algorithm.
	The returned graph is a DFA graph which will accept *precisely* the same
	languages. This massively improves the run-time performance of evaluation (at
	some 'compile-time' cost when running this function), since there is no need to
	emulate multiple states or recursively evaluate epsilon edges.
	"""

	if not isinstance(graph, nfa.NFANode):
		raise TypeError("Invalid graph type for NFA determinisation algorithm.")

	# Get the set of initial states and the initial DFA node.
	states = frozenset(graph._epsilon_closure())
	new_graph = dfa.DFANode(tag=states, accept=nfa._accepts(states))

	# Sink -- where all edges go to die.
	sink = dfa.DFANode(tag="sink", accept=False)
	for token in constants.ALPHABET:
		sink.add_edge(token, sink)

	seen = {states: new_graph}
	todo = [new_graph]

	while todo:
		# Get next node to create edges for.
		todo_node = todo.pop()
		states = todo_node._tag

		# Add sink node.
		todo_node._sink = sink

		# Ensure that each node has an edge the is in on of each of the states.
		for token in _all_edges(states):
			# Get set of states which are occupied after consuming the token.
			s = nfa._moves(states, token)
			s = frozenset(nfa._epsilon_closures(s))

			# No states -- just forward to the sink.
			if not s:
				todo_node.add_edge(token, sink)
				continue

			# New set of NFA states -- create a new DFA node to describe it.
			if s not in seen:
				node = dfa.DFANode(tag=s, accept=nfa._accepts(s))
				todo.append(node)
				seen[s] = node

			# Use pre-existing DFA node.
			else:
				node = seen[s]

			# Add edge for given token.
			todo_node.add_edge(token, node)

	return new_graph
