#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import redone

SUITES = [
	{
		"pattern": r"a?b+c*",
		"replace": lambda match: "<%s>" % (match.group().upper()),
		"cases": {
			"abcxcbabcxxbc": "<ABC>xc<B><ABC>xx<BC>",
			"aaaa": "aaaa",
			"bbbb": "<BBBB>",
		}
	},

	{
		"pattern": r"a?b+c*",
		"replace": "<...>",
		"cases": {
			"abcxcbabcxxbc": "<...>xc<...><...>xx<...>",
			"aaaa": "aaaa",
			"bbbb": "<...>",
		}
	},
]

def _test_sub_compile():
	for suite in SUITES:
		pattern = suite["pattern"]
		replace = suite["replace"]
		cases = suite["cases"]

		r = redone.compile(pattern)

		for test, expected in cases.items():
			result = r.sub(replace, test)

			if result != expected:
				print("[-] Failed matching '%s' against '%s'" % (test, pattern))
				print("[-]   Expected: '%s'" % (expected,))
				print("[-]        Got: '%s'" % (result,))

def _test_sub_otf():
	for suite in SUITES:
		pattern = suite["pattern"]
		replace = suite["replace"]
		cases = suite["cases"]

		for test, expected in cases.items():
			result = redone.sub(pattern, replace, test)

			if result != expected:
				print("[-] Failed matching '%s' against '%s'" % (test, pattern))
				print("[-]   Expected: '%s'" % (expected,))
				print("[-]        Got: '%s'" % (result,))

def test():
	print("[*] test: sub [compiled]")
	_test_sub_compile()

	print("[*] test: sub [on-the-fly]")
	_test_sub_otf()
