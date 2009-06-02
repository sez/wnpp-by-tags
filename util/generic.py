import gzip
import httplib
import os
import re
import sys
import time

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

class HttpClient(object):
    """Wrapper around httplib to get pages from a web server."""
    def __init__(self, http_server, verbose):
        self.conn = httplib.HTTPConnection(http_server)
        self.server_name = http_server
        self.verbose = verbose
    def get(self, url):
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

def younger_than(filename, max_age):
    """True if the specified file exists and is younger than "age".

    ``filename'' file to test

    ``max_age'' in seconds
    """
    now = time.time()
    return os.path.exists(filename) and \
                   now - os.stat(filename).st_mtime < max_age


def wget(server, url_paths, dest_dir, verbose=False):
    """Download a list of urls from a given web server.

    ``server'' http server to connect to

    ``url_paths'' list of paths to download from server

    ``dest_dir'' directory where to place the downloaded pages"""
    http_client = HttpClient(server, verbose)
    for url_path in url_paths:
        filename = os.path.basename(url_path)
        try:
            downloaded_page = http_client.get(url_path)
            create_file("%s/%s" % (dest_dir, filename), downloaded_page)
        except Exception, e:
            warn("failed to download ``%s'' bugs (%s)" % (url_path, e))
    http_client.close()

def decompress_gzip(gz_filename, uncompressed_filename=None):
    assert os.path.isfile(gz_filename)
    if uncompressed_filename is None:
        assert gz_filename.endswith(".gz")
        uncompressed_filename = gz_filename.rstrip(".gz")
    gz = gzip.GzipFile(gz_filename, "r")
    create_file(uncompressed_filename, gz.read())
    gz.close()
