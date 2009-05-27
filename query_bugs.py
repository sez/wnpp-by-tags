#!/usr/bin/python

import os
import sys
from optparse import OptionParser
from StringIO import StringIO
from glob import glob

import conf
from util.generic import warn, giveup, ensure_dir_exists
from util.bugs import extract_bugs, update_bug_data, Package, BugType
from util.debtags import filter_pkgs, Debtags
from util.popcon import Popcon, update_popcon_data

class Arguments:
    def __init__(self):
        usage = "usage: %prog --match-tags t1,t2,... [--exclude-tags t3,t4,...]"
        parser = OptionParser(usage)
        parser.add_option("-m", "--match-tags", dest="match_tags",
                          help="match packages having all these tags")
        parser.add_option("-x", "--exclude-tags", dest="excl_tags",
                          help="filter out packages having any of these tags")
        parser.add_option("-t", "--bug-types", dest="bug_types", default="any",
                          help="""query only against bugs of the types in this
                          comma-separated list (valid types: any, O, RFA, RFH,
                          ITP, being_adopted; default: any)""")
        parser.add_option("-f", "--force-update", action="store_true",
                          dest="force_update", default=False,
                          help="update bug/popcon data regardless of age")
        parser.add_option("-v", "--verbose", action="store_true",
                          dest="verbose", default=False)
        (options, args) = parser.parse_args()
        if len(args) > 0:
            parser.error("Unknown argument %s")
        if not options.match_tags:
            parser.error("You must specify at least -m")
            exit(1)

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

def main():
    # misc initialisations
    args = Arguments()
    ensure_dir_exists(conf.cache_dir)
    update_bug_data(args.force_update, "%s/bugs/" % conf.cache_dir,
                    args.full_name_bug_types, args.verbose)
    update_popcon_data(conf.cache_dir)
    debtags = Debtags()
    popcon = Popcon(conf.cache_dir)
    Package.init_sources(debtags.tags_of_pkg, popcon.inst_of_pkg)

    # build dict of package objects, indexed by package name, using the HTML
    # BTS pages
    pkgs_by_name = {}
    for bug_page in glob("%s/bugs/*.html" % conf.cache_dir):
        bug_type = BugType.abbreviation_of(os.path.basename(bug_page).rstrip(".html"))
        if bug_type in args.bug_types:
            pkgs_by_name = extract_bugs(open(bug_page, "r"), pkgs_by_name, bug_type)
    nbugs = sum([len(p.bugs) for p in pkgs_by_name.itervalues()])
    if args.verbose:
        print "%d bugs in %s packages" % (nbugs, len(pkgs_by_name))

    # filter packages using user-supplied tags
    tag_db = StringIO("\n".join([str(pkg) for pkg in pkgs_by_name.itervalues()]))
    matching_pkg_names = filter_pkgs(tag_db, args.match_tags, args.excl_tags)
    pkg_objs = [pkgs_by_name[p] for p in matching_pkg_names.iter_packages()]
    if args.verbose:
        print "query matches %d packages" % len(pkg_objs)

    # print list of matching packages, along with bug number and popcon
    for pkg_obj in sorted(pkg_objs, reverse=True):
        for b in pkg_obj.bug_list():
            print "%s: %s #%s (inst: %d)" % (b.type, pkg_obj.name, b.bug_no,
                                             pkg_obj.popcon)

if __name__ == '__main__':
    main()
