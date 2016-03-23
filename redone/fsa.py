#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

class FSANode(object):
	"""
	Base class for both DFA and NFA nodes.
	"""

	def accepts(self, string):
		raise NotImplementedError

	def add_edge(self, label, node):
		raise NotImplementedError
