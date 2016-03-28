#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Aleksa Sarai

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import redone

TESTS = [
	{
		"pattern": r"[Aa]?[^Ab]+g+",
		"cases": {
			"match": {
				# Full matches
				"aaxxxxxxxgxxxxxxg": "aaxxxxxxxgxxxxxxg",
				"gggggxg": "gggggxg",

				# Partial matches.
				"aaxxxxxxxgAxxxxxg": "aaxxxxxxxg",
				"xxxxxgxgxgxgxxxa": "xxxxxgxgxgxg",
				"xgxxxxx": "xg",

				# Searches.
				"aAxxxxxxxgxxxxxxg": None,
				"xxxxxaAaxxxg": None,
				"bxxxxgAaaag": None,

				# Non-matches.
				"x": None,
				"g": None,
				"": None,
			},

			"fullmatch": {
				# Full matches
				"aaxxxxxxxgxxxxxxg": "aaxxxxxxxgxxxxxxg",
				"gggggxg": "gggggxg",

				# Partial matches.
				"aaxxxxxxxgAxxxxxg": None,
				"xxxxxgxgxgxgxxxa": None,
				"xgxxxxx": None,

				# Searches.
				"aAxxxxxxxgxxxxxxg": None,
				"xxxxxaAaxxxg": None,
				"bxxxxgAaaag": None,

				# Non-matches.
				"x": None,
				"g": None,
				"": None,
			},

			"search": {
				# Full matches
				"aaxxxxxxxgxxxxxxg": "aaxxxxxxxgxxxxxxg",
				"gggggxg": "gggggxg",

				# Partial matches.
				"aaxxxxxxxgAxxxxxg": "aaxxxxxxxg",
				"xxxxxgxgxgxgxxxa": "xxxxxgxgxgxg",
				"xgxxxxx": "xg",

				# Searches.
				"aAxxxxxxxgxxxxxxg": "Axxxxxxxgxxxxxxg",
				"xxxxxaAaxxxg": "Aaxxxg",
				"bxxxxgAaaag": "xxxxg",

				# Non-matches.
				"x": None,
				"g": None,
				"": None,
			},
		},
	},
]

def _test_greedy_compile():
	for cases in TESTS:
		pattern = cases["pattern"]
		r = redone.compile(pattern)

		for test, expected in cases["cases"]["match"].items():
			result = r.match(test)

			if result:
				result = result.group()

			if result != expected:
				print("[-] Failed matching '%s' against '%s'" % (test, pattern))
				print("[-]   Expected: '%s'" % (expected,))
				print("[-]        Got: '%s'" % (result,))

		for test, expected in cases["cases"]["fullmatch"].items():
			result = r.fullmatch(test)

			if result:
				result = result.group()

			if result != expected:
				print("[-] Failed fullmatching '%s' against '%s'" % (test, pattern))
				print("[-]   Expected: '%s'" % (expected,))
				print("[-]        Got: '%s'" % (result,))

		for test, expected in cases["cases"]["search"].items():
			result = r.search(test)

			if result:
				result = result.group()

			if result != expected:
				print("[-] Failed searching '%s' against '%s'" % (test, pattern))
				print("[-]   Expected: '%s'" % (expected,))
				print("[-]        Got: '%s'" % (result,))

def _test_greedy_otf():
	for cases in TESTS:
		pattern = cases["pattern"]

		for test, expected in cases["cases"]["match"].items():
			result = redone.match(pattern, test)

			if result:
				result = result.group()

			if result != expected:
				print("[-] Failed matching '%s' against '%s'" % (test, pattern))
				print("[-]   Expected: '%s'" % (expected,))
				print("[-]        Got: '%s'" % (result,))

		for test, expected in cases["cases"]["fullmatch"].items():
			result = redone.fullmatch(pattern, test)

			if result:
				result = result.group()

			if result != expected:
				print("[-] Failed fullmatching '%s' against '%s'" % (test, pattern))
				print("[-]   Expected: '%s'" % (expected,))
				print("[-]        Got: '%s'" % (result,))

		for test, expected in cases["cases"]["search"].items():
			result = redone.search(pattern, test)

			if result:
				result = result.group()

			if result != expected:
				print("[-] Failed searching '%s' against '%s'" % (test, pattern))
				print("[-]   Expected: '%s'" % (expected,))
				print("[-]        Got: '%s'" % (result,))

def test():
	print("[*] test: greedy [compiled]")
	_test_greedy_compile()

	print("[*] test: greedy [on-the-fly]")
	_test_greedy_otf()
