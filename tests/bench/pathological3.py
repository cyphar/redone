#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Benchmark the pathological regular expression as defined here:
# http://swtch.com/~rsc/regexp/regexp1.html

import time

import re
import redone

_PATTERN = lambda size: "(a+a+)+b"
_STRING = lambda size: "a" * size

def _bench_re(size):
	PATTERN = _PATTERN(size)
	STRING = _STRING(size)

	compile_start = time.time()
	matcher = re.compile(PATTERN)
	compile_end = time.time()

	compile_delta = compile_end - compile_start
	print("[+] re:     n=%d -- compile:    %.16f seconds" % (size, compile_delta))

	match_start = time.time()
	assert matcher.fullmatch(STRING) is None
	match_end = time.time()

	match_delta = match_end - match_start
	print("[+] re:     n=%d -- match:      %.16f seconds" % (size, match_delta))

	return compile_delta + match_delta

def _bench_redone_compile(size):
	PATTERN = _PATTERN(size)
	STRING = _STRING(size)

	compile_start = time.time()
	matcher = redone.compile(PATTERN)
	compile_end = time.time()

	compile_delta = compile_end - compile_start
	print("[+] redone: n=%d -- compile:    %.16f seconds" % (size, compile_delta))

	match_start = time.time()
	assert matcher.fullmatch(STRING) is None
	match_end = time.time()

	match_delta = match_end - match_start
	print("[+] redone: n=%d -- comp match: %.16f seconds" % (size, match_delta))

	return compile_delta + match_delta

def _bench_redone_otf(size):
	PATTERN = _PATTERN(size)
	STRING = _STRING(size)

	match_start = time.time()
	assert redone.fullmatch(PATTERN, STRING) is None
	match_end = time.time()

	match_delta = match_end - match_start
	print("[+] redone: n=%d -- otf match:  %.16f seconds" % (size, match_delta))

	return match_delta

def bench(bench=25):
	print("[*] benchmark: pathological (easy)")

	delta = _bench_re(bench)
	print("[+] re:     n=%d -- total:      %.16f seconds" % (bench, delta))

	delta = _bench_redone_compile(bench)
	print("[+] redone: n=%d -- comp total: %.16f seconds" % (bench, delta))

	delta = _bench_redone_otf(bench)
	print("[+] redone: n=%d -- otf total:  %.16f seconds" % (bench, delta))

if __name__ == "__main__":
	bench()
