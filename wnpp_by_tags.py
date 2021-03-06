#!/usr/bin/python

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
import sys
from optparse import OptionParser
from StringIO import StringIO
from glob import glob

from lib.config import Config
from lib.util import warn, giveup, ensure_dir_exists, create_file
from lib.bugs import extract_bugs, update_bug_data, Package, BugType
from lib.debtags import filter_pkgs, Debtags, TagVocabulary
from lib.popcon import Popcon, update_popcon_data, POPCON_FNAME

__author__ = "Serafeim Zanikolas <serzan@hellug.gr>"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2009 Serafeim Zanikolas"
__license__ = "GPL-2+"


class Arguments:
    """Class to parse, check and encapsulate command-line argument values."""
    def __init__(self):
        self.conf = Config()
        usage = \
"""usage: %prog --match-tags t1,t2,... [--exclude-tags t3,t4,...]
                     [-t RFA,O,...] [-f] [-v]
       %prog --batch-queries-file --dest-dir <dirname>
       %prog --list-valid-tags
       %prog --untagged-pkgs-only"""
        parser = OptionParser(usage)
        parser.add_option("-b", "--batch-queries-file", dest="batch_qfile",
                          help="""in batch mode, read queries from this file
                          (one query per line)""", default=None)
        parser.add_option("-d", "--dest-dir", dest="batch_dir",
                          help="""in batch mode, create a result file for
                          every query in this directory""", default=None)
        parser.add_option("-m", "--match-tags", dest="match_tags",
                          help="""match packages having all these tags
                          (comma-separated list; not to be used with -l or -u)""")
        parser.add_option("-x", "--exclude-tags", dest="excl_tags",
                          help="""filter out packages having any of these tags
                          (comma-separated list)""")
        parser.add_option("-t", "--bug-types", dest="bug_types", default="any",
                          help="""query only against bugs of the types in this
                          comma-separated list (valid types: any, O, RFA, RFH,
                          ITP, being_adopted; default: any)""")
        parser.add_option("-l", "--list-valid-tags", action="store_true",
                          dest="list_tags", help="""use this if you don't know
                          what to query for (not to be used with -m or -u)""")
        parser.add_option("-u", "--untagged-pkgs-only", action="store_true",
                          dest="show_untagged",
                          help="""list only bugs for packages that haven't
                          been tagged yet (not to be used with -m or -l)""")
        parser.add_option("-f", "--force-update", action="store_true",
                          dest="force_update", default=False,
                          help="""update bug and popcon data regardless of age
                                  (by default,  bug data is updated when it's
                                  older than 7 days, and popcon data when it's
                                  older than 30 days)""")
        parser.add_option("--cache-dir", dest="cache_dir",
                          default=os.path.expanduser("~/.devscripts_cache"),
                          help="""cache directory for bug and popcon data
                          (default: ~/.devscripts_cache""")
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
        parser.add_option("-V", "--version", action="store_true",
                          dest="show_version", default=False,
                          help="show version information")
        (options, args) = parser.parse_args()
        if len(args) > 0:
            parser.error("Unknown argument %s")
        if options.show_version:
            print "wnpp-by-tags %s" % __version__
            exit(0)
        options.match_tags or options.show_untagged or options.list_tags or \
                options.batch_qfile or \
            parser.error("Please specify at least either -m, -b, -u or -l")
        options.match_tags and options.show_untagged and \
            parser.error("Please specify either -m or -u")
        if options.batch_qfile or options.batch_dir:
            options.batch_qfile and options.batch_dir or \
                parser.error("In batch mode, you have to specify both -b and -d")
            if options.batch_qfile == "-":
                queries_fd = sys.stdin
            else:
                assert os.path.exists(options.batch_qfile)
                queries_fd = open(options.batch_qfile)
            self.batch_queries = queries_fd.read().strip().split("\n")
            ensure_dir_exists(options.batch_dir)
            self.batch_dir = options.batch_dir
        else:
            self.batch_queries = None
            self.batch_dir = None

        self.match_tags = set()
        self.excl_tags = set()
        if options.match_tags:
            # parse tags to match and tags to exclude
            self.match_tags = set(options.match_tags.split(","))
            if options.excl_tags:
                self.excl_tags = set(options.excl_tags.split(","))

        if options.bug_types == "any":
            # query against default bug types
            self.full_name_bug_types = self.conf.bug_types_to_query
            self.bug_types = [BugType.abbreviation_of(bt) \
                              for bt in self.full_name_bug_types]
        else:
            # convert any bug type acronyms to uppercase
            self.bug_types = [b.upper() if len(b) <= 3 else b \
                              for b in options.bug_types.split(",")]
            # check that the user-supplied bug types are valid
            self.full_name_bug_types = [BugType.full_name_of(bt) for bt in self.bug_types]
            invalid_bug_types = set(self.full_name_bug_types).difference(self.conf.known_bug_types)
            if invalid_bug_types:
                giveup("invalid  bug type(s): %s" % ", ".join(list(invalid_bug_types)))
            self.bug_types = [BugType.abbreviation_of(bt) for bt in self.bug_types]
        self.bug_types = set(self.bug_types)

        self.force_update = options.force_update
        self.verbose = options.verbose
        self.list_tags = options.list_tags
        self.show_untagged = options.show_untagged
        self.debtags_file = os.path.abspath(options.debtags_file)
        self.cache_dir = os.path.abspath(options.cache_dir)
        self.tags_file = options.tags_file

def main():
    # parse user-supplied arguments
    args = Arguments()
    # sanity checks
    if not os.path.exists(args.debtags_file):
        giveup("The debtags file %s doesn't exist" % args.debtags_file)
    if not os.path.exists(args.tags_file):
        giveup("The tag vocabulary file %s doesn't exist" % args.tags_file)

    if args.match_tags or args.list_tags or args.batch_queries:
        vocabulary = TagVocabulary(args.tags_file)
        if args.list_tags:
            print vocabulary
            exit(0)
        invalid_tags = vocabulary.invalid_tags(args.match_tags.union(args.excl_tags))
        if invalid_tags:
            giveup("The following tags are not listed in %s:\n%s" % \
                    (args.tags_file, "\n".join(list(invalid_tags))))

    # misc initialisations
    bugs_dir = "%s/wnpp" % args.cache_dir
    popcon_dir = "%s/popcon" % args.cache_dir
    ensure_dir_exists(bugs_dir)
    ensure_dir_exists(popcon_dir)
    update_bug_data(args.force_update, bugs_dir, args.full_name_bug_types,
            args.conf.bugs_update_period_in_days, args.verbose)
    update_popcon_data(args.force_update, popcon_dir,
            args.conf.popcon_update_period_in_days, args.verbose)
    debtags = Debtags(open(args.debtags_file))
    popcon_file = "%s/%s" % (popcon_dir, POPCON_FNAME)
    assert os.path.isfile(popcon_file)
    popcon = Popcon(open(popcon_file, "r"))
    Package.init_sources(debtags.tags_of_pkg, popcon.inst_of_pkg)

    # build dict of package objects, indexed by package name, using the HTML
    # BTS pages
    pkgs_by_name = {}
    for bug_page in glob("%s/*.html" % bugs_dir):
        bug_type = BugType.abbreviation_of(os.path.basename(bug_page)[:-5])
        if bug_type in args.bug_types:
            pkgs_by_name = extract_bugs(open(bug_page, "r"), pkgs_by_name, bug_type)

    if args.show_untagged:
        # select only packages without tags
        pkg_objs = [p for p in pkgs_by_name.itervalues() if not p.tags]
        print format_matches(pkg_objs, args)
        exit(0)

    if args.verbose:
        nbugs = sum([len(p.bugs) for p in pkgs_by_name.itervalues()])
        print "loaded %d bugs in %s packages" % (nbugs, len(pkgs_by_name))

    # filter packages using user-supplied tags
    tag_db = StringIO("\n".join([str(p) for p in pkgs_by_name.itervalues()]))
    if not args.batch_queries:
        pkg_objs = gen_matches(tag_db, pkgs_by_name, args)
        print format_matches(pkg_objs, args)
        exit(0)

    # else we're in batch mode
    for facet in args.batch_queries:
        if args.verbose:
            print "processing \"%s\" tags" % facet
        facet_dir = "%s/%s" % (args.batch_dir, facet)
        ensure_dir_exists(facet_dir)
        for tag in vocabulary.tags_of_facet(facet):
            args.match_tags = set([tag])
            pkg_objs = gen_matches(tag_db, pkgs_by_name, args)
            try:
                tag_value = tag.split("::")[1]
            except ValueError:
                warn("skipping invalid tag \"%s\"" % tag)
                continue
            filename = "%s/%s" % (facet_dir, tag_value)
            matches = format_matches(pkg_objs, args)
            create_file(filename, matches)
            tag_db.seek(0)

def gen_matches(tag_db, pkgs_by_name, args):
    matching_pkg_names = filter_pkgs(tag_db, args.match_tags, args.excl_tags)
    pkg_objs = [pkgs_by_name[p] for p in matching_pkg_names.iter_packages()]
    return [p for p in pkg_objs if p.tags]

def format_matches(pkg_objs, args):
    """Return a string-formated list of matching packages, along with bug
       number and popcon."""
    result = []
    for pkg_obj in sorted(pkg_objs, reverse=True):
        for bug in pkg_obj.bug_list():
            if bug.type == 'BA' and \
               bug.dust < args.conf.being_adopted_threshold_in_days:
                   continue
            result.append("%s %s %s %d %s" % (bug.type, bug.bug_no,
                                                pkg_obj.name, pkg_obj.popcon,
                                                bug.dust))
    return "\n".join(result)

if __name__ == '__main__':
    main()
