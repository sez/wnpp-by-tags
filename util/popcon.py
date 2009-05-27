import os

from generic import remove_space_dups

class Popcon:
    def __init__(self, cache_dir):
        popcon_file = "%s/popcon/all-popcon-results.txt" % cache_dir
        assert os.path.isdir(cache_dir)
        assert os.path.exists(popcon_file)
        self.inst_by_pkg = {}
        for line in open(popcon_file):
            if line.startswith("Package:"):
                line = remove_space_dups(line)
                _, pkg, inst, = line.split(" ")[:3]
                try:
                    inst = int(inst)
                except ValueError:
                    inst = -1
                self.inst_by_pkg[pkg] = inst
    def inst_of_pkg(self, pkg):
        try:
            return self.inst_by_pkg[pkg]
        except KeyError:
            return None

def update_popcon_data(cache_dir):
    pass

if __name__ == '__main__':
    pc = Popcon()
    print pc.inst_of_pkg('indywiki')
