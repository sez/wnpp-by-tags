TESTS = test_query.py lib/test_debtags.py lib/test_popcon.py

all: manual

view-man: manual
	groff -Tascii -man tagbugger.1 | $${PAGER:more}

manual: tagbugger.1

tagbugger.1: query_bugs.py manpage.txt
	@help2man -i manpage.txt -N ./query_bugs.py | sed -e '12,16d' >tagbugger.1

clean:
	@find . -type f -name "*.pyc" -delete

tests:
	@for t in ${TESTS}; do echo "running $${t}"; python $${t}; done
