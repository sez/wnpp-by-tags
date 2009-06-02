# TagBugger - query WNPP bugs using the debtags of their packages
# Copyright (C) 2009 Serafeim Zanikolas <serzan@hellug.gr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import unittest
from StringIO import StringIO

import popcon

class PopconTest(unittest.TestCase):
    def testEmpty(self):
        for contents in ["", "invalid line"]:
            f = StringIO(contents)
            pc = popcon.Popcon(f)
            self.assertEqual(len(pc.inst_by_pkg.keys()), 0)
    def testOneEntry(self):
        f = StringIO("""
Package: a2ps                            1570  5696   868     3
Package: abcm2ps                           27   114     8     0
Package: acheck                            17    59     1     0
Package: acheck-rules                      16    46     1     0
invalid line
Package: easydiff.app                      27   128    72     0
""")
        pc = popcon.Popcon(f)
        self.assertEqual(len(pc.inst_by_pkg.keys()), 5)
        self.assertEqual(pc.inst_of_pkg("a2ps"), 1570)
        self.assertEqual(pc.inst_of_pkg("abcm2ps"), 27)
        self.assertEqual(pc.inst_of_pkg("acheck"), 17)
        self.assertEqual(pc.inst_of_pkg("acheck-rules"), 16)
        self.assertEqual(pc.inst_of_pkg("easydiff.app"), 27)

if __name__ == "__main__":
    unittest.main()
