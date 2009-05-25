import re

from debian_bundle import debtags
from btsutils.debbugs import debbugs

from BeautifulSoup import BeautifulSoup

tagdb='/var/lib/debtags/package-tags'

bts_db = debbugs()
debtags_db = debtags.DB()
debtags_db.read(open(tagdb, 'r'))

tags_by_bugtype = {
        'RFP' : ['time-commitment::long-term', 'contribution-type::packaging'],
        'RFA' : ['time-commitment::long-term', 'contribution-type::packaging'],
        }

class Bug:
    def __init__(self, bug_no, bug_url, pkgname):
        # add bug title
        self.bug_no = bug_no
        self.bug_url = bug_url
        self.pkg= Package(pkgname, bug_no)
        self.custom_tags = set()
    def tags(self):
        # TODO: metapackages and dummy pkgs
        return debtags_db.tags_of_package(self.pkg.name)
    def add_tags(self, tag_set):
        self.custom_tags.update(tag_set)
    def __repr__(self):
        return "%s: %s" % (self.bug_no, self.pkg)

def annotate_orphan(bug):
    """add tags to a given orphan bug"""
    pass # bug.custom_tags.update()

def annotate_rfp(bug):
    pass

def annotate_rfh(bug):
    pass

class Package:
    def __init__(self, pkgname, bug_no):
        self.name = pkgname
        self.tags = debtags_db.tags_of_package(pkgname)
        self.bug_no = bug_no
    def __repr__(self):
        return "%s: %s" % (self.name, ", ".join(self.tags))

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
    bugs_by_package = {}
    soup = BeautifulSoup(html_page_handle.read())
    container_div = soup.find('div', id='inner')
    links = container_div.findChildren('a',
            href=re.compile('http:\/\/bugs.debian.org\/[0-9]+'))
    assert links
    bug_list = []
    for link in links:
        bug_url = link['href']
        pkgname = link.string.split(":")[0]
        bug_no = bug_url.split("/")[-1]
        bug = Bug(bug_no, bug_url, pkgname)
        bug_list.append(bug)
        pkg_bugs = bugs_by_package.get(pkgname)
        if pkg_bugs:
            bugs_by_package[pkgname].append(bug)
        else:
            bugs_by_package[pkgname] = [bug]

    return bug_list, bugs_by_package

