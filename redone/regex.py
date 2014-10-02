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
from . import constants


class RegexParseException(Exception):
	pass


class RegexParser(object):
	"""
	An object used internally within redone in order to parse regular expressions
	and convert them into the equivalent NFANode graph. This is an implementation
	of a recursive descent parser which will parse valid regex.
	"""

	# EBNF for 'redone' extended regex:
	# <re>     ::= <simple> ( "|" <re> )?
	# <simple> ::= <basic>+
	# <basic>  ::= <elem> ("*" | "+" | "?")?
	# <elem>   ::= "(" <re> ")"
	# <elem>   ::= "[" "^"? <token>+ "]"
	# <elem>   ::= "."
	# <elem>   ::= <token>
	# <token>  ::= "\" ("^" | "." | "*" | "+" | "?" | "(" | ")" | "[" | "]" | "|" | "\")
	# <token>  ::= ¬("^" | "." | "*" | "+" | "?" | "(" | ")" | "[" | "]" | "|" | "\")

	ALPHABET = constants.ALPHABET
	METACHARS = constants.METACHARS

	def __init__(self, tokens, alphabet=None, metachars=None):
		self._tokens = tokens
		self._pos = 0
		self._length = len(tokens)

		if alphabet:
			self.ALPHABET = set(alphabet)

		if metachars:
			self.METACHARS = set(metachars)

	def end(self):
		"""
		Returns whether or not the parser state is at the end of the tokens.
		"""

		return self._pos == self._length

	def peek(self):
		"""
		Returns the current token in the parser state.
		"""

		if not self.end():
			return self._tokens[self._pos]

	def next(self, num=1):
		"""
		Advances the parser state forward by num tokens. Raises an error if the
		new parser state is out-of-bounds in the token list.
		"""

		if not self.end():
			self._pos += num

	def _parse_char(self):
		# Metacharacter Escapes
		if self.peek() == "\\":
			self.next()

			token = self.peek()
			self.next()

			if token not in self.METACHARS:
				raise RegexParseException("Invalid escape sequence: %s." % ('\\' + token))

			return token

		# All other characters.
		elif self.peek() not in self.METACHARS:
			token = self.peek()
			self.next()

			return token

	def _parse_elem(self):
		start = nfa.NFANode(tag="elem_start", accept=False)
		end = nfa.NFANode(tag="elem_end", accept=True)

		# Groups
		if self.peek() == "(":
			self.next()

			graph = self._parse_re()

			if self.peek() != ")":
				raise RegexParseException("Missing closing ')' in regex group.")
			self.next()

			# Make graph link with the start and end.
			start.add_edge(nfa.EPSILON_EDGE, graph)
			graph.patch(end, label=nfa.EPSILON_EDGE)

		# Sets.
		elif self.peek() == "[":
			inverted = False
			self.next()

			if self.peek() == "^":
				inverted = True
				self.next()

			token = self._parse_char()

			if token is None:
				raise RegexParseException("Empty regex set.")

			tokens = {token}
			while not self.end() and self.peek() != "]":
				token = self._parse_char()

				if token is None:
					break

				tokens.add(token)


			if self.peek() != "]":
				raise RegexParseException("Missing closing ']' in regex set.")
			self.next()

			# We want the inverse of the given character set.
			# Just XOR with the alphabet.
			if inverted:
				tokens = self.ALPHABET ^ tokens

			# Add all given tokens as edges to the end.
			for token in tokens:
				start.add_edge(token, end)

		# Wildcard.
		elif self.peek() == ".":
			self.next()

			for token in self.ALPHABET:
				start.add_edge(token, end)

		# All other characters.
		else:
			token = self._parse_char()

			if token is None:
				return None

			# Connect start and end with an edge with label=token.
			start.add_edge(token, end)

		return start

	def _parse_basic(self):
		node = self._parse_elem()

		if self.peek() in ["*", "+", "?"]:
			if node is None:
				raise RegexParseException("Modifier applied to a non-element.")

			modifier = self.peek()
			self.next()

			# Set up new start and end nodes.
			start = nfa.NFANode(tag="modifier_start", accept=False)
			end = nfa.NFANode(tag="modifier_end", accept=True)

			# Attach element to start and end.
			start.add_edge(nfa.EPSILON_EDGE, node)
			node.patch(end, label=nfa.EPSILON_EDGE)

			# Kleene Star
			# Connect the start and end node with epsilon edges (bidirectional).
			if modifier == "*":
				start.add_edge(nfa.EPSILON_EDGE, end)
				end.add_edge(nfa.EPSILON_EDGE, start)

			# Kleene Plus
			# Connect the end node to the start node with an epsilon edge.
			elif modifier == "+":
				end.add_edge(nfa.EPSILON_EDGE, start)

			# Optional
			# Connect the start node to the end node with an epsilon edge.
			elif modifier == "?":
				start.add_edge(nfa.EPSILON_EDGE, end)

			# Shouldn't ever reach this.
			else:
				raise RegexParseException("Unknown modifier.")

			# Update node to point to the start of the modifier.
			node = start

		if node is None:
			return None

		return node

	def _parse_simple(self):
		node = self._parse_basic()

		if node is None:
			return None

		while not self.end():
			right = self._parse_basic()

			if right is None:
				break

			# Concatinate nodes.
			node.patch(right, label=nfa.EPSILON_EDGE)

		return node

	def _parse_re(self):
		node = self._parse_simple()

		if node is None:
			return None

		if self.peek() == "|":
			self.next()

			left = node
			right = self._parse_re()

			if right is None:
				raise RegexParseException("Union without right side in expression.")

			# Create new starting and accepting nodes.
			start = nfa.NFANode(tag="union_start", accept=False)
			end = nfa.NFANode(tag="union_end", accept=True)

			# Add links to left and right.
			start.add_edge(nfa.EPSILON_EDGE, left)
			start.add_edge(nfa.EPSILON_EDGE, right)

			# Update left and right to point to the new end.
			left.patch(end, label=nfa.EPSILON_EDGE)
			right.patch(end, label=nfa.EPSILON_EDGE)

			# Update node to point to the new start node.
			node = start

		return node

	def parse(self):
		"""
		Parses a regular expression and produces an NFANode graph that represents that
		will match text according to the given regex rules.
		"""

		# Special case -- empty patterns produce a graph which will only match ""
		if not self._tokens:
			return nfa.NFANode(tag="empty_graph", accept=True)

		graph = self._parse_re()

		if graph is None:
			raise RegexParseException("Unknown error occurred.")

		return graph

def _optimise(pattern):
	# TODO: Optimise and expand patterns.
	return pattern

def _compile(pattern):
	"""
	Compile a given pattern into an NFA which represents the pattern's state
	machine. The return statement is an NFANode graph which will match according
	to the pattern's rules.
	"""

	pattern = _optimise(pattern)

	if not pattern:
		raise RegexParseException("Error encountered when optimising pattern.")

	tokens = list(pattern)
	parser = RegexParser(tokens)

	return parser.parse()
