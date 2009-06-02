#!/usr/bin/python

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

import os
import sys
from optparse import OptionParser
from StringIO import StringIO
from glob import glob

import conf
from util.generic import warn, giveup, ensure_dir_exists
from util.bugs import extract_bugs, update_bug_data, Package, BugType
from util.debtags import filter_pkgs, Debtags, TagVocabulary
from util.popcon import Popcon, update_popcon_data, POPCON_FNAME

class Arguments:
    """Class to parse, check and encapsulate command-line argument values."""
    def __init__(self):
        usage = \
"""usage: %prog --match-tags t1,t2,... [--exclude-tags t3,t4,...]
                     [-t RFA,O,...] [-f] [-v]
       %prog --untagged-pkgs-only [-f] [-v]"""
        parser = OptionParser(usage)
        parser.add_option("-m", "--match-tags", dest="match_tags",
                          help="""match packages having all these tags (not to
                          be used with -u)""")
        parser.add_option("-x", "--exclude-tags", dest="excl_tags",
                          help="filter out packages having any of these tags")
        parser.add_option("-t", "--bug-types", dest="bug_types", default="any",
                          help="""query only against bugs of the types in this
                          comma-separated list (valid types: any, O, RFA, RFH,
                          ITP, being_adopted; default: any)""")
        parser.add_option("-u", "--untagged-pkgs-only", action="store_true",
                          dest="show_untagged",
                          help="""list only bugs for packages that haven't
                          been tagged yet (not to be used with -m)""")
        parser.add_option("-f", "--force-update", action="store_true",
                          dest="force_update", default=False,
                          help="""update bug and popcon data regardless of age
                                  (by default,  bug data is updated when it's
                                  older than 7 days, and popcon data when it's
                                  older than 30 days)""")
        parser.add_option("--cache-dir", dest="cache_dir",
                          default=os.path.expanduser("~/.query-bugs"),
                          help="directory where to cache bug and popcon data")
        parser.add_option("--debtags-file", dest="debtags_file",
                          default="/var/lib/debtags/package-tags",
                          help="""use an alternative debtags file
                          (default: /var/lib/debtags/package-tags)""")
        parser.add_option("--vocabulary-file", dest="tags_file",
                          default="/var/lib/debtags/vocabulary",
                          help="""user-supplied tags for filtering are checked
                          against this tag file (default:
                          /var/lib/debtags/vocabulary)""")
        parser.add_option("-v", "--verbose", action="store_true",
                          dest="verbose", default=False)
        (options, args) = parser.parse_args()
        if len(args) > 0:
            parser.error("Unknown argument %s")
        if not options.match_tags and not options.show_untagged:
            parser.error("You must specify at least either -m or -u")
            exit(1)
        if options.match_tags and options.show_untagged:
            parser.error("You must either -m or -u")
            exit(1)

        if options.match_tags:
            # parse tags to match and tags to exclude
            self.match_tags = set(options.match_tags.split(","))
            if options.excl_tags:
                self.excl_tags = set(options.excl_tags.split(","))
            else:
                self.excl_tags = set()

        if options.bug_types == "any":
            # query against default bug types
            self.full_name_bug_types = conf.bug_types_to_query
            self.bug_types = [BugType.abbreviation_of(bt) \
                              for bt in self.full_name_bug_types]
        else:
            # convert any bug type acronyms to uppercase
            self.bug_types = [b.upper() if len(b) <= 3 else b \
                              for b in options.bug_types.split(",")]
            # check that the user-supplied bug types are valid
            self.full_name_bug_types = [BugType.full_name_of(bt) for bt in self.bug_types]
            invalid_bug_types = set(self.full_name_bug_types).difference(conf.known_bug_types)
            if invalid_bug_types:
                giveup("invalid  bug type(s): %s" % ", ".join(list(invalid_bug_types)))
            self.bug_types = [BugType.abbreviation_of(bt) for bt in self.bug_types]
        self.bug_types = set(self.bug_types)

        self.force_update = options.force_update
        self.verbose = options.verbose
        self.show_untagged = options.show_untagged
        self.debtags_file = os.path.abspath(options.debtags_file)
        self.cache_dir = os.path.abspath(options.cache_dir)
        self.tags_file = options.tags_file

def main():
    # parse user-supplied arguments
    args = Arguments()
    # sanity check
    vocabulary = TagVocabulary(args.tags_file)
    invalid_tags = vocabulary.invalid_tags(args.match_tags.union(args.excl_tags))
    if invalid_tags:
        giveup("The following tags are not listed in %s:\n%s" % \
                (args.tags_file, "\n".join(list(invalid_tags))))

    # misc initialisations
    bugs_dir = "%s/bugs" % args.cache_dir
    popcon_dir = "%s/popcon" % args.cache_dir
    ensure_dir_exists(bugs_dir)
    ensure_dir_exists(popcon_dir)
    update_bug_data(args.force_update, bugs_dir,
                    args.full_name_bug_types, args.verbose)
    update_popcon_data(args.force_update, popcon_dir, args.verbose)
    debtags = Debtags(args.debtags_file)
    popcon_file = "%s/%s" % (popcon_dir, POPCON_FNAME)
    assert os.path.isfile(popcon_file)
    popcon = Popcon(open(popcon_file, "r"))
    Package.init_sources(debtags.tags_of_pkg, popcon.inst_of_pkg)

    # build dict of package objects, indexed by package name, using the HTML
    # BTS pages
    pkgs_by_name = {}
    for bug_page in glob("%s/*.html" % bugs_dir):
        bug_type = BugType.abbreviation_of(os.path.basename(bug_page).rstrip(".html"))
        if bug_type in args.bug_types:
            pkgs_by_name = extract_bugs(open(bug_page, "r"), pkgs_by_name, bug_type)

    if args.show_untagged:
        # select only packages without tags
        pkg_objs = [p for p in pkgs_by_name.itervalues() if not p.tags]
    else:
        # filter packages using user-supplied tags
        tag_db = StringIO("\n".join([str(p) for p in pkgs_by_name.itervalues()]))
        matching_pkg_names = filter_pkgs(tag_db, args.match_tags, args.excl_tags)
        pkg_objs = [pkgs_by_name[p] for p in matching_pkg_names.iter_packages()]
        pkg_objs = [p for p in pkg_objs if p.tags]

    if args.verbose:
        nbugs = sum([len(p.bugs) for p in pkgs_by_name.itervalues()])
        print "loaded %d bugs in %s packages; query matches %d packages" \
                % (nbugs, len(pkgs_by_name), len(pkg_objs))

    # print list of matching packages, along with bug number and popcon
    for pkg_obj in sorted(pkg_objs, reverse=True):
        for bug in pkg_obj.bug_list():
            print "%s %s %s %d" % (bug.type, bug.bug_no, pkg_obj.name,
                                             pkg_obj.popcon)

if __name__ == '__main__':
    main()
