#-/usr/bin/env python3
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
		"": None,
	},
}


def _test_simple_compile():
	r = redone.compile(PATTERN)

	for test, expected in CASES["match"].items():
		result = r.match(test)

		if result != expected:
			print("[-] Failed matching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

	for test, expected in CASES["fullmatch"].items():
		result = r.fullmatch(test)

		if result != expected:
			print("[-] Failed fullmatching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

	for test, expected in CASES["search"].items():
		result = r.search(test)

		if result != expected:
			print("[-] Failed searching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

def _test_simple_otf():
	for test, expected in CASES["match"].items():
		result = redone.match(PATTERN, test)

		if result != expected:
			print("[-] Failed matching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

	for test, expected in CASES["fullmatch"].items():
		result = redone.fullmatch(PATTERN, test)

		if result != expected:
			print("[-] Failed fullmatching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

	for test, expected in CASES["search"].items():
		result = redone.search(PATTERN, test)

		if result != expected:
			print("[-] Failed searching '%s' against '%s'" % (test, PATTERN))
			print("[-]   Expected: '%s'" % (expected,))
			print("[-]        Got: '%s'" % (result,))

def test():
	print("[*] test: simple [compiled]")
	_test_simple_compile()

	print("[*] test: simple [on-the-fly]")
	_test_simple_otf()
