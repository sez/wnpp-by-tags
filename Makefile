TESTS = test_wnpp_by_tags.py lib/test_debtags.py lib/test_popcon.py

all: manual

view-man: manual
	@groff -Tascii -man wnpp-by-tags.1 | $${PAGER:more}

manual: wnpp-by-tags.1

wnpp-by-tags.1: wnpp_by_tags.py manpage.txt
	@help2man -i manpage.txt -N ./wnpp_by_tags.py | sed -e '18,22d' >wnpp-by-tags.1

clean:
	@find . -type f -name "*.pyc" -delete

tests:
	@for t in ${TESTS}; do echo "running $${t}"; python $${t}; done
