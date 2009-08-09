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

import os

from util import remove_space_dups, warn, wget, decompress_gzip, younger_than

POPCON_FNAME = "all-popcon-results.txt"

class Popcon(object):
    def __init__(self, popcon_file):
        self.inst_by_pkg = {}
        for line in popcon_file:
            if line.startswith("Package:"):
                line = remove_space_dups(line)
                try:
                    _, pkg, _, inst, = line.split(" ")[:4]
                    self.inst_by_pkg[pkg] = int(inst)
                except ValueError:
                    warn("failed to parse popcon inst value for '%s'" % pkg)
    def inst_of_pkg(self, pkg):
        try:
            return self.inst_by_pkg[pkg]
        except KeyError:
            return 0

def update_popcon_data(update_anyway, cache_dir, popcon_update_period_in_days,
        verbose=False):

    filename = "%s/%s" % (cache_dir, POPCON_FNAME)
    max_age = popcon_update_period_in_days * 86400
    if update_anyway or not younger_than(filename, max_age):
        url_paths = ["/%s.gz" % POPCON_FNAME]
        wget("popcon.debian.org", url_paths, cache_dir, verbose)
        decompress_gzip("%s.gz" % filename)
    elif verbose:
        print "using previously downloaded popcon data"

if __name__ == '__main__':
    pc = Popcon()
    print pc.inst_of_pkg('indywiki')
