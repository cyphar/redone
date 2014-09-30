#!/usr/bin/env python3

from . import regex

__all__ = ["compile", "match"]

class RegexMatcher(object):
	"""
	Wrapper for an internal structure which represents a regular expression
	finite state automata.
	"""

	def __init__(self, graph):
		self._graph = graph

	def match(self, string):
		return self._graph.accepts(string)

def compile(pattern):
	"""
	Compile a regular expression into a RegexMatcher which can be used to match
	any given string.
	"""

	graph = regex.compile_regex(pattern)
	matcher = RegexMatcher(graph)

	return matcher

def match(pattern, string):
	"""
	Matches a given string against a given regex pattern.
	"""

	return regex.compile_regex(pattern).accepts(string)
