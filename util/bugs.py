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
import os

from BeautifulSoup import BeautifulSoup

import conf
from generic import HttpClient, create_file, younger_than, warn, wget


class BugType(object):
    to_abbn = { "help_requested" : "RFH",
                "orphaned" : "O",
                "rfa_bypackage" : "RFA",
                "being_adopted" : "being_adopted" }
    to_name = { "RFH" : "help_requested",
                "O" : "orphaned" ,
                "RFA" : "rfa_bypackage",
                "being adopted" : "being_adopted" }
    def full_name_of(t):
        try:
            return BugType.to_name[t]
        except KeyError:
            return t
    def abbreviation_of(t):
        try:
            return BugType.to_abbn[t]
        except KeyError:
            return t
    full_name_of = staticmethod(full_name_of)
    abbreviation_of = staticmethod(abbreviation_of)


class Bug(object):
    def __init__(self, bug_no, title=None, type=None):
        # add bug title
        self.bug_no = bug_no
        self.title = title
        self.type = type
    def get_bug_title(self):
        if self.title is None:
            pass # TODO: get it from bts

def update_bug_data(update_anyway, cache_dir, bug_types, verbose=False):
    """Download bug if what's available is too old.

    ``update_anyway'' will download data regardless of how old they are

    ``cache_dir'' where to store the downloaded files

    ``bug_types'' what bug types to download data for (full names)

    """
    assert os.path.isdir(cache_dir)
    # see which bug files are missing or have to be updated, if any
    all_files = ["%s/%s.html" % (cache_dir, bt) for bt in bug_types]
    if update_anyway:
        files_to_update = all_files
    else:
        bugs_mtime_threshold = int(conf.bugs_update_period_in_days) * 86400
        files_to_update = [f for f in all_files \
                if not younger_than(f, bugs_mtime_threshold)]

        if not files_to_update:
            if verbose:
                print "using previously downloaded bug data"
            return

    url_paths = ["/devel/wnpp/%s" % os.path.basename(f) for f in files_to_update]
    wget("www.debian.org", url_paths, cache_dir, verbose)

class Package(object):
    tags_of_pkg = lambda x: None
    popcon_of_pkg = lambda x: None
    def init_sources(debtags_func, popcon_func):
        Package.tags_of_pkg = debtags_func
        Package.popcon_of_pkg = popcon_func
    init_sources = staticmethod(init_sources)
    def __init__(self, pkgname):
        self.name = pkgname
        self.bugs = set()
        self.tags = Package.tags_of_pkg(pkgname)
        self.popcon = Package.popcon_of_pkg(pkgname)
    def add_bug(self, bugno):
        self.bugs.add(bugno)
    def add_tags(self, tag_set):
        self.tags.update(tag_set)
    def bug_list(self):
        return list(self.bugs)
    def __repr__(self):
        return "%s: %s" % (self.name, ", ".join(self.tags))
    def __cmp__(self, other):
        """Used to allow sorting of packages based on popularity."""
        return self.popcon - other.popcon

#   <div id="inner">
#    <h1>
#     Orphaned packages
#    </h1>
#    <ul>
#     <li>
#      <a href="http://bugs.debian.org/525488">
#       9menu: Creates X menus from the shell
#      </a>
#      (
#       <a href="http://packages.debian.org/src:9menu">
#                           package info
#       </a>
#      )
#     </li>

#TODO: define a map of bug_type to cleanup function (eg, being_adopted -->
#parse page for pages since adoption, and filter out if less than a threshold)

def extract_bugs(html_page_handle, pkgs_by_name, bug_type):
    """Get list of bugs and corresponding pkg names."""
    soup = BeautifulSoup(html_page_handle.read())
    container_div = soup.find('div', id='inner')
    links = container_div.findChildren('a',
            href=re.compile('http:\/\/bugs.debian.org\/[0-9]+'))
    assert links
    for link in links:
        bug_url = link['href']
        pkgname = link.string.split(":")[0]
        bug_no = bug_url.split("/")[-1]

        pkg_obj = pkgs_by_name.get(pkgname)
        if pkg_obj is None:
            pkg_obj = Package(pkgname)
            pkgs_by_name[pkgname] = pkg_obj
        pkg_obj.add_bug(Bug(bug_no, pkgname, bug_type))

    return pkgs_by_name
