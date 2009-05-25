#!/usr/bin/python

import sys
from optparse import OptionParser
from StringIO import StringIO

from util.bugs import extract_bugs
from util.debtags import filter_pkgs
from util.popcon import popcon

orphaned_file = "/home/sez/fun/debian/participation/cache/bugs/orphaned.html"
popcon_file = '/home/sez/fun/debian/participation/cache/popcon-data/all-popcon-results.txt'

def main():
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

    bug_list, bugs_by_pkg = extract_bugs(open(orphaned_file, "r"))
    pc = popcon(popcon_file)
    tag_db = StringIO("\n".join([str(b.pkg) for b in bug_list]))
    pkgs_iter = filter_pkgs(tag_db, match_tags, excl_tags)
    pkgs = [p for p in pkgs_iter.iter_packages()]
    pkgs.sort(cmp=lambda x, y: pc.pkg_inst(x) - pc.pkg_inst(y), reverse=True)
    for p in pkgs:
        for b in bugs_by_pkg[p]:
            print "%s #%s (inst: %d)" % (p, b.bug_no, pc.pkg_inst(p))

if __name__ == '__main__':
    main()
