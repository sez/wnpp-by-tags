import re
import os.path

from debian_bundle import debtags

class Debtags:
    def __init__(self, tagdb='/var/lib/debtags/package-tags'):
        assert os.path.exists(tagdb)
        self.db = debtags.DB()
        self.db.read(open(tagdb, 'r'))
    def tags_of_pkg(self, pkgname):
        # TODO: virtual and dummy pkgs
        return self.db.tags_of_package(pkgname)

def gen_filter(match_tags, excl_tags):
    return lambda pkg_tags: match_tags.issubset(pkg_tags) and \
                        all(t not in excl_tags for t in pkg_tags)

def filter_pkgs(tag_db_fd, match_tags, excl_tags):
    db = debtags.DB()
    db.read(tag_db_fd)
    select = gen_filter(match_tags, excl_tags)
    return db.filter_packages_tags(lambda x: select(x[1]))
