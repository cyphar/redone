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
