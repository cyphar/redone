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


class Parser(object):
	"""
	Abstract parser class.
	"""

	ALPHABET = constants.ALPHABET
	METACHARS = constants.METACHARS
	SETMETA = constants.SETMETA

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

	def parse(self):
		raise NotImplementedError

class RegexParser(Parser):
	"""
	An object used internally within redone in order to parse regular expressions
	and convert them into the equivalent NFANode graph. This is an implementation
	of a recursive descent parser which will parse valid regex.
	"""

	# EBNF for 'redone' extended regex:
	# <re>        ::= <simple> ( "|" <re> )?
	# <simple>    ::= <basic>+
	# <basic>     ::= <elem> ("*" | "+" | "?")?
	# <elem>      ::= "(" <re> ")"
	# <elem>      ::= "[" "^"? <set-token>+ "]"
	# <elem>      ::= "."
	# <elem>      ::= <token>
	# <token>     ::= "\" ("^" | "." | "*" | "+" | "?" | "(" | ")" | "[" | "]" | "|" | "\")
	# <token>     ::= ¬("^" | "." | "*" | "+" | "?" | "(" | ")" | "[" | "]" | "|" | "\")
	# <set-token> ::= "\" ("[" | "]" | "\")
	# <set-token> ::= ¬("[" | "]" | "\")

	def _parse_set_token(self):
		# Metacharacter Escapes
		if self.peek() == "\\":
			self.next()

			token = self.peek()
			self.next()

			if token not in self.SETMETA:
				raise RegexParseException("Invalid escape sequence: %s." % ('\\' + token))

			return token

		elif self.peek() not in self.SETMETA:
			token = self.peek()
			self.next()

			return token

	def _parse_token(self):
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

			token = self._parse_set_token()

			if token is None:
				raise RegexParseException("Empty regex set.")

			tokens = {token}
			while not self.end() and self.peek() != "]":
				token = self._parse_set_token()

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
			token = self._parse_token()

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


class SimplifyParser(Parser):
	"""
	Parser used to simplify regex expressions to a format which can be understood
	by the RegexParser.
	"""

	# Repetition types.
	ITER_SET = 0       # <simple>{<n>}
	ITER_UNLIMITED = 1 # <simple>{<n>,}
	ITER_FULL = 2      # <simple>{<n>,<m>}

	# EBNF for Simplify Parser
	# <re>     ::= <full> ("|" <re>)?
	# <full>   ::= <basic>+
	# <basic>  ::= <simple> ("*" | "+" | "?" | <iter>)?
	# <iter>   ::= "{" <number> ("," <number>?)? "}"
	# <simple> ::= "(" <re> ")"
	# <simple> ::= "[" "^"? <set-token>+ "]"
	# <simple> ::= <token>

	def _parse_set_token(self):
		# Metacharacter escapes.
		if self.peek() == "\\":
			self.next()

			token = self.peek()
			self.next()

			if token not in self.SETMETA:
				raise RegexParseException("Invalid escape sequence: %s." % ('\\' + token))

			return "\\" + token

		# All other characters.
		elif self.peek() not in self.SETMETA:
			token = self.peek()
			self.next()

			return token

	def _parse_token(self):
		# Metacharacter escapes.
		if self.peek() == "\\":
			self.next()

			token = self.peek()
			self.next()

			if token not in self.METACHARS:
				raise RegexParseException("Invalid escape sequence: %s." % ('\\' + token))

			return "\\" + token

		# All other characters.
		elif self.peek() not in self.METACHARS:
			token = self.peek()
			self.next()

			return token

	def _parse_simple(self):
		# Groups.
		if self.peek() == "(":
			item = self.peek()
			self.next()

			item += self._parse_full()

			if self.peek() != ")":
				raise RegexParseException("Missing closing ')' in regex group.")
			item += self.peek()
			self.next()

			return item

		# Sets.
		elif self.peek() == "[":
			item = self.peek()
			self.next()

			if self.peek() == "^":
				item += self.peek()
				self.next()

			token = self._parse_set_token()

			if token is None:
				raise RegexParseException("Empty regex set.")

			item += token
			while not self.end() and self.peek() != "]":
				token = self._parse_set_token()

				if token is None:
					break

				item += token

			if self.peek() != "]":
				raise RegexParseException("Missing closing ']' in regex set.")
			item += self.peek()
			self.next()

			return item

		# Wildcards.
		elif self.peek() == ".":
			item = self.peek()
			self.next()

			return item

		# Other.
		else:
			token = self._parse_token()

			if token is None:
				return None

			return token

	def _parse_number(self):
		# Special case: leading zero is only the number 0.
		if self.peek() == "0":
			self.next()
			return 0

		# No digit => not a number.
		if self.peek() not in "0123456789":
			return None

		out = 0
		while self.peek() in "0123456789":
			digit = self.peek()
			self.next()

			# Shift rest up one place and add digit.
			out *= 10
			out += int(digit)

		return out

	def _parse_iter(self):
		# Counted repetition.
		if self.peek() == "{":
			self.next()

			_type = None
			n = self._parse_number()
			m = None

			if n is not None:
				_type = self.ITER_SET

			# Different form -- {n,m}.
			if self.peek() == ",":
				self.next()

				m = self._parse_number()

				if n is not None:
					_type = self.ITER_FULL

				if m is None:
					_type = self.ITER_UNLIMITED

				# Ensure values make sense.
				if _type == self.ITER_FULL and m < n:
					raise RegexParseException("Invalid values for {n,m} counted repetition.")

			if _type is None:
				raise RegexParseException("Invalid counted repitition format.")

			if self.peek() != "}":
				raise RegexParseException("Missing in closing '}' in counted repetition.")
			self.next()

			# Give the type data and {min,max} data.
			return (_type, n or 0, m or 0)

	def _parse_basic(self):
		item = self._parse_simple()

		if item is None:
			return None

		# Standard modifiers.
		if self.peek() in ["*", "+", "?"]:
			item += self.peek()
			self.next()

			return item

		_iter = self._parse_iter()

		if _iter is None:
			return item

		repeat = ""
		_type, n, m = _iter

		# Repeat "minimum".
		for _ in range(n):
			repeat += item

		# No limit -- just add plus.
		if _type == self.ITER_UNLIMITED:
			return repeat + "+"

		# Repeat "optional" maximum.
		for _ in range(m - n):
			repeat += item + "?"

		return repeat

	def _parse_re(self):
		basics = self._parse_basic()

		if basics is None:
			return None

		# Get basics.
		while not self.end():
			basic = self._parse_basic()

			if basic is None:
				break

			basics += basic

		return basics

	def _parse_full(self):
		item = self._parse_re()

		# Unions.
		if self.peek() == "|":
			item += self.peek()
			self.next()

			right = self._parse_full()
			if right is None:
				raise RegexParseException("Union without right side in expression.")

			item += right

		return item

	def parse(self):
		"""
		Parses a regular expression and produces a "simplified" version which can be
		understood by RegexParser.
		"""

		if not self._tokens:
			return ""

		pattern = self._parse_full()

		if pattern is None:
			raise RegexParseException("Unknown error occurred when simplifying regular expression.")

		# Pattern *must* be consumed.
		if not self.end():
			raise RegexParseException("Trailing characters in regular expression.")

		return pattern

def _parse(pattern):
	"""
	Compile a given pattern into an NFA which represents the pattern's state
	machine. The return statement is an NFANode graph which will match according
	to the pattern's rules. The pattern is first "simplified" in order to all for
	pre-parse checks and optimisations to patterns.
	"""

	pattern = SimplifyParser(list(pattern)).parse()
	tokens = list(pattern)

	return RegexParser(tokens).parse()
