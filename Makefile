TESTS = $(shell ls -1 test_*py lib/test_*py)

all: manual

view-man: manual
	@groff -Tascii -man wnpp-by-tags.1 | $${PAGER:more}

manual: wnpp-by-tags.1

wnpp-by-tags.1: wnpp_by_tags.py manpage.txt
	@help2man -i manpage.txt -N ./wnpp_by_tags.py | sed -e '19,23d' >wnpp-by-tags.1

clean:
	@find . -type f -name "*.pyc" -delete

tests:
	@for t in ${TESTS}; do echo "running $${t}"; python $${t}; done
