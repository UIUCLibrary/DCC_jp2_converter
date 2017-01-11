PYTHON      ?= python
PIP         ?= pip
TOX         ?= tox


current_dir = $(shell pwd)
SUBDIRS = build dist .cache .tox .eggs DCC_jp2_converter.egg-info

.PHONY: docs tests cleanpython cleandocs cleanextrafolders cleanreports

all:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install

uninstall:
	$(PIP) uninstall DCC-jp2-converter -y

docs:
	cd docs && make html

tests:
	$(TOX) --skip-missing-interpreters

reports: tests
	$(TOX) --skip-missing-interpreters -e reports

clean: cleanpython cleanextrafolders cleandocs cleanreports
	@if [ -a .coverage ] ; \
	then \
		rm .coverage; \
	fi;

cleanpython:
	@$(PYTHON) setup.py clean

cleandocs:
	cd docs && make clean

cleanextrafolders:
	@for f in $(SUBDIRS); do \
		if [ -d $$f ]; then \
			echo "removing " $$f; \
			rm -R $$f; \
        fi; \
	done

cleanreports:
	@echo 'cleaning reports'
	@rm -fR reports/*

