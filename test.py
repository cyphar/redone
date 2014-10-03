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

# Run benchmarks and tests.

import tests
import argparse

parser = argparse.ArgumentParser(description="Run the 'redone' test suite and benchmarks.")
o_tests = parser.add_mutually_exclusive_group()
o_tests.add_argument("-t", "--tests", dest='tests', action='store_true', help="enable tests")
o_tests.add_argument("-nt", "--no-tests", dest='tests', action='store_false', help="disable tests")
o_bench = parser.add_mutually_exclusive_group()
o_bench.add_argument("-b", "--benchmarks", dest='bench', action='store_true', help="enable benchmarks")
o_bench.add_argument("-nb", "--no-benchmarks", dest='bench', action='store_false', help="disable benchmarks")
parser.set_defaults(tests=False, benchmarks=False)

def main(do_tests=False, do_bench=False):
	# Neither tests nor benchmarks are being run.
	if not do_tests and not do_bench:
		print("test: neither tests nor benchmarks are enabled")
		parser.print_help()
		return

	if do_tests:
		print("[!] Running test suite!")
		tests.run_test()

	if do_bench:
		print("[!] Running benchmarks! (may take some time)")
		tests.run_bench()

if __name__ == "__main__":
	args = parser.parse_args()
	main(do_tests=args.tests, do_bench=args.bench)
