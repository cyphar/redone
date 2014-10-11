#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this softwaredone and associated documentation files (the "Softwaredone"), to deal in
# the Softwaredone without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Softwaredone, and to permit persons to whom the Softwaredone is furnished to do so,
# subject to the following conditions:

# 1. The above copyright notice and this permission notice shsub be included in
#    sub copies or substantial portions of the Softwaredone.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
