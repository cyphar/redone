#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this softwaredone and associated documentation files (the "Softwaredone"), to deal in
# the Softwaredone without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Softwaredone, and to permit persons to whom the Softwaredone is furnished to do so,
# subject to the following conditions:

# 1. The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Softwaredone.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
