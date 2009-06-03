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

from commands import getstatusoutput
from glob import glob
from tempfile import mkdtemp
import unittest
import os

from util.generic import create_file, warn
from test_query_data import orphaned_raw_data, rfa_raw_data, \
    popcon_raw_data

def setup_cache():
    cache_dir = mkdtemp("query-bugs")
    bugs_dir = "%s/bugs/" % cache_dir
    os.makedirs(bugs_dir)
    os.makedirs("%s/popcon" % cache_dir)
    create_file("%s/orphaned.html" % bugs_dir, orphaned_raw_data)
    create_file("%s/rfa_bypackage.html" % bugs_dir, rfa_raw_data)
    create_file("%s/popcon/all-popcon-results.txt" % cache_dir, popcon_raw_data)
    return cache_dir
cache_dir = setup_cache()

def run(cmd):
    status, output = getstatusoutput(cmd)
    if status != 0:
        warn("the command '%s' failed" % cmd)
    return status, output

class QueryTest(unittest.TestCase):
    prog = None
    prog = "./query_bugs.py --cache-dir %s" % cache_dir
    def testTagMatching1(self):
        expected_result = "RFA 447393 bins 29\nO 503554 a2ps-perl-ja 28"
        status, output = run("%s -t o,rfa -m implemented-in::perl" % QueryTest.prog)
        self.assertEqual(status, 0)
        self.assertEqual(output, expected_result)
    def testTagMatching2(self):
        """Same as previous test but for RFA only."""
        expected_result = "RFA 447393 bins 29"
        status, output = run("%s -t rfa -m implemented-in::perl" % QueryTest.prog)
        self.assertEqual(status, 0)
        self.assertEqual(output, expected_result)
    def testTagMatchingAndExclusion(self):
        expected_result = "RFA 447393 bins 29"
        status, output = run("%s -t o,rfa -m implemented-in::perl -x use::printing" % \
                QueryTest.prog)
        self.assertEqual(status, 0)
        self.assertEqual(output, expected_result)

if __name__ == "__main__":
    try:
        unittest.main()
    except Exception, e:
        print e
    finally:
        # wipe cache directory
        try:
            [os.remove(f) for f in glob("%s/*/*" % cache_dir)]
            os.rmdir("%s/popcon" % cache_dir)
            os.removedirs("%s/bugs" % cache_dir)
        except Exception, e:
            warn("error while trying to remove '%s':\n\t%s" % (cache_dir, e))
