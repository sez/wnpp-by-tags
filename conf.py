cache_dir = "/home/sez/fun/debian/participation/cache"
bugs_update_period_in_days = 7
popcon_update_period_in_days = 30
being_adopted_threshold_in_days = 150
being_packaged_threshold_in_days = 150

in_archive = ["orphaned", "help_requested", "being_adopted", "rfa_bypackage"]
not_in_archive = ["being_packaged", "requested"]
known_bug_types = set(in_archive)
known_bug_types.update(set(not_in_archive))
bug_types_to_query = in_archive

orphaned_file = "/home/sez/fun/debian/participation/cache/bugs/orphaned.html"
popcon_file = "/home/sez/fun/debian/participation/cache/popcon/all-popcon-results.txt"
