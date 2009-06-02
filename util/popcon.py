import os

import conf
from generic import remove_space_dups, warn, wget, decompress_gzip, younger_than

POPCON_FNAME = "all-popcon-results.txt"

class Popcon(object):
    def __init__(self, popcon_file):
        self.inst_by_pkg = {}
        for line in popcon_file:
            if line.startswith("Package:"):
                line = remove_space_dups(line)
                try:
                    _, pkg, inst, = line.split(" ")[:3]
                    self.inst_by_pkg[pkg] = int(inst)
                except ValueError:
                    warn("failed to parse popcon inst value for '%s'" % pkg)
    def inst_of_pkg(self, pkg):
        try:
            return self.inst_by_pkg[pkg]
        except KeyError:
            return 0

def update_popcon_data(update_anyway, cache_dir, verbose=False):
    filename = "%s/%s" % (cache_dir, POPCON_FNAME)
    max_age = int(conf.popcon_update_period_in_days) * 86400
    if update_anyway or not younger_than(filename, max_age):
        url_paths = ["/%s.gz" % POPCON_FNAME]
        wget("popcon.debian.org", url_paths, cache_dir, verbose)
        decompress_gzip("%s.gz" % filename)
    elif verbose:
        print "using previously downloaded popcon data"

if __name__ == '__main__':
    pc = Popcon()
    print pc.inst_of_pkg('indywiki')
