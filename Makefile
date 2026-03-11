PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
PROG = mprand
SRC = mprand.py

install:
	mkdir -p $(BINDIR)
	install -m 755 $(SRC) $(BINDIR)/$(PROG)

uninstall:
	rm -f $(BINDIR)/$(PROG)
