# wnpp-by-tags - query WNPP bugs using the debtags of their packages
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

import os.path

from util import giveup, warn

class Config(object):
    def __init__(self, verbose=False, rcfile=None):
        # defaults
        self.bugs_update_period_in_days = 7
        self.popcon_update_period_in_days = 30
        # consider packages that are "being adopted" for at least this many days
        self.being_adopted_threshold_in_days = 150
        # consider packages that are "being packaged" for at least this many days
        #self.being_packaged_threshold_in_days = 150

        self.in_archive = ["orphaned", "help_requested", "being_adopted", "rfa_bypackage"]
        #self.not_in_archive = ["being_packaged", "requested"]
        self.known_bug_types = set(self.in_archive)
        #self.known_bug_types.update(set(self.not_in_archive))
        self.bug_types_to_query = self.in_archive
        if rcfile is None:
            rcfile = os.path.expanduser("~/.wnpp-by-tags.rc")
            if not os.path.exists(rcfile):
                return

        parse_int = lambda x: int(x)
        parse_set = lambda x: set(x.split(","))
        self.parsing_func = {
                "bugs_update_period_in_days" : parse_int,
                "popcon_update_period_in_days" : parse_int,
                "being_adopted_threshold_in_days" : parse_int,
                #"being_packaged_threshold_in_days" : parse_int,

                #"in_archive" : parse_set,
                "known_bug_types" : parse_set,
                "bug_types_to_query" : parse_set
                }
        for line in open(rcfile):
            if line.isspace() or line.startswith("#"):
                continue
            try:
                parameter, raw_value = line.replace(" ", "").strip().split("=")
                func = self.parsing_func.get(parameter)
                if func is None:
                    giveup('invalid parameter "%s" in %s' % (parameter, rcfile))
                Config.__setattr__(self, parameter, func(raw_value))
                if verbose:
                    print 'overriding default for %s' % parameter
            except (ValueError, KeyError):
                warn('warning: ignoring invalid line in %s:\n"%s"' % (rcfile, line))
