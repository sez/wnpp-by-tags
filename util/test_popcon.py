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
