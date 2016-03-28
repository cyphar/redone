#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Aleksa Sarai

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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
