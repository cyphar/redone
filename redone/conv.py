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

from . import nfa
from . import dfa
from . import constants

# TODO(cyphar): Make the conversion faster (it makes the benchmarks *slower*
#               than the standard library).

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

		# Ensure that each node has an edge for every token in the alphabet.
		for token in constants.ALPHABET:
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
