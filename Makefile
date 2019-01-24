

help:
	@echo "Pick a release type by looking at the Makefile"

patch:
	./bin/semvergen --bump patch --filename setup.py

minor:
	./bin/semvergen --bump minor --filename setup.py

major:
	./bin/semvergen --bump major --filename setup.py

tag:
	./bin/semvergen --bump tag --filename setup.py

release:
	git add -u
	git commit -m"Checkin for release to pypi"
	git tag -a `./bin/semvergen --bareversion --filename setup.py` -m"Relase to PYPI"
	git push --tags
