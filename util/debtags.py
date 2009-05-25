from debian_bundle import debtags
import re

def gen_filter(match_tags, excl_tags):
    return lambda tags: match_tags.issubset(tags) and \
                        all(t not in excl_tags for t in tags)

def filter_pkgs(tag_db_fd, match_tags, excl_tags):
    db = debtags.DB()
    db.read(tag_db_fd)
    select = gen_filter(match_tags, excl_tags)
    return db.filter_packages_tags(lambda x: select(x[1]))

#print adb.package_count()
#for p in adb.iter_packages():
#        print p
