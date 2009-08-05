#!/usr/bin/python

# html-format - format batch query results produced by wnpp_by_tags.py
# Copyright (C) 2009 Serafeim Zanikolas <serzan@hellug.gr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from glob import glob
import os
import sys
import time

from lib.util import create_file, ensure_dir_exists, giveup, warn

bugs_html_template =\
"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>WNPP bugs for tag %s</title>
    </head>

    <body>
        <h3>WNPP bugs for tag %s</h3>
        <table border="1">
            <tr>
                <th>bug type</th>
                <th>bug number</th>
                <th>package</th>
                <th>popcon</th>
                <th>dust</th>
            </tr>
        %s
        </table>
    <h6>updated nightly; last update: %s</h6>
    </body>
</html>
"""

facet_values_html_template =\
"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>WNPP bugs for facet %s</title>
    </head>

    <body>
        <h3>WNPP bugs for facet %s</h3>
        <table border="1">
            <tr>
                <th>%s</th>
                <th>wnpp bugs</th>
            </tr>
            %s
        </table>
    <h6>updated nightly; last update: %s</h6>
    </body>
</html>
"""

main_page_template =\
"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>Browse WNPP bugs based on debtags</title>
    </head>

    <body>
    Browse <a href="http://www.debian.org/devel/wnpp">WNPP bugs</a>
    based on the following
    <a href="http://debtags.alioth.debian.org/">debtags</a>:
    <ul>
      %s
    </ul>
    <p>
    (drop me an <a href="mailto:serzan-AT-hellug-DOT-gr">email</a> if there's
    another facet you'd like to see added here; see also <a
    href="http://wnpp.debian.net">wnpp.debian.net</a>)
    </p>
    <h6>updated nightly; last update: %s</h6>
    </body>
</html>
"""

def main():
    try:
        src_dir = sys.argv[1]
        dst_dir = sys.argv[2]
    except IndexError:
        warn("syntax: %s <src-dir> <dest-dir>" % os.path.basename(sys.argv[0]))
        giveup("src-dir is the directory hierarchy created by running wnpp_by_tags.py in batch mode")
        exit(1)
    if not os.path.isdir(src_dir):
        giveup("\"%s\" does not exist or is not a directory" % src_dir)
    facets = []
    timestamp = "%s-%s-%d %s:%s" % time.gmtime()[:5]
    for src_facet_dir in glob("%s/*" % src_dir):
        if not os.path.isdir(src_facet_dir):
            continue
        facet = src_facet_dir.split("/")[-1]
        facet_values = []
        facets.append(facet)
        for src_tag_file in glob("%s/*" % src_facet_dir):
            facet_value = os.path.basename(src_tag_file)
            dst_facet_dir = "%s/%s" % (dst_dir, facet)
            ensure_dir_exists(dst_facet_dir)
            bug_table_rows = []
            for line in open(src_tag_file).readlines():
                # the columns are: bug type, bug number, package, popcon, dust
                cols = line.rstrip().split(" ")
                _, bug_no, package_name, popcon = cols[:4]
                if len(cols) != 5:
                    sys.stderr.write("skipping invalid line \"%s\"" % line)
                    continue
                # add link for bug number and package
                cols[1] = '<a href="http://bugs.debian.org/%s">%s</a>' \
                        % (bug_no, bug_no)
                cols[2] = '<a href="http://packages.qa.debian.org/%s/%s.html">%s</a>' \
                        % (package_name[0], package_name, package_name)
                cols[3] = '<a href="http://qa.debian.org/popcon.php?package=%s">%s</a>' \
                        % (package_name, popcon)
                cols = "</td><td>".join(cols)
                bug_table_rows.append("<tr><td>%s</td></tr>" % cols)
            nbugs = len(bug_table_rows)
            if nbugs > 0: row = "<tr><td><a href=\"./%s.html\">%s</a></td><td>%d</td></tr>" \
                        % (facet_value, facet_value, nbugs)
            else:
                row = "<tr><td>%s</td><td>%d</td></tr>" % (facet_value, nbugs)
            facet_values.append(row)
            dst_tag_file = "%s/%s.html" % (dst_facet_dir, facet_value)
            # FIXME: use newstyle dicts instead
            tag = "%s::%s" % (facet, facet_value)
            html_doc = bugs_html_template % (tag, tag, "\n".join(bug_table_rows),
                                             timestamp)
            create_file(dst_tag_file, html_doc)
        content = facet_values_html_template % \
                (facet, facet, facet, "\n".join(sorted(facet_values)), timestamp)
        create_file("%s/index.html" % dst_facet_dir, content)
    formated_facets = ["<li><a href=\"./%s/index.html\">%s</a></li>" % (f, f)
                       for f in facets]
    create_file("%s/index.html" % dst_dir,
                main_page_template % ("\n".join(formated_facets), timestamp))

if __name__ == '__main__':
    main()
