#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Aleksa Sarai

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import redone

PATTERN = r"a?b+c*"
CASES = {
	"abccbabcbc": ["abcc", "b", "abc", "bc"],
	"aaaa": [],
	"bbbb": ["bbbb"],
}

def _test_all_compile():
	r = redone.compile(PATTERN)

	for test, expected in CASES.items():
		result = [m.group() for m in r.findall(test)]

		if result != expected:
			print("[-] Failed matching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

def _test_all_otf():
	for test, expected in CASES.items():
		result = [m.group() for m in redone.findall(PATTERN, test)]

		if result != expected:
			print("[-] Failed matching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

def test():
	print("[*] test: findall [compiled]")
	_test_all_compile()

	print("[*] test: findall [on-the-fly]")
	_test_all_otf()
