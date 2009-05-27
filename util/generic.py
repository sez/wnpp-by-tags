import httplib
import os
import re
import sys

def warn(msg):
    sys.stderr.write("%s\n" % msg)

def giveup(msg):
    sys.stderr.write("%s\n" % msg)
    sys.exit(1)

def create_file(filename, contents):
    f = open(filename, "w")
    f.write(contents)
    f.close()

space_pat = re.compile("  *")
def remove_space_dups(s):
    return space_pat.sub(" ", s)

def ensure_dir_exists(dirname):
    if not os.path.isdir(dirname):
        try:
            os.makedirs(dirname)
        except OSError, e:
            giveup("failed to create %s ('%s')" % (dirname, e))

class HttpClient:
    """Wrapper around httplib to get pages from a single web server."""
    def __init__(self, http_server, verbose):
        self.conn = httplib.HTTPConnection(http_server)
        self.server_name = http_server
        self.verbose = verbose
    def get(self, url_suffix, url_prefix="/devel/wnpp"):
        """use a std module"""
        url = "%s/%s" % (url_prefix, url_suffix)
        self.conn.request("GET", url)
        response = self.conn.getresponse()
        if self.verbose:
            print "downloading %s" % url
        if response.status == 200:
            return response.read()
        raise Exception("%d %s" % (response.status, response.reason))
    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass
