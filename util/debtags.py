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
