TESTS = test_query.py util/test_debtags.py util/test_popcon.py

all: manual

view-man: manual
	groff -Tascii -N -man tagbugger.1 | $${PAGER:more}

manual: tagbugger.1

tagbugger.1: query_bugs.py synopsis.txt
	@help2man -i synopsis.txt -N ./query_bugs.py  >tagbugger.1

clean:
	@find . -type f -name "*.pyc" -delete

tests:
	@for t in ${TESTS}; do echo "running $${t}"; python $${t}; done
