#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# 1. The above copyright notice and this permission notice shall be included in
#    all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Benchmark the pathological regular expression as defined here:
# http://swtch.com/~rsc/regexp/regexp1.html

import time

import re
import redone

def _bench_re(size):
	PATTERN = ("a?" * size) + ("a" * size)
	STRING = "a" * size

	compile_start = time.time()
	matcher = re.compile(PATTERN)
	compile_end = time.time()

	compile_delta = compile_end - compile_start
	print("[+] re:     n=%d -- compile:    %.16f seconds" % (size, compile_delta))

	match_start = time.time()
	assert matcher.fullmatch(STRING).group() == STRING
	match_end = time.time()

	match_delta = match_end - match_start
	print("[+] re:     n=%d -- match:      %.16f seconds" % (size, match_delta))

	return compile_delta + match_delta

def _bench_redone_compile(size):
	PATTERN = ("a?" * size) + ("a" * size)
	STRING = "a" * size

	compile_start = time.time()
	matcher = redone.compile(PATTERN)
	compile_end = time.time()

	compile_delta = compile_end - compile_start
	print("[+] redone: n=%d -- compile:    %.16f seconds" % (size, compile_delta))

	match_start = time.time()
	assert matcher.fullmatch(STRING) == STRING
	match_end = time.time()

	match_delta = match_end - match_start
	print("[+] redone: n=%d -- comp match: %.16f seconds" % (size, match_delta))

	return compile_delta + match_delta

def _bench_redone_otf(size):
	PATTERN = ("a?" * size) + ("a" * size)
	STRING = "a" * size

	match_start = time.time()
	assert redone.fullmatch(PATTERN, STRING) == STRING
	match_end = time.time()

	match_delta = match_end - match_start
	print("[+] redone: n=%d -- otf match:  %.16f seconds" % (size, match_delta))

	return match_delta

def bench(bench=29):
	print("[*] benchmark: pathological")

	delta = _bench_re(bench)
	print("[+] re:     n=%d -- total:      %.16f seconds" % (bench, delta))

	delta = _bench_redone_compile(bench)
	print("[+] redone: n=%d -- comp total: %.16f seconds" % (bench, delta))

	delta = _bench_redone_otf(bench)
	print("[+] redone: n=%d -- otf total:  %.16f seconds" % (bench, delta))

if __name__ == "__main__":
	bench_pathological()
