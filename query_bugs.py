#!/usr/bin/python

import httplib
import os
import sys
import time
from optparse import OptionParser
from StringIO import StringIO
from glob import glob

import conf
from util.bugs import extract_bugs, Package
from util.debtags import filter_pkgs, Debtags
from util.popcon import Popcon

popcon_file = '%s/popcon/all-popcon-results.txt' % conf.cache_dir

verbose = True

bug_type_map = { "help_requested" : "RFH",
                 "orphaned" : "O",
                 "rfa_bypackage" : "RFA",
                 "being_adopted" : "being adopted" }

def vprint(msg):
    if verbose:
        print msg

def warn(msg):
    sys.stderr.write("%s\n" % msg)

def giveup(msg):
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)

def create_file(filename, contents):
    f = open(filename, "w")
    f.write(contents)
    f.close()

def parse_args():
    usage = "usage: %prog --match-tags t1,t2,... [--exclude-tags t3,t4,...]"
    parser = OptionParser(usage)
    parser.add_option("-m", "--match-tags", dest="match_tags",
                      help="match packages having all these tags")
    parser.add_option("-x", "--exclude-tags", dest="excl_tags",
                      help="filter out packages having any of these tags")
    parser.add_option("-f", "--force-refresh", dest="force_update",
                      default=False,
                      help="refresh bug/popcon data regardless of age")
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

class HttpClient:
    def __init__(self, http_server="www.debian.org"):
        self.conn = httplib.HTTPConnection(http_server)
        self.server_name = http_server
    def get(self, url_suffix, url_prefix="/devel/wnpp"):
        """use a std module"""
        url = "%s/%s" % (url_prefix, url_suffix)
        self.conn.request("GET", url)
        response = self.conn.getresponse()
        vprint("downloading %s" % url)
        if response.status == 200:
            return response.read()
        raise Exception("%d %s" % (response.status, response.reason))
    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass

def refresh_bug_data():
    """Downloads bug and popcon data, if what's available is too old."""
    if not os.path.isdir(conf.cache_dir):
        try:
            os.makedirs(conf.cache_dir)
        except OSError:
            giveup("cache directory '%s' doesn't exist and I can't created it")

    # see which bug files have to be updated, if any
    now = time.time()
    def file_is_ok(filename, min_age):
        """True if file exists and isn't too old."""
        return os.path.isfile(filename) and \
               now - os.stat(filename).st_mtime < min_age
    files = ["%s/bugs/%s.html" % (conf.cache_dir, bt) for bt in conf.bug_types_to_query]
    bugs_mtime_threshold = int(conf.bugs_refresh_period_in_days) * 86400
    files_to_update = [f for f in files if not file_is_ok(f, bugs_mtime_threshold)]

    if not files_to_update:
        vprint("using previously downloaded bug data")
        return

    # download whatever files are missing or are old
    http_client = HttpClient()
    for filename in files_to_update:
        url_suffix = os.path.basename(filename)
        try:
            bug_page = http_client.get(url_suffix)
            create_file(filename, bug_page)
        except Exception, e:
            warn("failed to download ``%s'' bugs (%s)" % (filename, e))
    http_client.close()

def refresh_popcon_data():
    pass

def main():
    # misc initialisations
    refresh_bug_data()
    match_tags, excl_tags = parse_args()
    debtags = Debtags()
    popcon = Popcon(popcon_file)
    Package.init_sources(debtags.tags_of_pkg, popcon.inst_of_pkg)

    # build dict of package objects, indexed by package names
    pkgs_by_name = {}
    for bug_page in glob("%s/bugs/*.html" % conf.cache_dir):
        bug_type = bug_type_map[os.path.basename(bug_page).rstrip(".html")]
        pkgs_by_name = extract_bugs(open(bug_page, "r"), pkgs_by_name, bug_type)
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
            print "%s: %s #%s (inst: %d)" % (b.type, pkg_obj.name, b.bug_no, pkg_obj.popcon)

if __name__ == '__main__':
    main()
