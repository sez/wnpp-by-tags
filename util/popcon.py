import os

from generic import remove_space_dups, warn

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

def update_popcon_data(cache_dir):
    pass

if __name__ == '__main__':
    pc = Popcon()
    print pc.inst_of_pkg('indywiki')
