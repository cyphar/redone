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
