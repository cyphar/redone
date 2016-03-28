#!/usr/bin/env python3
# redone: A correct regex implementation in Python
# Copyright (C) 2014 Aleksa Sarai

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import string

ALPHABET = set(string.printable)
METACHARS = {"^", ".", "*", "+", "?", "(", ")", "[", "]", "{", "}", "|", "\\"}
SETMETA = {"[", "]", "\\"}
