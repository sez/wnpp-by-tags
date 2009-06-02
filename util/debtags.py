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

import re
import os.path

from debian_bundle import debtags

class Debtags(object):
    tagdb_filename='/var/lib/debtags/package-tags'
    def __init__(self, tagdb=None):
        if not tagdb:
            tagdb = Debtags.tagdb_filename
        assert os.path.exists(tagdb)
        tagdb = open(tagdb)
        self.db = debtags.DB()
        self.db.read(tagdb)
        tagdb.close()
    def tags_of_pkg(self, pkgname):
        # TODO: virtual and dummy pkgs
        return self.db.tags_of_package(pkgname)

def gen_filter(match_tags, excl_tags):
    return lambda pkg_tags: match_tags.issubset(pkg_tags) and \
                        all(t not in excl_tags for t in pkg_tags)

def filter_pkgs(tag_db_fd, match_tags, excl_tags):
    """Return an iterator with pkgs with and without certain tags.

    ``tag_db_fd'' a multi-line string with the syntax of
                   /var/lib/debtags/package-tags

    ``match_tags'' select only packages matching all these tags (set)

    ``excl_tags'' filter out packages having any of these tags (set)
    """
    db = debtags.DB()
    db.read(tag_db_fd)
    select = gen_filter(match_tags, excl_tags)
    return db.filter_packages_tags(lambda x: select(x[1]))

class TagVocabulary(object):
    def __init__(self, tagfile, verbose=False):
        self.tagfile = tagfile
        self.tags = set([line.lstrip("Tag: ").rstrip("\n") \
                         for line in open(tagfile) \
                         if line.startswith("Tag: ")])
        assert self.tags
        if verbose:
            print "using vocabulary of %s tags" % len(self.tags)
    def invalid_tags(self, tags):
        return set(tags) - self.tags
