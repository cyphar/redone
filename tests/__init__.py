#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Cyphar

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .bench import pathological1
from .bench import pathological2
from .bench import pathological3

def run_bench():
	pathological1.bench(bench=16)
	pathological2.bench(bench=25)
	pathological3.bench(bench=25)

from .test import simple
from .test import sets
from .test import greedy
from .test import all as _all
from .test import sub
from .test import iter as _iter

def run_test():
	simple.test()
	sets.test()
	greedy.test()
	_all.test()
	sub.test()
	_iter.test()
