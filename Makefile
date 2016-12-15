PYTHON      ?= python
PIP         ?= pip
TOX         ?= tox
current_dir = $(shell pwd)

all:
	$(PYTHON) setup.py build

clean:
	@$(PYTHON) setup.py clean

	@if [ -d docs/build ]; then \
	    	echo 'deleting generated documentation'; \
		rm -R docs/build; \
    	fi

	@if [ -d build ]; then \
	    	echo 'deleting build'; \
    		rm -R build; \
    	fi

	@if [ -d dist ]; then \
		echo 'deleting dist'; \
		rm -R dist; \
	fi

	@if [ -d .cache ]; then \
		echo 'deleting cache'; \
		rm -R .cache; \
	fi

	@if [ -d .tox ]; then \
		echo 'deleting tox cache'; \
		rm -R .tox; \
	fi

	@if [ -d .eggs ]; then \
		echo 'deleting .egg cache'; \
		rm -R .eggs; \
	fi

	@if [ -d .cache ]; then \
		rm -R .cache; \
	fi

	@if [ -d DCC_jp2_converter.egg-info ]; then \
		echo 'Deleting DCC_jp2_converter.egg-info.'; \
		rm -R DCC_jp2_converter.egg-info; \
	fi
