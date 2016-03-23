#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import redone

PATTERN = "a?(b|bc|[de]*)*f+"
CASES = {
	"match": {
		# Full matches.
		"abcdeeff": "abcdeeff",
		"f": "f",
		"df": "df",
		"bcfff": "bcfff",

		# Partial matches.
		"abcdeeffxx": "abcdeeff",
		"fxx": "f",

		# Searches.
		"aabbcddeef": None,
		"xxabbcdeeff": None,
		"axbcdeef": None,
		"acff": None,

		# Non-matches.
		"abbcde": None,
		"bcd": None,
		"a": None,
		"": None,
	},

	"fullmatch": {
		# Full matches.
		"abcdeeff": "abcdeeff",
		"f": "f",
		"df": "df",
		"bcfff": "bcfff",

		# Partial matches.
		"abcdeeffxx": None,
		"fxx": None,

		# Searches.
		"aabbcddeef": None,
		"xxabbcdeeff": None,
		"axbcdeef": None,
		"acff": None,

		# Non-matches.
		"abbcde": None,
		"bcd": None,
		"a": None,
		"": None,
	},

	"search": {
		# Full matches.
		"abcdeeff": "abcdeeff",
		"f": "f",
		"df": "df",
		"bcfff": "bcfff",

		# Partial matches.
		"abcdeeffxx": "abcdeeff",
		"fxx": "f",

		# Searches.
		"aabbcddeef": "abbcddeef",
		"xxabbcdeeff": "abbcdeeff",
		"axbcdeef": "bcdeef",
		"acff": "ff",

		# Non-matches.
		"abbcde": None,
		"bcd": None,
		"a": None,
		"": None,
	},
}


def _test_simple_compile():
	r = redone.compile(PATTERN)

	for test, expected in CASES["match"].items():
		result = r.match(test)

		if result:
			result = result.group()

		if result != expected:
			print("[-] Failed matching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

	for test, expected in CASES["fullmatch"].items():
		result = r.fullmatch(test)

		if result:
			result = result.group()

		if result != expected:
			print("[-] Failed fullmatching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

	for test, expected in CASES["search"].items():
		result = r.search(test)

		if result:
			result = result.group()

		if result != expected:
			print("[-] Failed searching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

def _test_simple_otf():
	for test, expected in CASES["match"].items():
		result = redone.match(PATTERN, test)

		if result:
			result = result.group()

		if result != expected:
			print("[-] Failed matching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

	for test, expected in CASES["fullmatch"].items():
		result = redone.fullmatch(PATTERN, test)

		if result:
			result = result.group()

		if result != expected:
			print("[-] Failed fullmatching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

	for test, expected in CASES["search"].items():
		result = redone.search(PATTERN, test)

		if result:
			result = result.group()

		if result != expected:
			print("[-] Failed searching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

def test():
	print("[*] test: simple [compiled]")
	_test_simple_compile()

	print("[*] test: simple [on-the-fly]")
	_test_simple_otf()
