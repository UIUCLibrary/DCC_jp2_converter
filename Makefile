PYTHON      ?= python
PIP         ?= pip
TOX         ?= tox


current_dir = $(shell pwd)
SUBDIRS = build dist reports .cache .tox .eggs DCC_jp2_converter.egg-info

.PHONY: docs

all:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install

uninstall:
	$(PIP) uninstall DCC-jp2-converter -y

clean: cleanpython cleanextrafolders cleandocs

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

docs:
	cd docs && make html