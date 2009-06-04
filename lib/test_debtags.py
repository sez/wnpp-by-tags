# wnpp-by-tags - query WNPP bugs using the debtags of their packages
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

import debtags as DT

class DebtagsTest(unittest.TestCase):
    def parseTags(raw_tags):
        tags_by_pkg = {}
        for line in raw_tags.split("\n"):
            fields = line.split()
            pkgname = fields[0].rstrip(":")
            pkgtags = [t.rstrip(",") for t in fields[1:]]
            tags_by_pkg[pkgname] = set(pkgtags)
        dt = DT.Debtags(StringIO(raw_tags))
        return tags_by_pkg, dt
    parseTags = staticmethod(parseTags)
    def testTagParsing(self):
        """Test that the tags of every package are loaded correctly."""
        raw_tags = \
"""2vcard: implemented-in::perl, role::program, use::converting
3dchess: game::board, game::board:chess, implemented-in::c, interface::x11, role::program, uitoolkit::xlib, use::gameplaying, x11::application
4g8: admin::monitoring, protocol::ip, protocol::tcp, protocol::udp, role::program, works-with::network-traffic"""
        tags_by_pkg, dt = DebtagsTest.parseTags(raw_tags)
        for pkg, tags in tags_by_pkg.iteritems():
            self.assertEqual(dt.tags_of_pkg(pkg), tags)
    def testFiltering(self):
        raw_tags = \
"""vcard: implemented-in::perl, role::program, use::converting
jcard: implemented-in::java, role::program, use::converting"""
        match_tags = set(["role::program"])
        excl_tags = set(["implemented-in::java"])
        matching_pkgs = DT.filter_pkgs(StringIO(raw_tags), match_tags, excl_tags)
        matched_pkgs = [p for p in matching_pkgs.iter_packages()]
        self.assertEqual(matched_pkgs, ["vcard"])
    def testMatchingUntaggedPkgs(self):
        raw_tags = \
"""vcard: implemented-in::perl, role::program, use::converting
jcard: """
        match_tags = set(["role::program"])
        excl_tags = set([])
        matching_pkgs = DT.filter_pkgs(StringIO(raw_tags), match_tags, excl_tags)
        matched_pkgs = [p for p in matching_pkgs.iter_packages()]
        self.assertEqual(matched_pkgs, ["vcard"])

if __name__ == "__main__":
    unittest.main()
