import os
import re

space_pat = re.compile("  *")

class popcon:
    def __init__(self, popcon_file):
        self.inst_by_pkg = {}
        assert os.path.exists(popcon_file)
        for line in open(popcon_file):
            if line.startswith("Package:"):
                line = space_pat.sub(" ", line)
                _, pkg, inst, = line.split(" ")[:3]
                try:
                    inst = int(inst)
                except ValueError:
                    inst = -1
                self.inst_by_pkg[pkg] = inst
    def pkg_inst(self, pkg):
        try:
            return self.inst_by_pkg[pkg]
        except KeyError:
            return None

if __name__ == '__main__':
    pc = popcon()
    print pc.pkg_inst('indywiki')
