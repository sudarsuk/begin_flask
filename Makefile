all:
	@echo "Please see Makefile"
# endfold

run:
	@# run web interface on local
	export FLASK_APP=web.py; \
		export FLASK_DEBUG=1; \
		python -m flask run


