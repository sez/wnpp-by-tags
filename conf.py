cache_dir = "/home/sez/fun/debian/participation/cache"
bugs_update_period_in_days = 7
popcon_update_period_in_days = 30
# consider packages that are "being adopted" for at least this many days
being_adopted_threshold_in_days = 150
# consider packages that are "being packaged" for at least this many days
being_packaged_threshold_in_days = 150

in_archive = ["orphaned", "help_requested", "being_adopted", "rfa_bypackage"]
not_in_archive = ["being_packaged", "requested"]
known_bug_types = set(in_archive)
known_bug_types.update(set(not_in_archive))
bug_types_to_query = in_archive

