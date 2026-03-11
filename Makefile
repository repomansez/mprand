PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
PROG = mprand
SRC = mprand.py

PYTHON ?= python3

.PHONY: install uninstall check-deps

check-deps:
	@$(PYTHON) -c "import mpd" >/dev/null 2>&1 || \
	( echo "Error: python-mpd2 is not installed."; \
	  echo "Install it with:"; \
	  echo "  pip install python-mpd2"; \
	  echo "or (FreeBSD): pkg install py311-mpd2"; \
	  exit 1 )

install: check-deps
	mkdir -p $(BINDIR)
	install -m 755 $(SRC) $(BINDIR)/$(PROG)

uninstall:
	rm -f $(BINDIR)/$(PROG)
