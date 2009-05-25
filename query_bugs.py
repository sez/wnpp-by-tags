#!/usr/bin/python

import sys
from optparse import OptionParser
from StringIO import StringIO

from util.bugs import extract_bugs, Package
from util.debtags import filter_pkgs, Debtags
from util.popcon import Popcon

orphaned_file = "/home/sez/fun/debian/participation/cache/bugs/orphaned.html"
popcon_file = '/home/sez/fun/debian/participation/cache/popcon-data/all-popcon-results.txt'

verbose = False

def vprint(msg):
    if verbose:
        print msg

def parse_args():
    usage = "usage: %prog --match-tags t1,t2,... [--exclude-tags t3,t4,...]"
    parser = OptionParser(usage)
    parser.add_option("-m", "--match-tags", dest="match_tags",
                      help="match packages having all these tags")
    parser.add_option("-x", "--exclude-tags", dest="excl_tags",
                      help="filter out packages having any of these tags")
    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.error("Unknown argument %s")
    if not options.match_tags:
        parser.error("You must specify at least -m")
        exit(1)

    match_tags = set(options.match_tags.split(","))
    if options.excl_tags:
        excl_tags = set(options.excl_tags.split(","))
    else:
        excl_tags = set()
    return match_tags, excl_tags

def main():
    # misc initialisations
    match_tags, excl_tags = parse_args()
    debtags = Debtags()
    popcon = Popcon(popcon_file)
    Package.init_sources(debtags.tags_of_pkg, popcon.inst_of_pkg)

    # build dict of package objects, indexed by package names
    pkgs_by_name = extract_bugs(open(orphaned_file, "r"))
    nbugs = sum([len(p.bugs) for p in pkgs_by_name.itervalues()])
    vprint("%d bugs in %s packages" % (nbugs, len(pkgs_by_name)))

    # filter packages using user-supplied tags
    tag_db = StringIO("\n".join([str(pkg) for pkg in pkgs_by_name.itervalues()]))
    matching_pkg_names = filter_pkgs(tag_db, match_tags, excl_tags)
    pkg_objs = [pkgs_by_name[p] for p in matching_pkg_names.iter_packages()]
    vprint("query matches %d packages" % len(pkg_objs))

    # print list of matching packages, along with bug number and popcon
    for pkg_obj in sorted(pkg_objs, reverse=True):
        for b in pkg_obj.bug_list():
            print "%s #%s (inst: %d)" % (pkg_obj.name, b.bug_no, pkg_obj.popcon)

if __name__ == '__main__':
    main()
