import re

from btsutils.debbugs import debbugs

from BeautifulSoup import BeautifulSoup

#bts_db = debbugs()

tags_by_bugtype = {
        'RFP' : ['time-commitment::long-term', 'contribution-type::packaging'],
        'RFA' : ['time-commitment::long-term', 'contribution-type::packaging'],
        }

class Bug:
    def __init__(self, bug_no, title=None, type=None):
        # add bug title
        self.bug_no = bug_no
        self.title = title
        self.type = type
    def get_bug_title(self):
        if self.title is None:
            pass # TODO: get it from bts

class Package:
    tags_of_pkg = lambda x: None
    popcon_of_pkg = lambda x: None
    def init_sources(debtags_func, popcon_func):
        Package.tags_of_pkg = debtags_func
        Package.popcon_of_pkg = popcon_func
    init_sources = staticmethod(init_sources)
    def __init__(self, pkgname):
        self.name = pkgname
        self.bugs = set()
        self.tags = Package.tags_of_pkg(pkgname)
        self.popcon = Package.popcon_of_pkg(pkgname)
    def add_bug(self, bugno):
        self.bugs.add(bugno)
    def add_tags(self, tag_set):
        self.tags.update(tag_set)
    def bug_list(self):
        return list(self.bugs)
    def __repr__(self):
        return "%s: %s" % (self.name, ", ".join(self.tags))
    def __cmp__(self, other):
        return self.popcon - other.popcon

#   <div id="inner">
#    <h1>
#     Orphaned packages
#    </h1>
#    <ul>
#     <li>
#      <a href="http://bugs.debian.org/525488">
#       9menu: Creates X menus from the shell
#      </a>
#      (
#       <a href="http://packages.debian.org/src:9menu">
#                           package info
#       </a>
#      )
#     </li>

def extract_bugs(html_page_handle):
    # get list of bugs and corresponding pkg names
    pkgs_by_name = {}
    soup = BeautifulSoup(html_page_handle.read())
    container_div = soup.find('div', id='inner')
    links = container_div.findChildren('a',
            href=re.compile('http:\/\/bugs.debian.org\/[0-9]+'))
    assert links
    for link in links:
        bug_url = link['href']
        pkgname = link.string.split(":")[0]
        bug_no = bug_url.split("/")[-1]
        
        pkg_obj = pkgs_by_name.get(pkgname)
        if pkg_obj is None:
            pkg_obj = Package(pkgname)
            pkgs_by_name[pkgname] = pkg_obj
        pkg_obj.add_bug(Bug(bug_no, pkgname))

    return pkgs_by_name
