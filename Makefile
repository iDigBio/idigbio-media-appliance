version = $(shell python versioning.py --no-human get)

dist/pypi.json: idigbio_media_appliance/version.py
	mkdir -p dist
	curl -s https://pypi.python.org/pypi/idigbio-media-appliance/json -o dist/pypi.json

existing_dists: dist/pypi.json
	grep filename dist/pypi.json | awk '{print "dist/"$$2}' | tr -d '",' | xargs touch

existing_uploads: dist/pypi.json
	mkdir -p uploaded
	grep filename dist/pypi.json | awk '{print "uploaded/"$$2}' | tr -d '",' | xargs touch

dist/idigbio_media_appliance-%-py2.py3-none-any.whl: | existing_dists
	python setup.py bdist_wheel

dist/idigbio-media-appliance-%.tar.gz: | existing_dists
	python setup.py sdist

uploaded/%: dist/%
	twine upload $< > $@

pypi-%: uploaded/idigbio-media-appliance-%.tar.gz uploaded/idigbio_media_appliance-%-py2.py3-none-any.whl | existing_uploads
	echo pypi $@

v-%: pypi-%
	echo pypi $@

all: v-$(version)

clean:
	$(RM) -r build/*
	$(RM) dist/*
	$(RM) uploaded/*

build_client_js:
	browserify -t reactify -o idigbio_media_appliance/static/js/client.js client/client.js    

.PHONY: all clean
